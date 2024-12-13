import pytest
from unittest.mock import MagicMock
from wiki_music.classifier.classifiers.gpt_classifier import *

@pytest.fixture
def mock_openai_client(monkeypatch):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.tool_calls[0].function.arguments = '{"classifications": [true, false]}'
    mock_client.chat.completions.create.return_value = mock_response
    monkeypatch.setattr("wiki_music.classifier.classifiers.gpt_classifier.client", mock_client)
    return mock_client

def test_gpt_wrapper_basic(mock_openai_client):
    summaries = ["Love is a song about love.", "Warrior is a book about war"]
    result = gpt_wrapper(summaries, "system prompt", "user prompt")
    assert len(result) == 2
    assert isinstance(result[0], bool)

def test_gpt_classifier_batching():
    """Test that batching works correctly"""
    summaries = ["summary"] * 75  # More than one batch
    result = gpt_classifier(summaries)
    assert len(result) == 75

def test_gpt_wrapper_batch_size():
    """Test batch size assertion"""
    with pytest.raises(AssertionError):
        gpt_wrapper(["summary"] * (BATCH_SIZE + 1), "", "")

def test_gpt_wrapper_empty_input():
    """Test behavior with empty list"""
    result = gpt_wrapper([], "", "")
    assert isinstance(result, list)
    print(result)
    assert len(result) == 0

def test_response_length_matches_input(mock_openai_client):
    """Test that we get one classification per summary"""
    summaries = ["test1", "test2"]
    result = gpt_wrapper(summaries, "", "")
    assert len(result) == len(summaries)

def test_gpt_classifier_preserves_order():
    """Test that summaries and classifications stay aligned"""
    summaries = ["A", "B", "C"]
    results = gpt_classifier(summaries)
    assert [r["summary"] for r in results] == summaries