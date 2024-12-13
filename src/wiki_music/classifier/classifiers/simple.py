from wiki_music.utilities.types import TextLabel

KEYWORDS = ["song", "single", "musician", "album", "ep", "lp", "music"]

def contains_music_word(summary: str) -> TextLabel:
    return any(word in summary.lower() for word in KEYWORDS)

def simple_classifier(data: list[str]) -> list[TextLabel]:
    return [
        {"summary": summary, "is_music": contains_music_word(summary)}
        for summary in data
    ]