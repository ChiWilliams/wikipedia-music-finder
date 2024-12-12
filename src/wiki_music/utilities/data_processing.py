import json
import random
from pathlib import Path
import os

from wiki_music.utilities.types import TextLabel

CLASSIFICATION_FILE = 'classifications.jsonl'

def get_data_path() -> Path:
    """Returns the path of the data_directory containing the dataset"""
    data_dir = os.getenv("WIKI_MUSIC_DATA_DIR")
    if data_dir is None:
        current_dir = Path(__file__).parent
        while not (current_dir / 'setup.py').exists():
            current_dir = current_dir.parent
        data_dir = current_dir / 'data' / 'classfied_data'
    return Path(data_dir)

def get_custom_dataset() -> list[TextLabel]:
    """This is a wrapper for get_data() which inputs the correct filename"""
    filename: Path = get_data_path() / CLASSIFICATION_FILE
    return get_data(filename)

def load_data(filename: Path) -> list[TextLabel]:
    """Just loads the data"""
    with open(filename, "r") as jsonl:
        return [json.loads(line) for line in jsonl]

def get_data(filename: Path | str ) -> list[TextLabel]: 
    """
    Read from a jsonl file and return a shuffled_list of the data
    
    Args:
        filename: Path to the JSONL file
    """
    data = load_data(filename)
    random.shuffle(data)
    return data

def get_prompts_from_object(data: list[TextLabel]) -> list[str]:
    return [label['summary'] for label in data]

def summary_lengths(data: list[TextLabel]) -> list[int]: 
    """This function returns a list of the lengths of each summary"""
    return [len(x["summary"]) for x in data]

def get_five_of_each(data: list[TextLabel] | None = None) -> list[TextLabel]:
    """
    This function returns 5 music examples and 5 non_music examples

    Returns:
        Returns a list of JSON objects with two attributes
            "summary": The first sentence of a wikipedia article
            "is_music": a boolean classification
    """
    if data is None:
        data = get_custom_dataset()

    i = 0
    num_music, num_non_music = 0, 0

    return_list = []
    while num_music < 5 or num_non_music < 5:
        try:
            labelled_summary = data[i]
            if labelled_summary['is_music'] and num_music < 5:
                return_list.append(labelled_summary)
                num_music += 1
            if not labelled_summary['is_music'] and num_non_music < 5:
                return_list.append(labelled_summary)
                num_non_music += 1
            i += 1
        except IndexError:
            raise ValueError(f"Insufficient number of music examples ({num_music}) or non-music examples ({num_non_music})")
    return return_list
