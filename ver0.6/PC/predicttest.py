# -*- coding:utf-8 -*-
import os
import sys
import cv2
import numpy as np
from pybrain.tools.xml import NetworkReader


NPZ = 'data.npz'
XML = 'net.xml'
i = 0
detection = {}
true_labels = {}

#find XML file
if os.path.exists(XML) == False:
    print('XML file does not exist!')
    raw_input(">")
    sys.exit()

# load network
network = NetworkReader.readFrom(XML)

def detect(x):
     a = network.activate(image_array[x])
     return np.argmax(a)
    
# load training data
image_array = np.zeros((1, 9600))
label_array = np.zeros((1, 4), 'float')

with np.load(NPZ) as data:
    print data.files
    test_temp = data['train']
    test_labels_temp = data['train_labels']
    print test_temp.shape
    print test_labels_temp.shape
image_array = np.vstack((image_array, test_temp))
label_array = np.vstack((label_array, test_labels_temp))

test = image_array[1:, :]
test_labels = label_array[1:, :]


# test
while i < test_temp.shape[0]:
    detection[i] = detect(i)
    i += 1
prediction = np.array(detection.values())
print 'Prediction:\n', prediction


true_labels = test_labels.argmax(-1)
print 'True labels:\n', true_labels

print ('Testing...')
num_correct = np.sum( true_labels == prediction )
test_rate = np.mean(prediction == true_labels)
print ('Test rate: %f' % (test_rate*100))

raw_input(">")
