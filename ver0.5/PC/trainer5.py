# -*- coding: utf-8 -*-
import os
import sys
import time
import glob
import numpy as np
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.xml import NetworkWriter,NetworkReader
j = 0
NPZ = 'data.npz'
XML = 'net.xml'
image_array = np.zeros((1, 9600))
label_array = np.zeros((1, 4), 'float')

#find NPZ file
if os.path.exists(NPZ) == False:
    print('NPZ file does not exist!')
    raw_input(">")
    sys.exit()

if os.path.exists(XML) == True:
    # load neural network
    network = NetworkReader.readFrom(XML)
else:
    # build new neural network
    network = buildNetwork(9600, 32, 32, 4, bias = True)
    

training_data = glob.glob(NPZ)
target = SupervisedDataSet(9600, 4)
trainer = BackpropTrainer(network, target)


# load NPZ file
for single_npz in training_data:
    with np.load(single_npz) as data:
        print data.files
        train_temp = data['train']
        train_labels_temp = data['train_labels']
        print (train_temp.shape)
        print (train_labels_temp.shape)
    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, train_labels_temp))
t1 = time.time()
for i in range(train_temp.shape[0]):
    target.addSample(image_array[i],label_array[i])
print 'loading time : ' , time.time() - t1


# train
while True:
    try:
        while True:
            errors  = trainer.train()
            if (j % 5) == 0:
                print ("epoch%d error : %f" % (j, errors))
            elif(errors < 2e-2) :
                print ("epoch%d error : %f" % (j, errors))
                break
            j += 1
    finally:
        NetworkWriter.writeToFile(network, XML)
        break
raw_input('>')
