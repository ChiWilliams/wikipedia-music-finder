import wiki_music.data_collection.get_ulrs as get_ulrs

def make_1000_summaries(filename = "descriptions.txt", num_descriptions = 1000):
    """This function runs get_wikipedia_sentence summaries and saves the output to a file"""
    with open(filename, "a", encoding="utf-8") as f:
        summaries_list = get_ulrs.get_wikipedia_sentence_summaries(num_descriptions)
        f.writelines(summary + "\n" for summary in summaries_list)

if __name__ == "__main__":
    make_1000_summaries(num_descriptions=1000)