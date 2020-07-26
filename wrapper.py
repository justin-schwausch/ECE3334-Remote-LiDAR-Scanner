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
