# -*- coding: utf-8 -*-
"""Copy of Image Regression with CNNs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wx4NOOpM7wA90g0EZDxPBG9gFj2oIymZ

#Environment Setup

##Set Flag for Local or Hosted Runtime
"""

import os
import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import backend as K
from keras.models import Model, Sequential
from keras.layers import Dense, GlobalAveragePooling2D, MaxPooling2D, Lambda, Cropping2D
from keras.layers.convolutional import Convolution2D
from keras.layers.core import Flatten, Dense, Dropout, SpatialDropout2D
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator

import sklearn
from sklearn.model_selection import train_test_split
import pandas as pd

print("Tensorflow Version:", tf.__version__)
print("Tensorflow Keras Version:", tf.keras.__version__)

## Extract Dataset

path = '/home/wil/catkin_ws/src/diy_driverless_car_ROS/rover_ml/output'
data_set = 'office_2'
tar_file = data_set + ".tar.gz"
"""## Parse CSV File"""

# Define path to csv file

csv_path = path + '/' + data_set + '/interpolated.csv'

# Load the CSV file into a pandas dataframe
df = pd.read_csv(csv_path, sep=",")

# Print the dimensions
print("Dataset Dimensions:")
print(df.shape)

# Print the first 5 lines of the dataframe for review
print("\nDataset Summary:")
df.head(5)
"""# Clean and Pre-process the Dataset

## Remove Unneccessary Columns
"""

# Remove 'index' and 'frame_id' columns
df.drop(['index', 'frame_id'], axis=1, inplace=True)

# Verify new dataframe dimensions
print("Dataset Dimensions:")
print(df.shape)

# Print the first 5 lines of the new dataframe for review
print("\nDataset Summary:")
df.head(5)
"""## Detect Missing Data"""

# Detect Missing Values
print("Any Missing Values?: {}".format(df.isnull().values.any()))

# Total Sum
print("\nTotal Number of Missing Values: {}".format(df.isnull().sum().sum()))

# Sum Per Column
print("\nTotal Number of Missing Values per Column:")
print(df.isnull().sum())
"""## Remove Zero Throttle Values"""

# Determine if any throttle values are zeroes
print("Any 0 throttle values?: {}".format(df['speed'].eq(0).any()))

# Determine number of 0 throttle values:
print("\nNumber of 0 throttle values: {}".format(df['speed'].eq(0).sum()))

# Remove rows with 0 throttle values
if df['speed'].eq(0).any():
    df = df.query('speed != 0')

    # Reset the index
    df.reset_index(inplace=True, drop=True)

# Verify new dataframe dimensions
print("\nNew Dataset Dimensions:")
print(df.shape)
df.head(5)
"""## View Label Statistics"""

# Steering Command Statistics
print("\nSteering Command Statistics:")
print(df['angle'].describe())

print("\nThrottle Command Statistics:")
# Throttle Command Statistics
print(df['speed'].describe())
"""## Define an Image Data Generator and Split the Dataset"""

aug = 0

if aug:

    # Create a non augmented image generator for validation
    datagen = ImageDataGenerator(rescale=1. / 255.)

    # Construct the image generator for data augmentation
    aug_datagen = ImageDataGenerator(
        rotation_range=20,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest")

    df_train, df_validation = train_test_split(df, test_size=0.25)
    print("\nTraining Set:\n")
    print(train.shape)
    print("\nValidation Set:\n")
    print(test.shape)
else:
    datagen = ImageDataGenerator(rescale=1. / 255., validation_split=0.25)
"""## Load Data Generators

[Keras Image Processing Documentation](https://keras.io/preprocessing/image/)
"""

df2 = df.sample(frac=1).reset_index(drop=True)
df2 = df2.head(2500)

batch_size = 32

dir = path + '/' + data_set + '/'

if aug:

    # Create augmentation image directory
    aug_path = dir + 'aug'

    os.chdir(dir)
    #!if [ -d 'aug' ]; then echo 'Augmentation Directory Exists'; else mkdir 'aug' ; fi

    dataframe_train = df_train
    dataframe_validation = df_validation

    print("\nNumber of training samples:")

    train_generator = aug_datagen.flow_from_dataframe(
        dataframe=dataframe_train,
        directory=dir,
        x_col="filename",
        y_col="angle",
        subset="training",
        batch_size=batch_size,
        seed=42,
        shuffle=True,
        class_mode="raw",
        validate_filenames=True,
        target_size=(180, 320))

    print("\nNumber of validation samples:")

    valid_generator = datagen.flow_from_dataframe(
        dataframe=dataframe_validation,
        directory=dir,
        x_col="filename",
        y_col="angle",
        subset="validation",
        batch_size=batch_size,
        seed=42,
        shuffle=True,
        class_mode="raw",
        validate_filenames=True,
        target_size=(180, 320)
        #save_to_dir=aug_path,
        #save_prefix='test'
    )

else:
    dataframe_train = df  #df
    dataframe_validation = df  #df

    print("\nNumber of training samples:")

    train_generator = datagen.flow_from_dataframe(
        dataframe=dataframe_train,
        directory=dir,
        x_col="filename",
        y_col="angle",
        subset="training",
        batch_size=batch_size,
        seed=42,
        shuffle=True,
        class_mode="raw",
        validate_filenames=True,
        target_size=(180, 320))

    print("\nNumber of validation samples:")

    valid_generator = datagen.flow_from_dataframe(
        dataframe=dataframe_validation,
        directory=dir,
        x_col="filename",
        y_col="angle",
        subset="validation",
        batch_size=batch_size,
        seed=42,
        shuffle=True,
        class_mode="raw",
        validate_filenames=True,
        target_size=(180, 320)
        #save_to_dir=aug_path,
        #save_prefix='test'
    )
"""# Build and Train the Model

## Preprocess the Input Image
"""

# Initialize the model
model = Sequential()

# trim image to only see section with road
# (top_crop, bottom_crop), (left_crop, right_crop)
model.add(Cropping2D(cropping=((0, 0), (0, 0)), input_shape=(180, 320, 3)))
"""## Build the Model"""

# Nvidia model
model.add(
    Convolution2D(
        24, (5, 5), activation="relu", name="conv_1", strides=(2, 2)))
model.add(
    Convolution2D(
        36, (5, 5), activation="relu", name="conv_2", strides=(2, 2)))
model.add(
    Convolution2D(
        48, (5, 5), activation="relu", name="conv_3", strides=(2, 2)))
model.add(SpatialDropout2D(.5, dim_ordering='default'))

model.add(
    Convolution2D(
        64, (3, 3), activation="relu", name="conv_4", strides=(1, 1)))
model.add(
    Convolution2D(
        64, (3, 3), activation="relu", name="conv_5", strides=(1, 1)))

model.add(Flatten())

model.add(Dense(1164))
model.add(Dropout(.5))
model.add(Dense(100, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(50, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(10, activation='relu'))
model.add(Dropout(.5))
model.add(Dense(1))

model.compile(
    loss='mse', optimizer='adam', metrics=['mse', 'mae', 'mape', 'cosine'])

# Print model sumamry
model.summary()
"""## Setup Checkpoints"""

# checkpoint
model_path = data_set + '/model'

os.chdir(path)
#!if [ -d $model_path ]; then echo 'Directory Exists'; else mkdir $model_path; fi

filepath = path + '/' + model_path + "/weights-improvement-{epoch:02d}-{val_loss:.2f}.hdf5"
checkpoint = ModelCheckpoint(
    filepath,
    monitor='val_loss',
    verbose=1,
    save_best_only=True,
    mode='auto',
    period=1)

#model.load_weights(model_path + '/model.h5')
"""## Setup Early Stopping to Prevent Overfitting"""

from keras.callbacks import EarlyStopping

# The patience parameter is the amount of epochs to check for improvement
early_stop = EarlyStopping(monitor='val_loss', patience=10)
"""## Training"""

# Define step sizes
STEP_SIZE_TRAIN = train_generator.n // train_generator.batch_size
STEP_SIZE_VALID = valid_generator.n // valid_generator.batch_size

# Define number of epochs
n_epoch = 50

# Define callbacks
#callbacks_list = [tbCallBack]
#callbacks_list = [TensorBoardColabCallback(tbc), early_stop]
callbacks_list = [early_stop, checkpoint]

# Fit the model
history_object = model.fit_generator(
    generator=train_generator,
    steps_per_epoch=STEP_SIZE_TRAIN,
    validation_data=valid_generator,
    validation_steps=STEP_SIZE_VALID,
    callbacks=callbacks_list,
    #use_multiprocessing=True,
    epochs=n_epoch)
"""## Save the Model"""

# Save model
model_path_full = path + '/' + model_path + '/'

model.save(model_path_full + 'model.h5')
with open(model_path_full + 'model.json', 'w') as output_json:
    output_json.write(model.to_json())

# Save TensorFlow model
tf.train.write_graph(
    K.get_session().graph.as_graph_def(),
    logdir=model_path_full,
    name='model.pb',
    as_text=False)
"""# Evaluate the Model

## Plot the Training Results
"""

model_path_full = path + '/' + model_path + '/'

# Plot the training and validation loss for each epoch
print('Generating loss chart...')
plt.plot(history_object.history['loss'])
plt.plot(history_object.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.savefig(model_path_full + 'model.png')

# Done
print('Done.')
"""## Print Performance Metrics"""

scores = model.evaluate_generator(
    valid_generator, STEP_SIZE_VALID, use_multiprocessing=True)

metrics_names = model.metrics_names

print("{}: {:.3}\n{}: {:.3}\n{}: {:.3}".format(metrics_names[0], scores[0],
                                               metrics_names[1], scores[1],
                                               metrics_names[2], scores[2]))
"""## Create a Test Dataset"""

df_test = df2.sample(frac=1).reset_index(drop=True)
df_test = df_test.head(10)

batch_size = 32

dir = path + '/' + data_set + '/'

print("\nNumber of test samples:")

test_generator = datagen.flow_from_dataframe(
    dataframe=df_test,
    directory=dir,
    x_col="filename",
    y_col="angle",
    batch_size=batch_size,
    shuffle=False,
    class_mode="raw",
    validate_filenames=True,
    target_size=(180, 320))

#df_test.head(10)
"""## Compute Prediction Statistics"""

preds = model.predict_generator(
    test_generator, steps=len(test_generator), verbose=1)
#print(preds)
#print(test_generator.filenames)
#print(test_generator.labels)

testX = test_generator.filenames
testY = test_generator.labels
df_testY = pd.Series(testY)
df_preds = pd.Series(preds.flatten)

# Replace 0 angle values
if df_testY.eq(0).any():
    df_testY.replace(0, 0.0001, inplace=True)

# Calculate the difference
diff = preds.flatten() - df_testY
percentDiff = (diff / testY) * 100
absPercentDiff = np.abs(percentDiff)

# compute the mean and standard deviation of the absolute percentage
# difference
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)
print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))

# Compute the mean and standard deviation of the difference
print(diff.describe())

# Plot a histogram of the prediction errors
num_bins = 25
hist, bins = np.histogram(diff, num_bins)
center = (bins[:-1] + bins[1:]) * 0.5
plt.bar(center, hist, width=0.05)
plt.title('Historgram of Predicted Error')
plt.xlabel('Steering Angle')
plt.ylabel('Number of predictions')
plt.plot(np.min(diff), np.max(diff))

# Plot a Scatter Plot of the Error
plt.scatter(testY, preds)
plt.xlabel('True Values ')
plt.ylabel('Predictions ')
plt.axis('equal')
plt.axis('square')
plt.xlim([0, plt.xlim()[1]])
plt.ylim([0, plt.ylim()[1]])
"""## Plot a Prediction"""

# Plot the image with the actual and predicted steering angle
img_name = path + '/' + data_set + '/' + testX[0]
center_image = cv2.imread(img_name)
center_image_mod = cv2.resize(center_image,
                              (320, 180))  #resize from 720x1280 to 180x320
plt.imshow(center_image_mod)
plt.grid(False)
plt.xlabel('Actual: {:.2f} Predicted: {:.2f}'.format(testY[0],
                                                     float(preds[0])))
plt.show()
"""# References:
https://www.pyimagesearch.com/2019/01/28/keras-regression-and-cnns/
https://www.pyimagesearch.com/2019/01/21/regression-with-keras/
https://www.pyimagesearch.com/2018/12/24/how-to-use-keras-fit-and-fit_generator-a-hands-on-tutorial/
https://colab.research.google.com/github/tensorflow/examples/blob/master/courses/udacity_intro_to_tensorflow_for_deep_learning/l04c01_image_classification_with_cnns.ipynb#scrollTo=7MqDQO0KCaWS
"""