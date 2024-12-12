from wiki_music.utilities.types import TextLabel

class ClassifierMetrics:
    def __init__(self,classified: list[TextLabel], baseline: list[TextLabel]) -> None:
        false_positives_and_negatives = self.classifier_false_positives_and_negatives(classified, baseline)
        self.false_positives: list[TextLabel] = false_positives_and_negatives['false_positives']
        self.false_negatives: list[TextLabel] = false_positives_and_negatives['false_negatives']

        self.accuracy: float = self.classifier_accuracy(classified, baseline)
        self.false_positive_rate, self.false_negative_rate = self.classifier_precision_recall(classified, baseline)

    @staticmethod
    def classifier_false_positives_and_negatives(
            classifier_result: list[TextLabel], 
            baseline_result: list[TextLabel] | None) -> dict[str, list[TextLabel]]:
        """This function takes in a list of classifications by a classifier and returns
        a list of false positives and a list of false negatives
        
        Args:
            classifier_result: List of classifications from the classifier being evaluated
            baseline_result: list of ground truth classifications
            
        Returns:
            Dictionary with keys 'false_positives' and 'false_negatives', each containing
            a list of TextLabel objects that were misclassified"""
        if len(classifier_result) == 0:
            raise ValueError("Classifier and baseline results must not be empty!")
        if len(classifier_result) != len(baseline_result):
            raise ValueError("Classifier_result must be same length as baseline_result")
        false_positives = [label for i,label in enumerate(classifier_result)
                        if label["is_music"] and not baseline_result[i]["is_music"]]
        false_negatives = [label for i,label in enumerate(classifier_result)
                        if not label["is_music"] and baseline_result[i]["is_music"]]
        return {'false_positives':false_positives, 'false_negatives': false_negatives}

    @staticmethod
    def classifier_accuracy(classifier_result: list[TextLabel], 
                            baseline_result: list[TextLabel] | None) -> float:
        """Calculate accuracy against baseline results
        
        Args:
            classifier_result: List of classifications from the classifier being evaluated
            baseline_result: List of ground truth classifications
            
        Returns:
            float from 0 to 1"""
        false_pos_percent, false_neg_percent = ClassifierMetrics.classifier_precision_recall(classifier_result,baseline_result)
        return 1 - (false_pos_percent + false_neg_percent)

    @staticmethod
    def classifier_precision_recall(classifier_result: list[TextLabel],
                                    baseline_result: list[TextLabel] | None) -> tuple[float, float]:
        """Returns the false negative and false positive rate as a tuple
        
        Args:
            classifier_result: List of classifications from the classifier being evaluated
            baseline_result: List of ground truth classifications
            
        Returns:
            tuple with false positive and false negative rate"""
        errors = ClassifierMetrics.classifier_false_positives_and_negatives(classifier_result, baseline_result)
        num_false_positive = len(errors["false_positives"])
        num_false_negatives = len(errors["false_negatives"])
        n = len(classifier_result)
        return num_false_positive/n, num_false_negatives/n