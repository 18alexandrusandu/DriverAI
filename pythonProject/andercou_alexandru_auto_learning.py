# This is a sample Python script.
import numpy
import numpy as np
from  keras.layers import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from keras import *
from keras import losses
from keras import regularizers
from keras import optimizers
import matplotlib.pyplot as plt
from matplotlib import image
import tensorflow as tf
import os
import re
from sklearn.model_selection import train_test_split
from keras.callbacks import  EarlyStopping
from sklearn.preprocessing import MinMaxScaler


def read_data(path="data_AI_DRive.csv"):
  f=open(path,"r")
  labels=[]
  data=[]
  Lines = f.readlines()
  count=0
  for l in Lines:
      if count%2==0:
        label=l.strip()
        labels.append(label)
      else:
       sensors=[]
       nrs=l.split(" ")
       print("array:",nrs)
       for nr in nrs:
          if (not nr=="\n") and not nr=="":
           sensors.append(float(nr))
       data.append(np.array(sensors))
      count+=1

  scaler = MinMaxScaler()
  scaler.fit(data)
  data = scaler.transform(data)
  return (data,labels)


def encode_numericaly_labels(labels,categories=None):
    nr_label=0
    new_labels=[]
    uniqueLabel=[]
    uniqueLabelEncoded=[]
    for label in labels:
      print("label",label)
      if not categories==None:
        print("intrat")
        print("label",label)
        print("categories",categories)
        if label in categories:
            print("intra")
            ind=categories.index(label)
            new_labels.append(ind)
      else:
       if  label in uniqueLabel:
         ind= uniqueLabel.index(label)
         new_labels.append(uniqueLabelEncoded[ind])
         continue
       else:
          new_labels.append(nr_label)
          uniqueLabel.append(label)
          uniqueLabelEncoded.append(nr_label)
          nr_label=nr_label+1

    print("labels:",new_labels)
    return new_labels

def make_one_hot_encodings(labels_num,nr_labels=-1):
    start = min(labels_num)
    size = max(labels_num) - start
    encodings = []

    if nr_labels>0:
        for label in labels_num:
            hot_encoding = []
            for i in range(nr_labels):
                if i == label:
                    hot_encoding.append(1.0)
                else:
                    hot_encoding.append(0.0)
            encodings.append(np.array(hot_encoding))
    else:
     for label in labels_num:
        hot_encoding=[]
        for i in range(size+1):
            if i+start == label:
                hot_encoding.append(1.0)
            else:
                hot_encoding.append(0.0)
        encodings.append(np.array(hot_encoding))
    return encodings

def separate_train_test_data(X_data,Y_data):
     X_train, X_test, y_train, y_test = train_test_split(
        X_data, Y_data, test_size=0.3, random_state=0)
   # X_train=np.array(X_train)


     return (X_train,y_train, X_test,y_test)



def init_data():
 data=read_data()
 x_data,y_data=data
 numric_y=encode_numericaly_labels(y_data,["forward","stop","left","right"])
 labels=make_one_hot_encodings(numric_y,4)
 print(y_data)
 print(numric_y)
 print(labels)
 return (x_data,labels)

def build_model(name="driver"):
    print(name)
    model=Sequential()
    model.add(Dense(10,activation='relu',input_shape = (None,10)))
    model.add(Dense(20, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(4, activation='softmax'))

    model.compile(optimizer='adam',
    loss='categorical_crossentropy',metrics=["accuracy"])
    model.summary()
    return model

    # Use a breakpoint in the code line below to debug your script.
def fit(model,X_data_train,labels_train,X_data_test,labels_test,):
   x_data_train_nd=numpy.stack(X_data_train)
   y_data_train_nd = numpy.stack(labels_train)

   x_data_test_nd = numpy.stack(X_data_test)
   y_data_test_nd = numpy.stack(labels_test)

   early_stoping_mon=EarlyStopping(monitor='loss', patience=100)
   model.fit( x=x_data_train_nd, y=y_data_train_nd,
   batch_size = 10,
   epochs=5000,
   verbose = 1,
   validation_data = (x_data_test_nd, y_data_test_nd),
   callbacks=[early_stoping_mon]
              )
   return model

from  keras import models
def refit():
    model=models.load_model("model")
    data = init_data()
    data_separated = separate_train_test_data(data[0], data[1])
    X_data_train=data_separated[0]
    labels_train=data_separated[1]
    X_data_test=data_separated[2]
    labels_test=data_separated[3]

    x_data_train_nd = numpy.stack(X_data_train)
    y_data_train_nd = numpy.stack(labels_train)

    x_data_test_nd = numpy.stack(X_data_test)
    y_data_test_nd = numpy.stack(labels_test)

    early_stoping_mon = EarlyStopping(monitor='loss', patience=100)
    model.fit(x=x_data_train_nd, y=y_data_train_nd,
              batch_size=10,
              epochs=5000,
              verbose=1,
              validation_data=(x_data_test_nd, y_data_test_nd),
              callbacks=[early_stoping_mon]
              )
    model.save("model")
    return model