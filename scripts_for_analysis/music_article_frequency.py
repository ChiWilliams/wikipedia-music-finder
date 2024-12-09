# Here we write a script to analyze some of the data

# What do we care about? -- we care about 
# proportion classified as music
# and distribution of length

import json
import numpy as np
import matplotlib.pyplot as plt

with open("classifications.jsonl", 'r') as jsonl:
    data = [json.loads(line) for line in jsonl]

is_music = np.array([bool(x['is_music']) for x in data])

# percent_music = sum(1 for x in data if x['is_music']) / len(data)
percent_music = is_music.mean()
print(percent_music) # 7.4% of the sample is music

# now we calculate the distribution of gaps:
music_indices = np.where(is_music)[0]
gaps = np.diff(music_indices)
print(music_indices)
print(gaps)
print(gaps.mean())


# and now we graph!
x = np.arange(1, max(gaps) + 1)
plt.plot(x, 0.058 * (0.942)**(x-1), 'r--', label = 'p=0.058', linewidth = 2)
plt.plot(x, 0.090 * (0.910)**(x-1), 'g--', label = 'p=0.090', linewidth = 2)
plt.legend()
plt.hist(gaps, bins=range(0, max(gaps) + 2, 5), density= 'true', alpha = 0.7)
plt.xlabel('Gap Size')
plt.ylabel('Probability')
plt.title('Probability of gap size appearing (and observed)')
plt.show()




