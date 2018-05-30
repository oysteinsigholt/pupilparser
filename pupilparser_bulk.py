#!/usr/bin/python

import msgpack
import sys
import os
import math
import csv
import json
import matplotlib.pyplot as plt

ratings = {}
summaries = {}

def parse_pupil_data(file):
    with open(os.path.join(sys.argv[1], file, "summary.json")) as f:
        summaries[file] = json.load(f)

def main():
    if len(sys.argv) < 3:
        print "Usage: ./pupilparser.py <input folder> <output folder>"
        exit()

    with open('circle_data/ratings.json') as f:
        ratings = json.load(f)

    for file in os.listdir(sys.argv[1]):
        parse_pupil_data(file)

    i = 0
    for key in summaries[summaries.keys()[0]].keys():
        dimensionId = 0
        for dimension in ratings[ratings.keys()[0]]:
            feature = []
            rating = []
            for trial in summaries.keys():
                rating.append(ratings[trial][dimensionId]["mean"])
                feature.append(summaries[trial][key])

            plt.figure(i)
            plt.scatter(feature, rating)
            plt.xlabel(key)
            plt.ylabel(dimension["name"])
            plt.savefig(os.path.join(sys.argv[2], key + '_' + dimension["name"] + '.png'))

            i+=1
            dimensionId +=1

if __name__ == "__main__":
    main()
