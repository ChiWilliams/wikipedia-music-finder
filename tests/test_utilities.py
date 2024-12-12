import pytest
from wiki_music.utilities.data_processing import *

@pytest.fixture
def test_data_content_small():
    return [
    '{"summary": "Test 1", "is_music": true}\n',
    '{"summary": "Test 2", "is_music": false}\n'
    ]

@pytest.fixture
def test_jsonl_small(tmp_path, test_data_content_small):
    test_file = tmp_path / "test_small.jsonl"
    test_file.write_text("".join(test_data_content_small))
    return test_file

def create_n_music_m_non_music(n: int, m: int) -> list[dict]:
    data = [{"summary": "music sentence", "is_music": True}]*n + [{"summary": "not music sentence", "is_music": False}]*m
    return data

def assert_valid_music_data_format(data):
    """Helper function to validate music data format"""
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('summary' in item and 'is_music' in item for item in data)
    assert all(isinstance(item, dict) for item in data)


def test_get_data_path_respects_env_var(monkeypatch):
    test_path = Path('dummy/test/path')
    monkeypatch.setenv('WIKI_MUSIC_DATA_DIR', str(test_path))
    assert get_data_path() == test_path

def test_get_data_path_finds_directory():
    path = get_data_path()
    assert isinstance(path, Path)
    assert path.exists(), f"Path {path} does not exist"
    assert path.is_dir(), f"Path {path} is not a directory"
    # Maybe test that is in directory, but not high priority

def test_get_data_leads_to_loadable_data():
    path = get_data_path()
    data_file = path / CLASSIFICATION_FILE
    assert data_file.exists(), "Data file not found in data directory"

    try:
        data = load_data(data_file)
        assert_valid_music_data_format(data)
    except json.JSONDecodeError:
        pytest.fail("File exists but contains invalid JSON data")

def test_get_custom_dataset():
    data = get_custom_dataset()[:2]

    assert_valid_music_data_format(data)
    assert len(data) == 2

def test_load_data(test_jsonl_small):
    data = load_data(test_jsonl_small)
    assert data[0]['summary'] == 'Test 1'
    assert len(data) == 2
    assert all(isinstance(item, dict) for item in data)
    assert_valid_music_data_format(data)

def test_summary_lengths(test_jsonl_small):
    result = load_data(test_jsonl_small)
    assert summary_lengths(result) == [len("Test 1"), len("Test 2")]

def test_if_load_nonexistent_dataset_then_error():
    with pytest.raises(FileNotFoundError):
        load_data(Path('nonexistent.jsonl'))

def test_get_five_of_each_basic():
    n, m = 5, 5
    data = create_n_music_m_non_music(n, m)
    result = get_five_of_each(data)
    assert len(result) == 10
    assert sum(1 for x in result if x["is_music"]) == 5
    assert sum(1 for x in result if not x["is_music"]) == 5

def test_get_five_of_each_insufficient_music():
    n, m = 2, 5
    data = create_n_music_m_non_music(n, m)
    with pytest.raises(ValueError, match="Insufficient number of"):
        get_five_of_each(data)

def test_get_five_of_each_insufficient_non_music():
    n, m = 5, 3
    data = create_n_music_m_non_music(n, m)
    with pytest.raises(ValueError, match="Insufficient number of"):
        get_five_of_each(data)

def test_get_five_of_each_insufficient_both():
    n, m = 3,3
    data = create_n_music_m_non_music(n, m)
    with pytest.raises(ValueError, match="Insufficient number of"):
        get_five_of_each(data)

