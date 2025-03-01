import os
from pathlib import Path
from wiki_music.classifier.classifiers.gemini_classifier import gemini_classifier
from wiki_music.classifier.classifier_test_harness import small_evaluate_classifier, large_evaluate_classifier

# Set the data directory path
current_dir = Path(__file__).parent
data_dir = current_dir / 'data' / 'classified_data'
os.environ['WIKI_MUSIC_DATA_DIR'] = str(data_dir)

# Run the test
# small_evaluate_classifier(gemini_classifier) 
large_evaluate_classifier(gemini_classifier)