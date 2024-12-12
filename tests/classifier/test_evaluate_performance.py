import pytest
from wiki_music.classifier.test_results import *
from conftest import create_labeled_data_from_bools

def assert_accuracy_classifier_relationship(result: ClassifierMetrics) -> None:
    assert result.accuracy + result.false_negative_rate + result.false_positive_rate == 1

def assert_test_result(
        result: ClassifierMetrics,
        expected_false_positives: int,
        expected_false_negatives: int,
        expected_accuracy: float,
        expected_rates: tuple[float, float]
) -> None:
    """Helper function to verify all attributes of a TestResult object"""
    assert len(result.false_positives) == expected_false_positives
    assert len(result.false_negatives) == expected_false_negatives
    assert result.accuracy == expected_accuracy
    assert (result.false_positive_rate, result.false_negative_rate) == expected_rates
    assert_accuracy_classifier_relationship(result)

def test_perfect_classification():
    labels = [True, True, False, True, True]
    classifier = create_labeled_data_from_bools(labels)
    baseline = create_labeled_data_from_bools(labels)

    result = ClassifierMetrics(classifier, baseline)
    assert_test_result(result, 0, 0, 1.0, (0.0,0.0))
    

def test_all_false_positives():
    baseline = create_labeled_data_from_bools([False, False, False])
    classifier = create_labeled_data_from_bools([True, True, True])
    
    result = ClassifierMetrics(classifier, baseline)
    assert_test_result(result, 3, 0, 0.0, (1.0, 0.0))
    

def test_all_false_negatives():
    baseline = create_labeled_data_from_bools([True, True, True])
    classifier = create_labeled_data_from_bools([False, False, False])

    result = ClassifierMetrics(classifier, baseline)
    assert_test_result(result, 0, 3, 0.0, (0.0, 1.0))

def test_mixed_errors():
    baseline = create_labeled_data_from_bools([True, False, True, False])
    classifier = create_labeled_data_from_bools([False, True, True, False])

    result = ClassifierMetrics(classifier, baseline)
    assert_test_result(result, 1, 1, 0.5, (0.25, 0.25))

def test_mismatched_length_error():
    baseline = create_labeled_data_from_bools([True, False])
    classifier = create_labeled_data_from_bools([False])
    with pytest.raises(ValueError):
        ClassifierMetrics(classifier, baseline)

def test_empty_classification_error():
    baseline = create_labeled_data_from_bools([])
    classifier = create_labeled_data_from_bools([])
    with pytest.raises(ValueError):
        ClassifierMetrics(classifier, baseline)  

def test_wrong_input_error_raises_type_error():
    baseline = [True, True, True]
    classifier = [True, True, True]
    with pytest.raises(TypeError):
        ClassifierMetrics(classifier, baseline)                                        



# def test_perfect_accuracy_classifier_accuracy_is_one():
#     labels = [1, 1, 0, 1, 1]
#     classifier = create_labeled_data_from_bools(labels)
#     baseline = create_labeled_data_from_bools(labels)
#     assert classifier_accuracy(classifier, baseline) == 1



