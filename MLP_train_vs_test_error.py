import os
from keras import optimizers
from keras.models import model_from_json, Sequential, load_model
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
	model.add(Dense(5, activation='softmax'))#softmax se multiclass, sigmoid se 2class
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
	model_name = str(num_hid_layers) + '.' + str(cells_per_layer) + '.' + str(dropout_rate)
	num_classes = 5
	nb_epoch = 100
	optimizer = 'rmsprop'
	optimizer_w_params = optimizers.RMSprop(lr=0.0001)
	loss_function = 'categorical_crossentropy'
	results_file = 	results_directory + dataset_name + '.' + loss_function + '.' + optimizer + '.Dropout' + str(dropout_rate) + 'Layers' + str(num_hid_layers) + '.Cells' + str(cells_per_layer)
	write_results(results_file, 'loss|acc|val_loss|val_acc')
	model = get_model(num_hid_layers, cells_per_layer, dropout_rate)
	model.compile(optimizer=optimizer, loss=loss_function, metrics=['accuracy'])
	hist = model.fit(x_train, keras.utils.np_utils.to_categorical(y_train, num_classes), validation_data =(x_test,keras.utils.np_utils.to_categorical(y_test)), epochs = nb_epoch, batch_size = 128, shuffle=True)
	#hist = model.fit(x_train, y_train, validation_data=(x_test,y_test), epochs = nb_epoch, batch_size = 128, shuffle=True)
	write_results(results_file,hist.history['loss'])
	write_results(results_file,hist.history['acc'])
	write_results(results_file,hist.history['val_loss'])
	write_results(results_file,hist.history['val_acc'])
	model.save(models_directory + '/full_models/' + dataset_name + '.' + model_name + '.h5')

def write_results(results_file, text):
	fp_results = open(results_file, 'a')
	fp_results.write(str(text))
	fp_results.write('\n')
	fp_results.close()

fit_and_eval(0,2,30,0.4)

