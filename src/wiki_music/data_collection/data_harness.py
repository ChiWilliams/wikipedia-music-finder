# dataset harness
import sys
import json
import os
from getch import getch


def get_judgement(summary: str) -> bool:
    """This function gets the classification of an individual Wikipedia summary
    Input:
        summary: (str) a one sentence summary of the article
    Returns:
        a boolean classification
    Side effects:
        Prints to stdout
        Exits the program if 'q' is pressed"""
    print(summary)
    while True:
        print("Is this music (y/n)? (Press Q to quit)")
        classification = getch().decode().upper()
        if classification in ['Y', 'N', 'Q']:
            break
        print("Please enter Y, N, or Q")
    if classification == 'Q':
        sys.exit(0)
    else:
        print(classification)
        return classification == 'Y'
        

def save_to_jsonl(summary: str, is_music: bool, jsonl) -> None:
    """This is a small helper function which appends a json object to a filepath given a
    summary and a classification.
    
    Parameters:
        summary (str): the one-sentence wikipedia summary
        is_music (bool): the classification
        jsonl: the name of the .jsonl filepath
    Returns: None
    Side effects: Writes to jsonl file
    """
    data = {
        "summary" : summary,
        "is_music" : is_music
    }
    json.dump(data, jsonl)
    jsonl.write('\n')

def classify_music_data(*, summary_file = 'raw_data_small.txt', jsonl_file = 'dataset.jsonl') -> None:
    """
    This function oversees processing a raw dataset of strings into a classified dataset stored as jsonl

    Parameters:
        summary_file (str): the file path of the input strings
        jsonl_file (str): the filepath where the output will be stored
    """
    with open(summary_file, 'r', encoding="utf-8") as f:
        summaries = f.readlines()
        num_summaries = len(summaries)
        with open(jsonl_file, 'a', encoding="utf-8") as jsonl:
            num_processed = sum(1 for _ in open(jsonl_file)) if os.path.exists('dataset.jsonl') else 0

            summaries_to_process = summaries[num_processed:]

            for summary in summaries_to_process:
                print("-"*80)
                print(f"Progress: {num_processed}/{num_summaries} ({num_processed/num_summaries*100:.1f}%)")
                print()

                is_music = get_judgement(summary)
                save_to_jsonl(summary, is_music, jsonl)

                print()
                print()
                num_processed += 1
            
        print("Finished processing entries!")

if __name__=="__main__":
    classify_music_data(summary_file='raw_data.txt',jsonl_file='classifcations.jsonl')