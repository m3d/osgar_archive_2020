#!/usr/bin/python
"""
  Plot data
  usage:
       ./plot.py <text data>
"""
import argparse
import math
import matplotlib.pyplot as plt


def scatter(arr1, arr2):
    "mix two time based arrays based on first axis (time)"
    i, j = 0, 0
    arr = []
    while i < len(arr1) and j < len(arr2):
        if abs(arr1[i][0] - arr2[j][0]) < 0.001:
            arr.append( (arr1[i][1], arr2[j][1]) )
            i += 1
            j += 1
        elif arr1[i][0] < arr2[j][0]:
            i += 1
        else:
            j += 1
    return arr


def get_arr0(filename):
    arr = []
    enc_arr = []
    wheel_arr = []
    prev_wheel = 0
    for line in open(filename):
        if 'ENC' in line:
            prefix_cmd, t, x, y = line.split()
            enc_arr.append((float(t), (int(x), int(y))))
        if 'WHEEL' in line:
            prefix_cmd, t, angle, desired = line.split()
            if desired != 'None':
#                wheel_arr.append((float(t), (int(angle), float(desired))))
                wheel_arr.append((float(t), int(angle)))
                prev_wheel = float(desired)
            else:
#                wheel_arr.append((float(t), (int(angle), prev_wheel)))
                wheel_arr.append((float(t), int(angle)))
        if 'xSPEED' in line:
            prefix_cmd, t, raw, avr = line.split()
            arr.append((t, (raw, avr)))
        if 'xGAS' in line:
            prefix_cmd, gas, desired = line.split()
            arr.append((len(arr), (int(gas), int(desired))))
        if 'xSYNC' in line:
            gas = line.split()[-1]
            if gas != '0':
                arr.append((len(arr), float(gas)))

    for prev, curr in zip(enc_arr, enc_arr[6:]):
        L, R = curr[1][0]-prev[1][0], curr[1][1]-prev[1][1]
#        arr.append(( (prev[0]+curr[0])/2, (L, R)))
        if abs(L + R) > 20:
            arr.append(( (prev[0]+curr[0])/2, (R-L)/(L+R) ))
#    return scatter(arr, wheel_arr)
    return scatter(wheel_arr, arr)


def get_arr_driver_dist(filename):
    arr = []
    for line in open(filename):
        if 'DRIVER_DIST' in line:
            prefix_cmd, t, dist = line.split()
            arr.append((t, dist))
    return arr


def get_arr_laser_cones(filename):
    arr = []
    for line in open(filename):
        if 'LASER_CONE' in line:
            prefix_cmd, t, raw_angle, raw_dist, raw_width, color = line.split()
            arr.append((t, int(raw_angle)/2 - 135, color))
    return arr


def draw(arr, ylabel=None, marker='o'):
#    plt.plot(arr, 'o-', linewidth=2)
    x = [x for (x, _) in arr]
    y = [y for (_, y) in arr]
    plt.plot(x, y, marker, linewidth=2)
#    plt.xlabel('raw steering')
#    plt.ylabel('encoders normalized difference')
    plt.xlabel('time (sec)')
#    plt.ylabel('signed distance (meters)')
#    plt.ylabel('laser angle (deg)')
    if ylabel is not None:
        plt.ylabel(ylabel)

#    z = []
#    for i in xrange(len(y)):
#        z.append(sum(y[i-50:i+50])/100.0)
#    plt.plot(x, z, 'o-', linewidth=2)

    plt.show()



def draw3(arr):
    for color in ['FF0000', '00FF00', '0000FF', 'FFFFFF',
                  'FF8000', '808080']:
        x = [x for (x, _, c) in arr if c == color]
        y = [y for (_, y, c) in arr if c == color]
        if color == 'FFFFFF':
            color = '000000'
        plt.plot(x, y, 'o', linewidth=2, color='#'+color)
    plt.xlabel('time (sec)')
    plt.ylabel('laser angle (deg)')
    plt.show()


def draw_camera_cones(filename):
    # parse old camera logs like
    # (('logs/cam170808_170348_044.jpg', None), [(690, 410, 16, 39)])
    scale = 90.0/1024  # Field Of View / image resolution
    arr = []
    start_time = None
    for line in open(filename):
        if line.startswith('(('):
            a = eval(line)  # TODO weaker version
            for x, y, w, h in a[1]:
                arr.append((t, x * scale))
        else:
            s = line.split()
            if len(s) == 2:
                t = float(s[1])
                if start_time is None:
                    start_time = t
                t -= start_time
            else:
                break
    draw(arr, ylabel='camera angle (deg)')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse text output data')
    parser.add_argument('filename', help='input text filename')
    parser.add_argument('--select', choices=['laser-cones', 'camera-cones', 'driver-dist'],
                        default='laser-cones')
    args = parser.parse_args()

    if args.select == 'laser-cones':
        arr = get_arr_laser_cones(args.filename)
        draw3(arr)
    elif args.select == 'driver-dist':
        arr = get_arr_driver_dist(args.filename)
        draw(arr, ylabel='signed distance (meters)', marker='o-')
    elif args.select == 'camera-cones':
        draw_camera_cones(args.filename)


# vim: expandtab sw=4 ts=4 

