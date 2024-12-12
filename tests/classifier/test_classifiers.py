import pytest
from wiki_music.classifier.interface import validate_classifier_output

class BaseClassifierInterface:
    """Base class for classifier testing"""

    @pytest.fixture
    def classifier(self):
        """Each classifier test class should overwrite this!"""
        raise NotImplementedError
    
    def test_classifier_follows_interface(self, classifier):
        test_inputs = ["A music piece", "Not music", "Another song"]
        result = classifier(test_inputs)
        validate_classifier_output(test_inputs, result)

class TestSimpleClassifier(BaseClassifierInterface):
    @pytest.fixture
    def classifier(self):
        from wiki_music.classifier.classifiers.simple import simple_classifier
        return simple_classifier