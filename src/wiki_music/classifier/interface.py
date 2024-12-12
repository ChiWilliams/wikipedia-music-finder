from wiki_music.classifier.classifier_metrics import ClassifierMetrics
from wiki_music.utilities.types import TextLabel
from wiki_music.utilities.data_processing import get_prompts_from_object

def validate_classifier_output(
    original_prompts: list[str],
    classifier_output: list[TextLabel]
) -> None:
    """
    Validates that classifier output meets all requirements
    Raises ValueError if any validation fails
    """
    if len(original_prompts) != len(classifier_output):
        raise ValueError(f"Classifier output length ({len(classifier_output)}) does not match input length ({len(original_prompts)})")
    
    if len(original_prompts) == 0:
        raise ValueError("Empty dataset provided")

    # Format validation
    for i, item in enumerate(classifier_output):
        if not isinstance(item, dict):
            raise TypeError(f"Item at index {i} is not a dictionary")
        
        # Check required keys exist
        if "summary" not in item or "is_music" not in item:
            raise ValueError(f"Missing required keys in item at index {i}")
            
        # Type checking
        if not isinstance(item["summary"], str):
            raise TypeError(f"Summary at index {i} is not a string")
        if not isinstance(item["is_music"], bool):
            raise TypeError(f"is_music at index {i} is not a boolean")

def classifier_harness(classifier: callable, dataset: list[TextLabel]) -> ClassifierMetrics:
    """This is an interface which takes in a callable function and returns it's classifier metrics,
    given a dataset
    
    Args:
        classifier: this is a callable function which takes in a list of summaries (list[str])
            and returns a list[TextLabel] object *in the same order as it was presented*
        dataset: this the 'ground truth' dataset upon which the classifier will be graded
        
    Returns:
        A ClassifierMetrics object, which contains information on how well the class did"""
    prompts = get_prompts_from_object(dataset)
    result = classifier(prompts)

    validate_classifier_output(prompts, result)
    return ClassifierMetrics(result, dataset)