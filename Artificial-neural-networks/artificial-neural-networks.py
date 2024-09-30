import tensorflow
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.datasets import mnist
from keras import utils
import numpy as np
import cv2

# extra validation function - external inspo
def valid_imshow_data(data):
    data = np.asarray(data)
    if data.ndim == 2:
        return True
    elif data.ndim == 3:
        if 3 <= data.shape[2] <= 4:
            return True
        else:
            print('The "data" has 3 dimensions but the last dimension '
                  'must have a length of 3 (RGB) or 4 (RGBA), not "{}".'
                  ''.format(data.shape[2]))
            return False
    else:
        print('To visualize an image the data must be 2 dimensional or '
              '3 dimensional, not "{}".'
              ''.format(data.ndim))
        return False



# Loading the dataset

(X_train, y_train), (X_test, y_test) = mnist.load_data()

# plt.imshow(X_train[0], cmap='gray')
# plt.title('Class: ' + str(y_train[0]))
# plt.waitforbuttonpress()

X_train = X_train.reshape(60000, 28*28)
X_train.shape

X_test = X_test.reshape(10000, 28*28)
X_test.shape

# Pre-processing the images

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train = X_train / 255     #   normalize to 0-1 range
X_test = X_test / 255       #   normalize to 0-1 range

#   Sigmoid - 0 to 1 (2 classes)
#   Softmax - 0 to 1 (3 classes)


y_train = utils.to_categorical(y_train)
y_test = utils.to_categorical(y_test)

print(X_train.max())        #   validate normilization
print(X_train.min())

print(y_train[0])           #   test-print random lines of y_train

# Building and training the neural network

# 784 -> 397 -> 397 -> 10  : layer definition
# 784 initial values : from 28x28 pixels table -> 397 nodes -> 397 nodes -> 10 expected output values : numbers from 0 to 9)
# (784 + 10) / 2 = 397 -> hidden layer size

network = Sequential()
network.add(Dense(input_shape = (784,), units = 397, activation = 'relu'))
network.add(Dense(units = 397, activation = 'relu'))
network.add(Dense(units = 10, activation = 'softmax'))

network.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

history = network.fit(X_train, y_train, batch_size = 128, epochs = 2)

# Evaluating the neural network

#   history.history.keys() -> loss, accuracy

#   we can notice that after a certain point of epochs the loss ( and the accuracy ) remain more or less stable
#   we can use this amount of epochs for our future scenarios, not to overkill the system with pointless repetitions

# plt.plot(history.history['loss'])

# plt.plot(history.history['accuracy']);
# plt.show()
# plt.waitforbuttonpress()

network.evaluate(X_test, y_test)

#   so after the evaluation we predict the rest of the X_test
predictions = network.predict(X_test)

#   and we can test for our selves using any random prediction - for example the 2nd prediction
# print(predictions.shape)
#   we expect to find a list of evaluations in an array from 0-9. only one value should be equal to 1.

test_index = 4
print(predictions[test_index])

print('Predicted value : ' + str(np.argmax(predictions[test_index])))
#   and then we can view the X_test image as well , in order to double-check on our own
plt.imshow(X_test[test_index].reshape(28,28), cmap='gray')
plt.title('Class: ' + str(X_test[test_index]))
plt.waitforbuttonpress()

#   Now we can test our own scenario with an image that we will upload

test_image = cv2.imread('./digit.png')

test_image = cv2.resize(test_image, (28,28))  # reshape image to our trained model - nodes
test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)    # color in grayscale
cv2_imshow(test_image)

test_image = test_image.reshape(1, 28*28)
test_image = test_image / 255 # normalize to 0-1 values
# print(test_image.shape)

prediction = network.predict(test_image)
print(prediction)
print('Custom Predicted value : ' + str(np.argmax(prediction)))

print('EOF')