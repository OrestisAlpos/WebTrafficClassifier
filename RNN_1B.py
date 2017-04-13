
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
model.add(SimpleRNN(units=50, input_shape=(1,length), batch_input_shape=(1,1,length), recurrent_initializer='uniform', kernel_initializer='uniform', activation='relu', stateful=True))
model.add(Dense(3, kernel_initializer='uniform', activation = 'softmax'))


model.summary()
plot_model(model, to_file='/home/orestis/net/RNNmodels/RNN_1B.png', show_shapes=True)
fp = open('/home/orestis/net/RNNmodels/RNN_1B.json', 'w')
fp.write(model.to_json())
fp.close()

