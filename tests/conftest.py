import pytest

from wiki_music.utilities.types import TextLabel

def create_labeled_data_from_bools(classifications: list[bool]) -> list[TextLabel]:
    return [
        {
            "summary": f"{'music' if is_music else 'not music'} {i}",
            "is_music": bool(is_music)
        }
        for i, is_music in enumerate(classifications)
    ]