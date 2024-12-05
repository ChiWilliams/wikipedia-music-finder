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
    if 'query' not in response_json:
        raise ValueError("Missing 'query' key in response")
    if 'pages' not in response_json['query']:
        raise ValueError("Missing 'pages' in query")

def get_random_ids(num_pages) -> list[str]:
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
    #print(data)

    return [str(x['id']) for x in data['query']['random']]

def build_getter_params(ids: list[str], continue_params: Dict[str, str] | None) -> WikiQuery:
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
    params = build_getter_params(ids, continue_params)
    response = requests.get(WIKIPEDIA_ENDPOINT, params=params)
    validate_wiki_response(response.json())
    response.raise_for_status()
    return response.json()

def merge_responses(base: WikiResponse, new: WikiResponse) -> None:
    for page_id, page_data in new['query']['pages'].items():
                if 'extract' in page_data:
                    base['query']['pages'][page_id]['extract'] = page_data['extract']

def get_full_summaries(ids: list[str]) -> list[str]:
    # the API call can only take 50 or fewer IDS at a time
    assert len(ids) <= 50

    summaries = get_wiki_pages(ids, None)
    continue_params = summaries.get('continue',{})
    while continue_params:
        new_summaries = get_wiki_pages(ids, continue_params)
        merge_responses(summaries, new_summaries)
        continue_params = new_summaries.get('continue', {})

    summaries_txt = [ x['extract'] for _,x in summaries['query']['pages'].items() if 'extract' in x]
    return summaries_txt

def first_sentences(summaries: list[str]) -> list[str]:
    return [ text_to_sentences(summary).split('\n')[0] for summary in summaries ]

def get_wikipedia_sentence_summaries(num_pages: int = 50) -> list[str]:
    ids = get_random_ids(num_pages)
    full_summaries = get_full_summaries(ids)
    return first_sentences(full_summaries)

if __name__ == "__main__":
    # ids = get_random_ids(5)
    # print(get_wiki_pages(get_random_ids(1)))

    summaries = get_wikipedia_sentence_summaries()
    print(summaries)
    print(f"{len(summaries)=}")
