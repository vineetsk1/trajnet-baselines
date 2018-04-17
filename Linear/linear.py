# Script for simple linear predictions

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import imageio
import os
import time
import numpy.polynomial.polynomial as poly

def extract_traj(data, ped_id):
    return data[data[:, 1] == ped_id, :]

def read_testfile(fname):
    data = np.genfromtxt(fname, delimiter=" ", dtype=None)
    ndata = []
    for i in range(len(data)):
        if data[i][2] == '?':
            ndata.append([data[i][0], data[i][1], -1, -1])
        else:
            ndata.append([data[i][0], data[i][1], float(data[i][2]), float(data[i][3])])
    data = np.asarray(ndata)
    return data

def predict_traj(traj):

    # linear prediction, simple polyfit
    rng = range(8) # use first 8 frames: frames 0-7 (0 index)
    x = traj[:, 2][rng]
    y = traj[:, 3][rng]
    xcoefs = poly.polyfit(rng, x, 1) # fit line for x
    ycoefs = poly.polyfit(rng, y, 1) # fit line for y
    
    ntraj = np.copy(traj)
    for i in range(8, 20): # predict for frames 8-19 (0 index)
        ntraj[i,2] = xcoefs[0] + i*xcoefs[1]
        ntraj[i,3] = ycoefs[0] + i*ycoefs[1]
    return ntraj

def predict_file(data):
    ndata = []
    peds = set()
    for i in range(data.shape[0]):
        if data[i,1] not in peds:
            peds.add(data[i,1])
            traj = extract_traj(data, data[i,1])
            pred = predict_traj(traj)
            for j in range(pred.shape[0]):
                ndata.append(pred[j])
    ndata = np.asarray(ndata)
    return ndata

def save_file(data, fname):
    st = ""
    for i in range(data.shape[0]):
        if i != 0:
            st += "\n"
        st += "%f %f %f %f" % (data[i,0], data[i,1], data[i,2], data[i,3])
    with open(fname, "w") as fw:
        fw.write(st)

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_predictions(root, other):
    ensure_dir(root + other)
    for folder in os.listdir(root + "test"):
        if "." in folder:
            continue
        print "Processing folder", folder
        ensure_dir(root + other + "/" + folder)
        for fname in os.listdir(root + "test/" + folder):
            if not fname.endswith(".txt"):
                continue
            print "Processing file", fname
            test_data = read_testfile(root + "test/" + folder + "/" + fname)
            predict_data = predict_file(test_data)
            save_file(predict_data, root + other + "/" + folder + "/" + fname)

def main():
    create_predictions("../data/challenges/1/", "predict_linear")

if __name__ == '__main__':
    main()