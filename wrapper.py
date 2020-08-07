'''
A wrapper program designed to interface with the RPLidar library to control the RPLidar A1M8 scanner.
Created for CMPE Project Lab, ECE 3334, Summer 2020.

Created by: Justin Schwausch
justinschwausch980@gmail.com

Used in the following Repo: https://github.com/justin-schwausch/ECE3334-Remote-LiDAR-Scanner
This file and the rest of the repo are released under the GNU General Public License v3.0 license.
The code is provided as-is, with no guarantees to functionality or warranties. Users take full responsibility for any
and all damages incurred by using this program or any of this repository.
'''
from rplidar import RPLidar  # import RPLidar framework
import time  # time for scan benchmarking


class Wrapper(object):  # wrapper object

    def __init__(self, port):  # set up LiDAR connection
        self.lidar = RPLidar(port)
        self.lidar.stop_motor()  # stop motor

    def start(self):  # start motor
        self.lidar.start_motor()

    def stop(self):  # stops motor
        self.lidar.stop_motor()

    def output(self, amount):  # samples for number of seconds
        i = 0
        measurements = []  # stores readings
        secs = amount  # 2000 samples per second
        begin = time.time()  # grab unix start time
        for measurement in self.lidar.iter_measurments():  # iterate through measurements
            measurements.append(measurement)  # add to measurement array
            i = i + 1

            if i == secs:  # break if done sampling
                end = time.time()  # grab unix end times
                break

        print('Begin: ', begin)  # print start times, end times, and time elapsed
        print('End: ', end)
        print('Elapsed: ', end - begin)
        self.lidar.stop_motor()  # stop motor
        self.lidar.stop()  # stop scanning
        return measurements
