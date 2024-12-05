import requests, time
from requests.exceptions import HTTPError
from blingfire import text_to_sentences
from typing import TypedDict, Dict

WIKIPEDIA_ENDPOINT = 'https://en.wikipedia.org/w/api.php'

class WikiPage(TypedDict):
    extract: str
    ns: int
    pageid: int
    title: str

class WikiQuery(TypedDict):
     pages: Dict[str, WikiPage]
    
class WikiContinue(TypedDict, total=False):
    batchcomplete: str
WikiContinue.__annotations__['continue'] = Dict[str,str]

class WikiResponse(WikiQuery, WikiContinue):
     query: WikiQuery


def validate_wiki_response(response_json: WikiResponse) -> None:
    """
    This function validates whether a given response from the Wikimedia API has the
    expected structure.

    Args:
        response_json: This is a JSON from a Wikimedia API query made by get_wiki_pages
    
    Raises:
        Raises a ValueError if the structure doesn't work
    """
    if 'query' not in response_json:
        raise ValueError("Missing 'query' key in response")
    if 'pages' not in response_json['query']:
        raise ValueError("Missing 'pages' in query")

def get_random_ids(num_pages: int) -> list[str]:
    """
    This function gets the ids of wikipedia pages using the Wikimedia API

    Args:
        num_pages: int, Must be between 1 and 500
    
    Returns:
        a list of strings with the ids of the pages
    """
    assert 1 <= num_pages <= 500
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "formatversion": "2",
        "rnnamespace": "0",
        "rnlimit": num_pages,
    }

    response = requests.get(WIKIPEDIA_ENDPOINT, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    return [str(x['id']) for x in data['query']['random']]

def build_getter_params(ids: list[str], continue_params: Dict[str, str] | None) -> WikiQuery:
    """
    This function takes in the ids of wikipedia and formats the parameters for a wikimedia API call

    Note that the hard-coded parameters are for building a query from pages

    Args:
        ids: a list of the pageids of the desired wikimedia
        continue_params: When the Wikimedia API is unable to complete a request, it sends a key noting
            what still needs to be done. This is a dict. If the response is complete, continue_params
            is None

    Returns:
        A JSON of parameters following the WikiQuery class type 
    """
    continue_params = continue_params or {}
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "pageids": "|".join(ids)
    }
    params.update(continue_params)
    return params

def get_wiki_pages(ids: list[str], continue_params: WikiContinue | None = None) -> WikiResponse:
    """
    This method takes in a list of page ids and any continue_parameters and makes a wikimedia API call

    args:
        ids: list of ids
        continue_params: When the Wikimedia API is unable to complete a request, it sends a key noting
            what still needs to be done. This is a dict. If the response is complete, continue_params
            is None
    
    returns:
        A JSON structure that should follow the structure of WikiResponse
    """
    params = build_getter_params(ids, continue_params)
    response = requests.get(WIKIPEDIA_ENDPOINT, params=params)
    validate_wiki_response(response.json())
    response.raise_for_status()
    return response.json()

def merge_responses(base: WikiResponse, new: WikiResponse) -> None:
    """This is a helper function which modifies the JSON with summaries
    to include any new summaries"""
    for page_id, page_data in new['query']['pages'].items():
                if 'extract' in page_data:
                    base['query']['pages'][page_id]['extract'] = page_data['extract']

def get_all_wiki_responses(ids: list[str]) -> WikiResponse:
    """
    This function takes in a list of pagesids and returns a full response. 
    This can take a couple of API calls, done through get_wiki_pages()
    """
    # the API call can only take 50 or fewer IDS at a time
    summaries = get_wiki_pages(ids, None)
    continue_params = summaries.get('continue',{})
    while continue_params:
        new_summaries = get_wiki_pages(ids, continue_params)
        merge_responses(summaries, new_summaries)
        continue_params = new_summaries.get('continue', {})
    return summaries
    
def get_full_summaries(ids: list[str]) -> list[str]:
    """Extract summaries from Wikipedia response"""
    assert len(ids) <= 50
    wiki_responses = get_all_wiki_responses(ids)
    return [ x['extract'] 
                for _,x in wiki_responses['query']['pages'].items() 
                if 'extract' in x]

def first_sentences(summaries: list[str]) -> list[str]:
    """Uses the blingfire package to get the first sentence of a list of strings"""
    return [ text_to_sentences(summary).split('\n')[0] for summary in summaries ]

def get_wikipedia_sentence_summaries(num_pages: int = 50) -> list[str]:
    """Using multiple API calls, this function returns a given number of random 
    wikipedia page summaries."""
    assert num_pages > 0
    ids = get_random_ids(num_pages)
    full_summaries = get_full_summaries(ids)
    return first_sentences(full_summaries)

if __name__ == "__main__":
    # ids = get_random_ids(5)
    # print(get_wiki_pages(get_random_ids(1)))

    summaries = get_wikipedia_sentence_summaries()
    print(summaries)
    print(f"{len(summaries)=}")
