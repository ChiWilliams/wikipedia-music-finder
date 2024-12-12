import pytest

from wiki_music.utilities.types import TextLabel

def create_labeled_data_from_bools(classifications: list[bool]) -> list[TextLabel]:
    """This is a helper function that, given a list of boolean classifications, returns an array of objects
    
    Example:
        create_labeled_data_from_bools([True, False]) returns
            [
                {"summary":'music 0', "is_music": True}, 
                {"summary":'not music 1', "is_music": False},
            ]
    """
    return [
        {
            "summary": f"{'music' if is_music else 'not music'} {i}",
            "is_music": bool(is_music)
        }
        for i, is_music in enumerate(classifications)
    ]