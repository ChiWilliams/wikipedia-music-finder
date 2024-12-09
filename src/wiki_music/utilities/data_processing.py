import json
import random

#TODO: Ask Claude if filename can be typed for a specific file-type?
def get_data(filename) -> list[dict]:  #TODO: use custom types   
    """This function reads from a jsonl file and returns a list of json objects"""
    with open(filename, "r") as jsonl:
        data = [json.loads(line) for line in jsonl]
        random.shuffle(data)
        return data

def summary_lengths(data: list[dict]) -> list[int]: #TODO: use custom types
    """This function returns a list of hte lengths of each summary"""
    return [len(x["summary"]) for x in data]

def get_five_of_each(data = get_data()):
    """
    This function returns 5 music examples and 5 non_music examples

    Returns:
        Returns a list of JSON objects with two attributes
            "summary": The first sentence of a wikipedia article
            "is_music": a boolean classification
    """
    i = 0
    num_music, num_non_music = 0, 0

    return_list = []
    while num_music < 5 or num_non_music < 5:
        labelled_summary = data[i]
        if labelled_summary['is_music'] and num_music < 5:
            return_list.append(labelled_summary)
            num_music += 1
        if not labelled_summary['is_music'] and num_non_music < 5:
            return_list.append(labelled_summary)
            num_non_music += 1
        i += 1
    return return_list

def random_func():
    print("I was called!")