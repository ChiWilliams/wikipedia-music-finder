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

def test_get_custom_dataset():
    sample_data = get_custom_dataset()[:2]

    assert isinstance(sample_data, list)
    assert len(sample_data) == 2
    assert all('summary' in item and 'is_music' in item for item in sample_data)

def test_load_dataset(test_jsonl_small):
    result = load_data(test_jsonl_small)
    assert result[0]['summary'] == 'Test 1'
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    assert all('summary' in item and 'is_music' in item for item in result)

def test_if_load_nonexistent_dataset_then_error():
    with pytest.raises(FileNotFoundError):
        load_data(Path('nonexistent.jsonl'))

    