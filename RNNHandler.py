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

def MyMetrics(y_true, y_pred):
	y_pred[y_pred<0.5] = 0.0
	y_pred[y_pred>=0.5] = 1.0
	y_true[y_true<0.5] = 0.0
	y_true[y_true>=0.5] = 1.0

	if np.count_nonzero(y_pred == 1.0) == y_pred.shape[0]:
		y_pred[0]=0.0
	if np.count_nonzero(y_pred == 0.0) == y_pred.shape[0]:
		y_pred[0]= 1.0
	if np.count_nonzero(y_true == 1.0) == y_true.shape[0]:
		y_true[0]=0.0
	if np.count_nonzero(y_true == 0.0) == y_true.shape[0]:
		y_true[0]= 1.0
	confusion = metrics.confusion_matrix(y_true, y_pred)
	TP = confusion[1, 1]
	TN = confusion[0, 0]
	FP = confusion[0, 1]
	FN = confusion[1, 0]
	precision = TP / (TP + FP)
	recall = TP / (TP + FN)
	fscore = 2 * precision * recall / ( precision + recall)
	return (precision, recall, fscore)


class RNNHandler:
	
	results_directory = './RNNresults'
	models_directory = './RNNmodels'

	def __init__(self, model_name, num_categories, loss, optimizer, optimizer_name):
		# GET THE MODEL
		fp_model = open(os.path.join(self.models_directory, model_name + '.json'), 'r')
		model_str = fp_model.read()
		self.model = model_from_json(model_str)
		self.model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])		
		fp_model.close()

		self.model_name = model_name
		self.num_categories = num_categories
		self.loss = loss
		self.optimizer = optimizer
		self.optimizer_name = optimizer_name
		
		
	def fit_and_eval(self, x_train, y_train, x_test, y_test, nb_epoch, dataset_name):	#batch_size is always 1 and shuffle is always False, so we don't pass them as parameters
		self.results_file = os.path.join(self.results_directory, dataset_name + '.' + self.model_name)
		self.write_result(self.model_name + ' ' + dataset_name + ' Loss:' + self.loss + ' Optimizer:' + self.optimizer_name + ' Dropout:No')
		self.write_result('Epoch|Loss|Accuracy|Precision|Recall|Fscore')		
		res_loss = []
		res_accuracy = []
		res_precision = []		
		res_recall = []
		res_fscore = []
		x_train = x_train.reshape(x_train.shape[0], 1, -1)
		x_test = x_test.reshape(x_test.shape[0], 1, -1)
		if self.num_categories > 2:
			y_train = to_categorical(y_train, self.num_categories)
			y_test = to_categorical(y_test, self.num_categories)
		for i in range(1, nb_epoch+1):			
			self.model.fit(x_train, y_train, batch_size=1, epochs=1, shuffle=False)
			self.model.reset_states()
			(loss, accuracy) = self.model.evaluate(x_test, y_test, batch_size=1)
			self.model.reset_states()
			res_loss.append(loss)
			res_accuracy.append(accuracy)
			(precision, recall, fscore) = (0,0,0)
			if self.num_categories == 2:			
				y_pred = self.model.predict(x_test, batch_size=1)
				self.model.reset_states()
				(precision, recall, fscore) = MyMetrics(y_test, y_pred)
				res_precision.append(precision)
				res_recall.append(recall)
				res_fscore.append(fscore)
			self.write_result(str(i) +'|'+ str(loss) +'|'+ str(accuracy) +'|'+ str(precision) +'|'+ str(recall) +'|'+ str(fscore))

		self.model.save(self.models_directory + '/full_models/' + dataset_name + '.' + self.model_name + '.h5')
		return (res_loss, res_accuracy, res_precision, res_recall, res_fscore)
	

	def write_result(self, text):
		fp = open(self.results_file, 'a')
		fp.write(text + '\n')
		fp.close()

#	def save_weights():



	@staticmethod
	def plot_results(title, metric, results):
		lns = []
		for k in results.keys():
			result = results[k]
			myplot = plt.subplot()
			myplot.grid(True)
			myplot.set_xlabel("Epoch Number")
			myplot.set_ylabel(metric)
			x_Axis = np.arange(1, len(result)+1)
			#myplot.xaxis.set_ticks(x_Axis)#np.arange(	1, len(x_Axis)+1, 1))
			#myplot.set_xticklabels(x_Axis, rotation=0)
			tokens = k.split('|')
			loss = tokens[0]
			if loss=='categorical_crossentropy' or loss=='binary_crossentropy':
				loss = 'crossentropy'
			optimizer = tokens[1]
			line = myplot.plot(x_Axis, result, label = 'loss:' + loss + ' opt:' + optimizer)		
			lns = lns + line
		box = myplot.get_position()
		myplot.set_position([box.x0, box.y0 + box.height * 0.25, box.width, box.height * 0.75])
		labs = [l.get_label() for l in lns]
		plt.title(title)
		lgd = plt.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=2)
		plt.savefig('./RNNresults/' + title + '.png')
		plt.clf()
