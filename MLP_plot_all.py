import os
from keras.models import model_from_json, Sequential
from keras.layers import Activation, Dense, Dropout
from keras.engine import Input, Model
import keras.utils
from keras.utils.vis_utils import plot_model
import numpy as np
import datetime
import random
from reader import Reader
import matplotlib.pyplot as plt


results_directory = './MLPresults/'
models_directory = './MLPmodels/'


def get_model(num_hid_layers, cells_per_layer, dropout_rate):
	length = Reader.getInputShape()
	model = Sequential()
	model.add(Dense(cells_per_layer, input_shape=(length,), activation='relu'))
	model.add(Dropout(dropout_rate))

	for i in range(num_hid_layers):
		model.add(Dense(cells_per_layer, activation='relu'))
		model.add(Dropout(dropout_rate))

	model.add(Dense(1, activation='sigmoid'))#softmax se multiclass, sigmoid se 2class

	model_name = models_directory + 'MLP.hidlay' + str(num_hid_layers) + '.cells' + str(cells_per_layer) + '.drop' + str(dropout_rate)
	plot_model(model, to_file = model_name + '.2class' +  '.png', show_shapes=True)

	fp_model = open(model_name + '.2class' + '.json', 'w+')
	fp_model.write(model.to_json())
	fp_model.close()
	return model


def fit_and_eval(loss_function, optimizer, dropout_rate, dataset_name):
	results_file = 	results_directory + dataset_name + '.' + loss_function + '.' + optimizer + '.Dropout' + str(dropout_rate)
	
	write_results(results_file, 'HiddenLayers|CellsPerLayer|Accuracy')
	
	# READ THE INPUT
	#fp_logfile = open('./working/logfile', 'a')
	#reader = Reader(fp_logfile, False)
	(x_train, y_train), (x_test, y_test) = Reader.getDataset(1)

	#(x_train, y_train), (x_test, y_test) = Reader.getDataset(5)
	#x_train = x_train[0:1000,:]
	#y_train = y_train[0:1000]
	#x_test = x_test[0:1000,:]
	#y_test = y_test[0:1000]
	
	num_classes = 2
	nb_epoch = 20

	lns = []
	for num_hid_layers in [0,1,2,3,4]:
		results = []
		for cells_per_layer in [20,30,40,50,60]:
			model = get_model(num_hid_layers, cells_per_layer, dropout_rate)
			model.compile(optimizer=optimizer, loss=loss_function, metrics=['accuracy'])
			#model.fit(x_train, keras.utils.np_utils.to_categorical(y_train, num_classes), epochs = nb_epoch, batch_size = 128, shuffle=True)
			model.fit(x_train, y_train, epochs = nb_epoch, batch_size = 128, shuffle=True)

			#ev = model.evaluate(x = x_test, y = keras.utils.np_utils.to_categorical(y_test, num_classes), batch_size = 128)
			ev = model.evaluate(x = x_test, y = y_test, batch_size = 128)

			results.append(ev[1])
			#results.append(0.1*num_hid_layers + 0.001*cells_per_layer)		
			write_results(results_file, str(num_hid_layers) + '|' + str(cells_per_layer) + '|' + str(ev[1]))
		myplot = plt.subplot()
		myplot.grid(True)
		myplot.set_xlabel("Cells per Layer")
		myplot.set_ylabel("Accuracy")
		#myplot.set_xticklabels([20,30,40,50,60], rotation=45)
		line = myplot.plot([20,30,40,50,60], results, label='hidLayers:'+str(num_hid_layers))		
		lns = lns + line
	
	
	loss_short = loss_function
	if loss_short == 'categorical_crossentropy' or loss_short == 'binary_crossentropy':
		loss_short = 'crossentropy'
	plt.title(dataset_name + ',MLP, Loss: ' + loss_short + ', Opt: ' + optimizer + ', Batch: 128, Dropout: ' + str(dropout_rate))
	box = myplot.get_position()
	myplot.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])	
	labs = [l.get_label() for l in lns]
	lgd = plt.legend(lns, labs,loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=3) #
	plt.savefig(results_directory + 'MLP ' + dataset_name + ' Loss:' + loss_short + ' Opt:' + optimizer + ' Batch:128 Dropout:' + str(dropout_rate) + '.png')
	plt.clf()


def write_results(results_file, text):
	fp_results = open(results_file, 'a')
	fp_results.write(text +'\n')	
	fp_results.close()




#fit_and_eval('mse', 'sgd', 0) 					DONE in Z   CORRECT
#fit_and_eval('mse', 'sgd', 0.2) 				DONE in Z   CORRECT
#fit_and_eval('mse', 'sgd', 0.4)				DONE in Z CORRECT
#fit_and_eval('mse', 'sgd', 0.6, 'Dataset0')			DONE in Z CORRECT
#fit_and_eval('mse', 'sgd', 0.5, 'Dataset0')			DONE in Z CORRECT
#fit_and_eval('mse', 'sgd', 0.8,'Dataset0')			DONE in Z CORRECT

#fit_and_eval('mae', 'sgd', 0)
#fit_and_eval('mae', 'sgd', 0.2)
#fit_and_eval('mae', 'sgd', 0.4)
#fit_and_eval('mae', 'sgd', 0.6)

#fit_and_eval('categorical_crossentropy', 'adagrad', 0, 'Dataset0')	#DONE Z CORRECT
#fit_and_eval('categorical_crossentropy', 'adagrad', 0.2, 'Dataset0')	#DONE Z CORRECT
#fit_and_eval('categorical_crossentropy', 'adagrad', 0.4, 'Dataset0')	#Trying again on the VM, aaand CORRECT in Z!!
#fit_and_eval('categorical_crossentropy', 'adagrad', 0.6,'Dataset0')	#DONE Z CORRECT

#fit_and_eval('categorical_crossentropy', 'sgd', 0, 'Dataset0') 	#DONE Z CORRECT
#fit_and_eval('categorical_crossentropy', 'sgd', 0.2, 'Dataset0')	#DONE Z CORRECT
#fit_and_eval('categorical_crossentropy', 'sgd', 0.4, 'Dataset0')	#DONE Z CORRECT
#fit_and_eval('categorical_crossentropy', 'sgd', 0.6, 'Dataset0')	#DONE Z CORRECT

#fit_and_eval('categorical_crossentropy', 'rmsprop', 0, 'Dataset0')	#Done Z CORRECT
#fit_and_eval('categorical_crossentropy', 'rmsprop', 0.2, 'Dataset0')	#Done Z CORRECT
#fit_and_eval('categorical_crossentropy', 'rmsprop', 0.4, 'Dataset0')	#Done in Z CORRECT
#fit_and_eval('categorical_crossentropy', 'rmsprop', 0.6, 'Dataset0')	#Done Z  CORRECT


# Dataset 5 with MLP
#fit_and_eval('mse', 'sgd', 0.4, 'Dataset5')							DONE in Z	CORRECT
#fit_and_eval('categorical_crossentropy', 'rmsprop', 0.4, 'Dataset5')	DONE in Z	with ERROR


# Dataset 1 ping attack
#fit_and_eval('mse', 'sgd', 0.2, 'Dataset1')
#fit_and_eval('mse', 'sgd', 0.4, 'Dataset1')
fit_and_eval('binary-crossentropy', 'rmsprop', 0.2, 'Dataset1')
fit_and_eval('binary-crossentropy', 'rmsprop', 0.4, 'Dataset1')
