from wiki_music.data_collection.get_urls import *

def test_get_url():
    assert get_url(56887264) == "https://en.wikipedia.org/wiki/Yannick_Schmid"

def test_get_random_ids():
    five_random_ids = get_random_ids(5)
    assert len(five_random_ids) == 5
    assert isinstance(five_random_ids[0], str)

def test_get_wiki_pages():
    id = '51628145'
    page = get_wiki_pages([id])
    assert 'query' in page
    assert 'pages' in page['query']
    assert page['query']['pages'][str(id)]['title'] == "Tony and Susan"
    assert 'extract' in page['query']['pages'][str(id)]

    pages = get_wiki_pages(get_random_ids(5))
    assert 'query' in pages
    assert 'pages' in pages['query']
    for page in pages['query']['pages'].values():
        assert 'extract' in page

    pages = get_wiki_pages(get_random_ids(30))
    assert 'query' in pages
    assert 'continue' in pages
    assert 'pages' in pages['query']
    assert 'extract' not in list(pages['query']['pages'].values())[-1]

def test_get_summaries():
    summaries = get_wikipedia_sentence_summaries(60)
    assert len(summaries) == 60
    assert isinstance(summaries[0], str)