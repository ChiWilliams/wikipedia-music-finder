import json
import random
import matplotlib.pyplot as plt
from wiki_music.utilities.data_processing import random_func

random_func()

with open("classifications.jsonl", "r") as jsonl:
    data = [json.loads(line) for line in jsonl]
    summary_lengths = [len(x["summary"]) for x in data]
    random.shuffle(data)

import heapq
def get_largest_n_lengths(data, n = 10):
    summary_lengths = [len(x["summary"]) for x in data]
    return heapq.nlargest(20, summary_lengths)

def percent_over_length_n(data, n = 400):
    summary_lengths = [len(x["summary"]) for x in data]
    return sum(x > n for x in summary_lengths)/len(summary_lengths)

def get_5_samples(data):
    i = 0
    music_examples, non_music_examples = [], []
    while len(music_examples) < 5 or len(non_music_examples) < 5:
        labelled_summary = data[i]
        if labelled_summary['is_music'] and len(music_examples) < 5:
            music_examples.append(labelled_summary["summary"])
        if not labelled_summary['is_music'] and len(non_music_examples) < 5:
            non_music_examples.append(labelled_summary["summary"])
        i += 1
    return music_examples, non_music_examples

# print(sum(summary_lengths)/len(summary_lengths))

# print(percent_over_length_n(data, 300))
# print(get_5_samples(data))


# plt.hist(sorted(len(x["summary"]) for x in data), bins=100)
# plt.show()


# print
    # num_music, num_not_music = 0, 0
    # while num_music < 5 and num_not_music < 5: