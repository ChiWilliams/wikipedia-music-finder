import json
import random

def get_data() :
    with open("classifications.jsonl", "r") as jsonl:
        data = [json.loads(line) for line in jsonl]
        random.shuffle(data)
        return data


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

print(get_five_of_each())