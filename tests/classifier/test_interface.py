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