from wiki_music.utilities.data_processing import get_five_of_each, get_custom_dataset
from wiki_music.classifier.interface import classifier_harness
import time

def evaluate_classifier_performance(classifier, dataset):
    start_time = time.time()
    result = classifier_harness(classifier, dataset)
    end_time = time.time()
    print(f"It took {end_time-start_time} seconds")
    print(result)
    print()


def small_evaluate_classifier(classifier):
    dataset = get_five_of_each()
    evaluate_classifier_performance(classifier, dataset)
    

def large_evaluate_classifier(classifier):
    dataset = get_custom_dataset()
    evaluate_classifier_performance(classifier, dataset)

if __name__ == "__main__":
    from wiki_music.classifier.classifiers.gemini_classifier import gemini_classifier
    from wiki_music.classifier.classifiers.simple import simple_classifier
    # small_evaluate_classifier(simple_classifier)
    # large_evaluate_classifier(simple_classifier)
    small_evaluate_classifier(gemini_classifier)
    # large_evaluate_classifier(gemini_classifier)
