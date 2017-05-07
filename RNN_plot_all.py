import keras.utils
from keras.models import Sequential, model_from_json, load_model
from keras.layers import Dense, Activation, SimpleRNN
from keras.utils.vis_utils import plot_model
import keras.utils.np_utils
from keras.utils.np_utils import to_categorical

import os
import numpy as np
import datetime
import random
from reader import Reader
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn import metrics
import RNNHandler


#(1, 'Dataset1', 2, 'RNN_1A')
#(2, 'Dataset2', 2, 'RNN_1A')
#(3, 'Dataset3', 2, 'RNN_1A') !! grafiki
#(4, 'Dataset4', 2, 'RNN_1A') !!! mixed type binary and continous
#(5, 'Dataset5', 3, 'RNN_1B') +categorical
#(6, 'Dataset0', 5, 'RNN_1C') +categorical
dataset_id = 0
dataset_name = 'Dataset0'
num_classes = 5
#RNN_name = 'RNN_1A'

num_epochs = 20

(x_train, y_train), (x_test, y_test) = Reader.getDataset(dataset_id)
#x_train = x_train[0:1000,:]
#y_train = y_train[0:1000]
#x_test = x_test[0:1000,:]
#y_test = y_test[0:1000]

for RNN_name in ['RNN_2C']:
	results = {}
	for loss,optimizer in [('mse','sgd')]:#, ('categorical_crossentropy','rmsprop')]:	#categorical_crossentropy
	#for optimizer in ['sgd', 'rmsprop']:
		RNNmodel = RNNHandler.RNNHandler(RNN_name, num_classes, loss, optimizer)
		(res_loss, res_accuracy, res_precision, res_recall, res_fscore) = RNNmodel.fit_and_eval(x_train, y_train, x_test, y_test, num_epochs, dataset_name)
		if num_classes == 2:		
			results[loss + '|' + optimizer] = res_fscore
		else:
			results[loss + '|' + optimizer] = res_accuracy
	
	title = dataset_name + '.' + RNN_name
	metric = 'accuracy'
	if num_classes == 2:
		metric = 'fscore'
	RNNHandler.RNNHandler.plot_results(title, metric, results)



#(6, 'Dataset0', 5, 'RNN_1C') +categorical
#dataset_id = 6
#dataset_name = 'Dataset0'
#num_classes = 5
#RNN_name = 'RNN_1C'
#
#num_epochs = 10
##
#fp_logfile = open('./debug/logfile', "a")
#reader = Reader(fp_logfile, False)
#(x_train, y_train), (x_test, y_test) = reader.getDataNormalized()
#x_train = x_train[0:1000,:]
#y_train = y_train[0:1000]
#x_test = x_test[0:1000,:]
#y_test = y_test[0:1000]
#results = {}
#for loss in ['mse', 'categorical_crossentropy']: 
	#for optimizer in ['sgd','adagrad', 'rmsprop']:
#		RNNmodel = RNNHandler.RNNHandler(RNN_name, num_classes, loss, optimizer)
#		#(res_loss, res_accuracy, res_precision, res_recall, res_fscore) = RNNmodel.fit_and_eval(x_train, y_train, x_test, y_test, num_epochs, #dataset_name)			
		#if num_classes == 2:		
#			results[loss + '|' + optimizer] = res_fscore
		#else:
#			results[loss + '|' + optimizer] = res_accuracy
#
#title = dataset_name + '.' + RNN_name
#metric = 'accuracy'
#if num_classes == 2:
	#metric = 'fscore'
#RNNHandler.RNNHandler.plot_results(title, metric, results)
#
