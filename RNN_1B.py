
from keras.models import Sequential
from keras.layers import Dense, Activation, SimpleRNN
from keras.utils.visualize_util import plot
import os
import numpy as np
from reader import Reader


length = Reader.getInputShape()

model = Sequential()

#EXPECTS INPUT AS (nb_sample, timesteps, nb_features), where nb_sample=1 (batch_size = 1), timesteps = 1 and nb_features = length

#model.add(Dense(40, input_dim = 12, init='uniform', activation='relu'))
model.add(SimpleRNN(output_dim=50, input_shape=(1,length), batch_input_shape=(1,1,length), init='uniform', inner_init='uniform', activation='relu', stateful=True))
model.add(Dense(3, init='uniform', activation = 'softmax'))


model.summary()
plot(model, to_file='/home/orestis/net/RNNmodels/RNN_1B.png')
fp = open('/home/orestis/net/RNNmodels/RNN_1B.json', 'w')
fp.write(model.to_json())
fp.close()

