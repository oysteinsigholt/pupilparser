#!/usr/bin/python

import msgpack
import sys
import os
import math
import csv
import matplotlib.pyplot as plt

def main():
    blink_filter_length = 0.2
    blink_confindence_threshold = 0.5
    blink_resolution = 20.0
    fixation_resolution = .1

    blinks = []
    blink_freq = []

    pupil_diameter_x = [] # time
    pupil_diameter_y = [] # diameter

    pupil_error_x = [] # time
    pupil_error_y = []

    start_time = sys.maxint
    end_time = -sys.maxint
    last_blink_onset = -1

    if len(sys.argv) < 3:
        print "Usage: ./pupilparser.py <pupil_data file> <output folder>"
        exit()

    try:
        pupil_data_file = open(sys.argv[1], 'rb')
        pupil_data = pupil_data_file.read()
    except:
        print "Could not open pupil_data file"
        exit()
    finally:
        pupil_data_file.close()

    pupil_data_object = msgpack.unpackb(pupil_data, use_list=False, raw=False)

    # Get start and end timestamps
    for pupil_position in pupil_data_object["pupil_positions"]:
        if pupil_position["timestamp"] < start_time:
            start_time = pupil_position["timestamp"]
        if pupil_position["timestamp"] > end_time:
            end_time = pupil_position["timestamp"]

    print "Recording is " + str(end_time-start_time) + " seconds long"

   # Get blink times
    for blink in pupil_data_object["blinks"]:
        if blink["confidence"] > blink_confindence_threshold:
            if blink["type"] == "onset":
                last_blink_onset = blink["timestamp"]
            elif blink["timestamp"] - last_blink_onset < blink_filter_length:
                blinks.append(last_blink_onset)

    print str(len(blinks)) + " blinks"

    # Get blink freq
    for i in range(int(blink_resolution), int(end_time-start_time)):
        blink_count = 0

        for blink in blinks:
            if blink > (i - blink_resolution) + start_time and blink < i + start_time:
                blink_count += 1

        blink_freq.append(blink_count/blink_resolution)

    # -------
    # Pupil Diameter
    last_diameter = -1
    last_timestamp = -1

    for pupil_position in pupil_data_object["pupil_positions"]:
        pupil_error_x.append(pupil_position["timestamp"] - start_time)
        pupil_error_y.append(pupil_position["confidence"])
        if pupil_position["confidence"] > 0.6:
            if last_timestamp == -1 or last_diameter == -1 or abs(last_diameter - pupil_position["diameter_3d"])/abs(pupil_position["timestamp"]-last_timestamp) < 1:
                pupil_diameter_x.append(pupil_position["timestamp"] - start_time)
                pupil_diameter_y.append(pupil_position["diameter_3d"])
                last_timestamp = pupil_position["timestamp"]
                last_diameter = pupil_position["diameter_3d"]

    # -----
    # Duration

    fixations = [0] * int(((1.0/fixation_resolution) * (end_time - start_time)))
    for fixation in pupil_data_object["fixations"]:
        fixation_start = int((fixation["timestamp"] - start_time) * 1./fixation_resolution)
        fixation_end = fixation_start + int(fixation["duration"] / 1000. * 1./fixation_resolution)
        for i in range(fixation_start, fixation_end):
            if i < len(fixations):
                fixations[i] = 1

    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])

    blinkPlt = plt.figure(0)

    plt.plot(blink_freq)
    plt.ylabel('Blink Frequency')
    plt.xlabel('time [s]')
    plt.savefig(os.path.join(sys.argv[2], 'blink.png'))
    #blinkPlt.show()

    diameterPlt = plt.figure(1)
    plt.plot(pupil_diameter_x, pupil_diameter_y)
    plt.ylabel("diameter [mm]")
    plt.xlabel("time [s]")
    plt.savefig(os.path.join(sys.argv[2], 'diameter.png'))


    error = plt.figure(2)
    plt.plot(pupil_error_x, pupil_error_y)
    plt.ylabel("confidence")
    plt.xlabel("time [s]")
    plt.savefig(os.path.join(sys.argv[2], 'error.png'))


    with open(os.path.join(sys.argv[2], 'diameter.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(pupil_diameter_x)
        writer.writerow(pupil_diameter_y)

    with open(os.path.join(sys.argv[2], 'blink.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(blink_freq)


    with open(os.path.join(sys.argv[2], 'confidence.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(pupil_error_x)
        writer.writerow(pupil_error_y)

    #fixationPlt = plt.figure(2)
    #plt.plot(fixations)
    #plt.bar(range(len(fixations)), fixations, 1)
    #plt.ylabel("fixating [bool]")
    #plt.xlabel("time [s*10]")
    #plt.show()

if __name__ == "__main__":
    main()
