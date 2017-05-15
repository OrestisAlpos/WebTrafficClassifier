import os
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


(x_train, y_train), (x_test, y_test) = Reader.getDataset(100)


#MLP
model = keras.models.load_model('./MLPmodels/full_models/Dataset0/dataset0.2.30.0.4.h5')
ev = model.evaluate(x = x_test, y = keras.utils.np_utils.to_categorical(y_test, 5), batch_size = 128)
accMLP = str(ev[1])

x_train = x_train.reshape(x_train.shape[0], 1, -1)
x_test = x_test.reshape(x_test.shape[0], 1, -1)
#RNN
model = keras.models.load_model('./RNNmodels/full_models/Dataset0.RNN2.mse-sgd.99/Dataset0.RNN_2C.h5')
ev = model.evaluate(x = x_test, y = keras.utils.np_utils.to_categorical(y_test, 5), batch_size = 1)
accRNN = str(ev[1])
#LSTM
model = keras.models.load_model('./LSTMmodels/full_models/Dataset0.LSTM_2C/Dataset0.LSTM_2C.epoch6.h5')
ev = model.evaluate(x = x_test, y = keras.utils.np_utils.to_categorical(y_test, 5), batch_size = 1)
accLSTM = str(ev[1])

st = '\nAccuracies: MLP: ' + accMLP + ' RNN: ' + accRNN + ' LSTM: ' + accLSTM + '\n'
print(st)
fp = open('./final_test/results', 'a')
fp.write(st)
fp.close()

