import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Activation
import re
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    # loop through series
    for num in range(0,len(series)-window_size, 1):
        # add inputs from the series for each window size
        X.append(series[num:num+window_size])
        # add output from series from after the window size
        y.append(series[num + window_size])

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):

    #initiate the model
    model = Sequential()
    #add LSTM with 5 hidden layer units
    model.add(LSTM(5, input_shape=(window_size, 1)))
    #add FC layer
    model.add(Dense(1))

    return model




### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    # punctuation = ['!', ',', '.', ':', ';', '?']

    unique_chars = list(set(text))

    print('unique characters: ', unique_chars)

    # # Remove non-english characters
    text = re.sub(r'[^\x00-\x7F]+',' ', text)

    # Remove digits
    text = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", text)

    # # shorten any extra dead space created above
    # text = text.replace('  ',' ')

    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    # loop through series
    for num in range(0,len(text)-window_size, step_size):
        # add inputs from the series for each window size
        inputs.append(text[num:num+window_size])
        # add output from series from after the window size
        outputs.append(text[num + window_size])


    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):

    #initiate the model
    model = Sequential()
    # added a LSTM model with 200 hidden layers, with an input shape
    # the size of a window and length for the num_charts
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    # added FC layer
    model.add(Dense(num_chars))
    # add softmax activation
    model.add(Activation('softmax'))

    return model








