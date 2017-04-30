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


results_directory = './MLPresults/train_vs_test_error/'
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


def fit_and_eval(dataset_id, num_hid_layers, cells_per_layer, dropout_rate):
	#fp_logfile = open('./working/logfile', 'a')
	#reader = Reader(fp_logfile, False)
	dataset_name = 'dataset' + str(dataset_id)
	(x_train, y_train), (x_test, y_test) = Reader.getDataset(dataset_id)
	#x_train = x_train[0:100,:]
	#y_train = y_train[0:100]
	#x_test = x_test[0:100,:]
	#y_test = y_test[0:100]
	num_classes = 2
	nb_epoch = 500
	optimizer = 'sgd'
	loss_function = 'mse'
	results_file = 	results_directory + dataset_name + '.' + loss_function + '.' + optimizer + '.Dropout' + str(dropout_rate) + 'Layers' + str(num_hid_layers) + '.Cells' + str(cells_per_layer)
	write_results(results_file, 'loss|acc|val_loss|val_acc')
	model = get_model(num_hid_layers, cells_per_layer, dropout_rate)
	model.compile(optimizer=optimizer, loss=loss_function, metrics=['accuracy'])
	#model.fit(x_train, keras.utils.np_utils.to_categorical(y_train, num_classes), epochs = nb_epoch, batch_size = 128, shuffle=True)
	hist = model.fit(x_train, y_train, validation_data=(x_test,y_test), epochs = nb_epoch, batch_size = 128, shuffle=True)
	#ev = model.evaluate(x = x_test, y = keras.utils.np_utils.to_categorical(y_test, num_classes), batch_size = 128)
	#ev = model.evaluate(x = x_test, y = y_test, batch_size = 128)
	write_results(results_file,hist.history['loss'])
	write_results(results_file,hist.history['acc'])
	write_results(results_file,hist.history['val_loss'])
	write_results(results_file,hist.history['val_acc'])

def write_results(results_file, text):
	fp_results = open(results_file, 'a')
	fp_results.write(str(text))
	fp_results.write('\n')
	fp_results.close()

fit_and_eval(3,1,40,0.5)
fit_and_eval(3,4,40,0.5)

