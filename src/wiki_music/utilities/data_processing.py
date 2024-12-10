import json
import random
from pathlib import Path
import os

def get_data_path() -> Path:
    """Returns the path of the data_directory containing the dataset"""
    data_dir = os.getenv("WIKI_MUSIC_DATA_DIR")
    if data_dir is None:
        current_dir = Path(__file__).parent
        while not (current_dir / '.env').exists():
            current_dir = current_dir.parent
        data_dir = current_dir / 'data' / 'classfied_data'
    return Path(data_dir)

def get_custom_dataset() -> list[dict]:
    """This is a wrapper for get_data() which inputs the correct filename"""
    filename: Path = get_data_path() / 'classifications.jsonl'
    return get_data(filename)

#TODO: Ask Claude if filename can be typed for a specific file-type?
def get_data(filename: Path | str ) -> list[dict]:  #TODO: use custom types   
    """
    Read from a jsonl file and return a list of json objects
    
    Args:
        filename: Path to the JSONL file
    """
    with open(filename, "r") as jsonl:
        data = [json.loads(line) for line in jsonl]
        random.shuffle(data)
        return data

def summary_lengths(data: list[dict]) -> list[int]: #TODO: use custom types
    """This function returns a list of hte lengths of each summary"""
    return [len(x["summary"]) for x in data]

def get_five_of_each(data):
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

if __name__ == "__main__":
    print(get_custom_dataset()[:2])