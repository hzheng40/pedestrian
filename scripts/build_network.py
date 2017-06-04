from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization


# Load the data set
#TODO load images from training data



#TODO resize images after importing

# define the network structure
# input is a 227 x 227 rgb

network = input_data(shape=[None, 227, 227, 3])

# building alexnet
network = conv_2d(network, 96, 11, strides=4, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = local_response_normalization(network)
network = conv_2d(network, 256, 5, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = local_response_normalization(network)
network = conv_2d(network, 384, 3, activation='relu')
network = conv_2d(network, 384, 3, activation='relu')
network = conv_2d(network, 256, 3, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = local_response_normalization(network)
network = fully_connected(network, 4096, activation='tanh')
network = dropout(network, 0.5)
network = fully_connected(network, 4096, activation='tanh')
network = dropout(network, 0,5)
network = fully_connected(network, 17, activation='softmax')
network = regression(network, optimizer='momentum',
					loss='categorical_crossentropy',
					learning_rate=0.001)


# training the model
model = tflearn.DNN(network, checkpoint_path='model_alexnet',
					max_checkpoints=1, tensorboard_verbose=2)
model.fit(X, Y, n_epoch=1000, validation_set=0.1, shuffle=True,
				show_metric=True, batch_size=64, snapshot_step=200,
				snapshot_epoch=False, run_id='alexnet_pedestrian')


# saving the model
model.save('alexnet_pedestrian.tfl')
print('Network trained and saved')