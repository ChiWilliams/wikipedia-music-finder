from typing import Optional, Tuple, Dict, List

from wiki_music.data_collection.get_urls import get_wikipedia_summaries_and_ids, get_url
from wiki_music.classifier.classifiers.gemini_classifier import gemini_classifier

def get_random_music_url(batch_size: int = 50, max_attempts: int = 3) -> str:
    """Find a random Wikipedia URL about music.
    
    This function combines the Wikipedia summary collector with the Gemini classifier
    to find a random Wikipedia article about music. It will make multiple attempts
    if necessary.
    
    Args:
        batch_size: Number of Wikipedia summaries to fetch per attempt
        max_attempts: Maximum number of batches to try before giving up
        
    Returns:
        str: URL to a Wikipedia article about music
        
    Raises:
        ValueError: If no music article is found after max_attempts
    """
    url, _ = get_random_music_url_with_summary(batch_size, max_attempts)
    return url

def get_random_music_url_with_summary(batch_size: int = 50, max_attempts: int = 3) -> Tuple[str, str]:
    """Like get_random_music_url but also returns the summary.
    
    Args:
        batch_size: Number of Wikipedia summaries to fetch per attempt
        max_attempts: Maximum number of batches to try before giving up
    
    Returns:
        Tuple[str, str]: (URL, summary) pair for a random music article
        
    Raises:
        ValueError: If no music article is found after max_attempts
    """
    attempts = 0
    
    while attempts < max_attempts:
        # Get summaries and IDs
        summary_id_pairs = get_wikipedia_summaries_and_ids(batch_size)
                
        # Extract just the summaries for classification
        summaries = [summary for summary, _ in summary_id_pairs]
        
        # Classify the summaries
        classifications = gemini_classifier(summaries)
        
        # Find the first music article
        for i, classification in enumerate(classifications):
            if classification["is_music"]:
                summary, article_id = summary_id_pairs[i]
                url = get_url(str(article_id))
                return url, summary
        
        attempts += 1
    
    raise ValueError(f"No music articles found after {max_attempts} attempts "
                    f"(checked {max_attempts * batch_size} articles)") 