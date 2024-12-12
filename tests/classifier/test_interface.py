import pytest
from conftest import create_labeled_data_from_bools
from wiki_music.classifier.interface import *

def test_interface_preserves_metrics(simple_failure_classifier):
    """Ensure basic metrics functionality works regardless of implementation"""
    simple_dataset = create_labeled_data_from_bools([True, True, False])
    results = classifier_harness(simple_failure_classifier, simple_dataset)
    assert hasattr(results, 'accuracy')
    assert hasattr(results, 'false_positives')
    assert hasattr(results, 'false_negatives')

def test_when_given_wrong_input_raises_type_error(simple_failure_classifier):
    """Ensure basic metrics functionality works regardless of implementation"""
    simple_dataset = ["Music", "not music", "bob."]
    with pytest.raises(TypeError):
        results = classifier_harness(simple_failure_classifier, simple_dataset)

def test_interface_perfect_classification(simple_success_classifier):
    simple_dataset = create_labeled_data_from_bools([True, True, False, False])
    results = classifier_harness(simple_success_classifier, simple_dataset)
    print(results)
    assert results.accuracy == 1.0
    assert results.false_positive_rate == 0
    assert results.false_negative_rate == 0
    
def test_interface_all_wrong(simple_failure_classifier):
    """Test when classifier gets everything wrong"""
    simple_dataset = create_labeled_data_from_bools([False, False, False])
    results = classifier_harness(simple_failure_classifier, simple_dataset)
    assert results.accuracy == 0.0
    assert results.false_positive_rate == 1.0
    assert results.false_negative_rate == 0

    
def test_interface_empty_dataset(simple_failure_classifier):
    """Test behavior with empty dataset"""
    empty_dataset = []
    with pytest.raises(Exception):
        results = classifier_harness(simple_failure_classifier, empty_dataset)

def test_interface_malformed_text_label(simple_failure_classifier):
    """Test behavior when TextLabel is missing required fields"""
    malformed_dataset = [{"summary": "music", "is_music": True}, {"is_music": False}]
    with pytest.raises(Exception):
                results = classifier_harness(simple_failure_classifier, malformed_dataset)
    
def test_interface_none_classifier():
    """Test behavior when classifier is None"""
    simple_dataset = create_labeled_data_from_bools([True, True, False])
    with pytest.raises(Exception):
        results = classifier_harness(None, simple_dataset)

def test_interface_wrong_type():
    """Test behavior when classifier is None"""
    simple_dataset = create_labeled_data_from_bools([True, True, False])
    with pytest.raises(ValueError):
        results = classifier_harness(simple_dataset, simple_dataset)