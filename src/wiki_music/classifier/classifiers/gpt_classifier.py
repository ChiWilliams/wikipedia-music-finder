# In this file, we make a GPT classifier
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

from wiki_music.utilities.types import TextLabel
from wiki_music.classifier.classifiers.config import *

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def gpt_classifier(
        summaries: list[str],
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        user_prompt: str = DEFAULT_USER_PROMPT
) -> list[TextLabel]:
    """This is our main classification function with customizable prompts
    
    Args:
        summaries: the list of one-sentence wikipedia summaries
        system_prompt: the system prompt for the eventual call (str)
        user_prompt: the user prompt for the eventual api call (str)
        
    Returns:
        list[TextLabel]: the summaries with their corresponding classifications"""
    
    num_summaries = len(summaries)
    i = 0
    boolean_responses: list[bool] = []
    while i < num_summaries:
        upper_bound = min(i+BATCH_SIZE, num_summaries)
        responses = gpt_wrapper(summaries[i:upper_bound], system_prompt, user_prompt)
        boolean_responses.extend(responses)
        i += BATCH_SIZE

    return [
        {"summary": summaries[i], "is_music": boolean_responses[i]}
        for i in range(num_summaries)
    ]

def gpt_wrapper(
        summaries: list[str],
        system_prompt: str,
        user_prompt: str
) -> list[bool]:
    """This function actually calls the OpenAI API, and gets a structured 
    response back
    
    Args:
        Summaries: the list of one-sentence wikipedia summaries
        
    Returns:
        list[bool]: the bare classifications in order"""
    assert len(summaries) <= BATCH_SIZE
    if len(summaries) == 0:
        return []

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{user_prompt}\n\nSummaries:\n" + "\n".join(summaries)}
    ]

    tools = TOOLS_SCHEMA

    try:
        result = client.chat.completions.create(
            model=MODEL,
            messages = messages,
            tools = tools,
            tool_choice={"type": "function", "function": {"name": "classify_summaries"}}
        )
    except Exception as e:
        raise

    json_response = result.choices[0].message.tool_calls[0].function.arguments
    json_response_parsed = json.loads(json_response)
    return json_response_parsed['classifications']


    
