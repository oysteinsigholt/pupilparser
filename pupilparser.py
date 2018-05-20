#!/usr/bin/python

import msgpack
import sys
import matplotlib.pyplot as plt

def main():
    blink_filter_length = 0.2
    blink_confindence_threshold = 0.5
    blink_resolution = 20.0

    blinks = []
    blink_freq = []

    start_time = sys.maxint
    end_time = -sys.maxint
    last_blink_onset = -1

    if len(sys.argv) < 2:
        print "Usage: ./pupilparser.py <pupil_data file>"
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

    plt.plot(blink_freq)
    plt.ylabel('Blink Frequency')
    plt.show()

if __name__ == "__main__":
    main()
