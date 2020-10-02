from typing import Iterator
import numpy as np
import csv
import matplotlib.pyplot as plt

def get_x_values():
    return range(1, 3935 + 1)

def get_y_values(path: str) -> Iterator[float]:
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            head, *_ = row
            yield float(head)

x_values = get_x_values()
time_levenshtein = list(get_y_values("time_levenshtein2.csv"))
time_jarowinkler = list(get_y_values("time_jarowinkler.csv"))
time_hamming = list(get_y_values("time_hamming.csv"))

fig = plt.figure()
ax = plt.subplot(111)
ax.plot(x_values, time_levenshtein, label='Levenshtein')
ax.plot(x_values, time_jarowinkler, label='Jaro-Winkler')
ax.plot(x_values, time_hamming, label='Hamming')

plt.title("Temps de correction selon le nombre de fautes")
plt.xlabel("Nombre de mots")
plt.ylabel("Temps(s)")
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=3)

# plot all on one
plt.show()