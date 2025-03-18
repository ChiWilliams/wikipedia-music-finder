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

def get_url(id: str) -> str:
    """This gets an id and returns the url"""
    try:
        id = int(id)
    except ValueError:
        raise ValueError("Get_url only accepts an integer, or a string of an integer:", id)
    params = {
        "action": "query",
        "format": "json",
        "prop": "info",
        "inprop": "url",
        "pageids": id
    }
    response = requests.get(WIKIPEDIA_ENDPOINT, params=params)
    response.raise_for_status()
    return response.json()['query']['pages'][str(id)]['fullurl']

def get_wiki_pages(ids: list[str], continue_params: WikiContinue | None = None) -> WikiResponse:
    """
    This method takes in a list of page ids and any continue_parameters and makes a wikimedia API call
    The wikimedia call includes an extract.

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
    to include any new summaries
    Returns: None
    Side effects: mutates the base WikiResponse object!"""
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
    """Extract summaries from Wikipedia response in the same order as the input IDs"""
    assert len(ids) <= 50
    wiki_responses = get_all_wiki_responses(ids)
    pages = wiki_responses['query']['pages']
    
    # Return summaries in the same order as input IDs
    return [
        pages[id_str]['extract']
        for id_str in ids
        if 'extract' in pages[id_str]
    ]

def first_sentences(summaries: list[str]) -> dict[str,str]:
    """Uses the blingfire package to get the first sentence of a list of strings"""
    return [ text_to_sentences(summary).split('\n')[0] for summary in summaries ]

def get_wikipedia_summaries_and_ids(num_pages: int = 50) -> list[tuple[str, int]]:
    """Using multiple API calls, this function returns a given number of random 
    wikipedia page summaries. It splits the num_pages into batches of 50
    
    Returns:
        List of (summary, id) tuples in the order they were fetched
    """
    assert num_pages > 0
    result = []
    summaries_remaining = num_pages
    while summaries_remaining > 0:
        #divide into batches of 50, for API call reasons
        batch_size = min(summaries_remaining, 50)
        summaries_remaining -= batch_size

        batch_ids = get_random_ids(batch_size)
        full_summaries = get_full_summaries(batch_ids)
        first_sentences_list = first_sentences(full_summaries)
        
        # Create tuples of (summary, id) in order
        result.extend(list(zip(first_sentences_list, map(int, batch_ids))))

    return result

def get_wikipedia_sentence_summaries(num_pages: int = 50) -> list[str]:
    """This is a wrapper for get_wikipedia_summaries_and_ids which just gets the summaries"""
    return [summary for summary, _ in get_wikipedia_summaries_and_ids(num_pages)]

if __name__ == "__main__":
    print(get_wiki_pages(get_random_ids(30)))

    # summaries = get_wikipedia_sentence_summaries(60)
    # print(summaries)
    # print(f"{len(summaries)=}")