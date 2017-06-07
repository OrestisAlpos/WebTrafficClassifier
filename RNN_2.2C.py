
from keras.models import Sequential
from keras.layers import Dense, Activation, SimpleRNN
from keras.utils.vis_utils import plot_model
import os
import numpy as np
from reader import Reader


length = Reader.getInputShape()

model = Sequential()

#EXPECTS INPUT AS (nb_sample, timesteps, nb_features), where nb_sample=1 (batch_size = 1), timesteps = 1 and nb_features = length

#model.add(Dense(40, input_dim = 12, init='uniform', activation='relu'))
model.add(SimpleRNN(units=50, input_shape=(1,length), batch_input_shape=(1,1,length), recurrent_initializer='random_uniform', kernel_initializer='random_uniform', activation='sigmoid', return_sequences=True, stateful=True))
model.add(SimpleRNN(units=50, recurrent_initializer='random_uniform', kernel_initializer='random_uniform', activation='sigmoid', stateful=True))
model.add(Dense(5, kernel_initializer='random_uniform', activation = 'softmax'))


model.summary()
plot_model(model, to_file='./RNNmodels/RNN_2.2C.png', show_shapes=True)
fp = open('./RNNmodels/RNN_2.2C.json', 'w')
fp.write(model.to_json())
fp.close()
