import pytest

from wiki_music.utilities.types import TextLabel

@pytest.fixture
def simple_failure_classifier():
    """This classifier always returns 'is_music = True' on data made by create_labeled_data_from_bools"""
    def classifier(prompts: list[str]) -> list[TextLabel]:
           return [{"summary": prompt, "is_music": "music" in prompt.lower()} 
                for prompt in prompts]
    return classifier

@pytest.fixture
def simple_success_classifier():
    """This classifier always gets the correct response on data made by create_labeled_data_from_bools"""
    def classifier(prompts: list[str]) -> list[TextLabel]:
           return [{"summary": prompt, "is_music": not "not" in prompt.lower()} 
                for prompt in prompts]
    return classifier

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