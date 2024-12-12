import pytest
from wiki_music.classifier.evaluate_performance import *
from conftest import create_labeled_data_from_bools

@pytest.mark.parametrize("func,expected", [
    (classifier_false_positives_and_negatives, {"false_positives": [], "false_negatives" : []}),
    (classifier_accuracy, 1.0),
    (classifier_precision_recall, (0.0, 0.0))
])
def test_perfect_classification(func, expected):
    labels = [True, True, False, True, True]
    classifier = create_labeled_data_from_bools(labels)
    baseline = create_labeled_data_from_bools(labels)
    assert func(classifier, baseline) == expected
    

def test_all_false_positives():
    baseline = create_labeled_data_from_bools([False, False, False])
    classifier = create_labeled_data_from_bools([True, True, True])
    result = classifier_false_positives_and_negatives(classifier, baseline)
    assert len(result["false_positives"]) == 3
    assert len(result["false_negatives"]) == 0
    assert all(item["is_music"] for item in result["false_positives"])

def test_all_false_negatives():
    baseline = create_labeled_data_from_bools([True, True, True])
    classifier = create_labeled_data_from_bools([False, False, False])
    result = classifier_false_positives_and_negatives(classifier, baseline)
    assert len(result["false_positives"]) == 0
    assert len(result["false_negatives"]) == 3
    print("Result is", [result["false_negatives"]])
    assert all(not item["is_music"] for item in result["false_negatives"])

def test_mixed_errors():
    baseline = create_labeled_data_from_bools([True, False, True, False])
    classifier = create_labeled_data_from_bools([False, True, True, False])
    result = classifier_false_positives_and_negatives(classifier, baseline)
    assert len(result["false_positives"]) == 1
    assert len(result["false_negatives"]) == 1

def test_mismatched_length_error():
    baseline = create_labeled_data_from_bools([True, False])
    classifier = create_labeled_data_from_bools([False])
    with pytest.raises(ValueError):
        classifier_false_positives_and_negatives(classifier, baseline)

def test_empty_classification_error():
    baseline = create_labeled_data_from_bools([])
    classifier = create_labeled_data_from_bools([])
    with pytest.raises(ValueError):
        classifier_false_positives_and_negatives(classifier, baseline)  

def test_wrong_input_error_raises_type_error():
    baseline = [True, True, True]
    classifier = [True, True, True]
    with pytest.raises(TypeError):
        classifier_false_positives_and_negatives(classifier, baseline)                                        



# def test_perfect_accuracy_classifier_accuracy_is_one():
#     labels = [1, 1, 0, 1, 1]
#     classifier = create_labeled_data_from_bools(labels)
#     baseline = create_labeled_data_from_bools(labels)
#     assert classifier_accuracy(classifier, baseline) == 1



