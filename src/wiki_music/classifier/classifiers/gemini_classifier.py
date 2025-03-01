import os
from google import genai
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv
import json
from typing import List, Dict

from wiki_music.utilities.types import TextLabel
from wiki_music.classifier.classifiers.config import GEMINI_PROMPT

load_dotenv()

# Initialize the Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configuration
BATCH_SIZE = 20  # Starting with a conservative batch size
MODEL = "gemini-2.0-flash"

def gemini_classifier(summaries: List[str]) -> List[TextLabel]:
    """Classify Wikipedia summaries to determine if they are about music.
    
    Args:
        summaries: List of one-sentence Wikipedia summaries
        
    Returns:
        List[TextLabel]: List of dictionaries containing the summary and classification
    """
    num_summaries = len(summaries)
    i = 0
    boolean_responses: List[bool] = []
    
    while i < num_summaries:
        upper_bound = min(i + BATCH_SIZE, num_summaries)
        batch_responses = gemini_wrapper(summaries[i:upper_bound])
        boolean_responses.extend(batch_responses)
        i += BATCH_SIZE
    
    return [
        {"summary": summaries[i], "is_music": boolean_responses[i]}
        for i in range(num_summaries)
    ]

def gemini_wrapper(summaries: List[str]) -> List[bool]:
    """Process a batch of summaries using Gemini API.
    
    Args:
        summaries: List of Wikipedia summaries to classify
        
    Returns:
        List[bool]: List of boolean classifications
    """
    if not summaries:
        return []
    
    prompt = GEMINI_PROMPT + "\n".join(f"{i+1}. {summary}" for i, summary in enumerate(summaries))

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=1024,
                response_mime_type="application/json",
            )
        )
        try:
            result = json.loads(response.text)
        except json.JSONDecodeError:
            print(f"Invalid JSON response format: {response.text}")
            raise ValueError("Invalid JSON response format")
        
        if "classifications" not in result:
            raise ValueError("Missing classifications in response")
        
        if len(result["classifications"]) != len(summaries):
            raise ValueError("Mismatched number of classifications")
            
        return result["classifications"]
        
    except Exception as e:
        print(f"Error processing batch: {e}")
        # Return conservative false classifications on error
        return [False] * len(summaries)

    
