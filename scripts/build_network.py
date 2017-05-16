from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import pickle


# Load the data set
X, Y, X_test, Y_test = pickle.load(open("full_dataset.pkl", "rb"))

# Shuffle the data
X, Y = shuffle(X, Y)

img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()


# Create extra synthetic training data by flipping, rotating and blurring the
# images on our data set.
# img_aug = ImageAugmentation()
# img_aug.add_random_flip_leftright()
# img_aug.add_random_rotation(max_angle=25.)
# img_aug.add_random_blur(sigma_max=3.)
# will create error in this specific scenario



# define the network structure
# input is a 32x32 image rgb?

network = input_data(shape=[None, 32, 32, 3],
					 data_preprocessing=img_prep)
# 1. convolution
network = conv_2d(network, 32, 3, activation='relu')

# 2. max pooling
network = max_pool_2d(network, 2)

# 3. convolution again
network = conv_2d(network, 64, 3, activation='relu')

# 4. convolution again
network = conv_2d(network, 64, 3, activation='relu')

# 5. max pooling again
network = max_pool_2d(network, 2)

# 6. fully-connected 512 node neural network
network = fully_connected(network, 512, activation='relu')

# 7. dropout: prevent overfitting, is it really necessary? since we want to overfit? kinda?
network = dropout(network, 0.5)

# 8. fully-connected nn with 6 outputs
network = regression(network, optimizer='adam',loss='categorical_crossentropy', learning_rate=0.001)

# wrap the network in a model object
model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='bird-classifier.tfl.ckpt')

# training, 100 passes
model.fit(X, Y, n_epoch=100, shuffle=True, validation_set=(X_test, Y_test),
		  show_metric=True, batch_size=96, snapshot_epoch=True, run_id='bird-classifier')

# save model when training is complete
model.save('bird-classifier.tfl')
print('Network trained and saved.')