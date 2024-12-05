import requests, time
from blingfire import text_to_sentences

def get_random_summaries(num_pages = 50):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
    "action": "query",
    "format": "json",
    "list": "random",
    "formatversion": "2",
    "rnnamespace": "0",
    "rnlimit": num_pages,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    page_ids = [str(x['id']) for x in data['query']['random']]

    summary_params = {
    "action": "query",
    "format": "json",
    "prop": "extracts",
    "exintro": True,
    "explaintext": True,
    "pageids": "|".join(page_ids)
    }

    summaries = requests.get(url, params=summary_params)
    summaries.raise_for_status()
    summaries_JSON = summaries.json()
    continue_params = summaries.json().get('continue',{})
    while continue_params:
        summary_params.update(continue_params)
        summaries = requests.get(url, params = summary_params)
        try:
            summaries.raise_for_status()
            new_response = summaries.json()
            for page_id, page_data in new_response['query']['pages'].items():
                if 'extract' in page_data:
                    summaries_JSON['query']['pages'][page_id]['extract'] = page_data['extract']
            print("---")
            continue_params = new_response.get('continue', {})
        except:
            break

    summaries_txt = [ x['extract'] for _,x in summaries_JSON['query']['pages'].items() if 'extract' in x]
    return summaries_txt

def first_sentences(summaries):
    return [ text_to_sentences(summary).split('\n')[0] for summary in summaries ]


if __name__ == "__main__":
    start_time = time.time()
    summs = get_random_summaries()
    summs_got_time = time.time()
    summaries = first_sentences(summs)
    end_time = time.time()
    print(summaries)
    print(f"{len(summaries)=}")
    print(f"This took {summs_got_time - start_time} seconds to get summaries")
    print(f"This took {end_time-summs_got_time} seconds to split summaries")
