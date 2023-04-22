
import keyboard
from PIL import Image
from tkinter import ttk

import tkinter
import time
from andercou_alexandru_auto_learning import *


import andercou_alexandru_Simulare
if __name__ == '__main__':
 choice=input("choose step:\n 1. Simulate  to generate data and train\n"
              " 2. train on existent data\n "
              "3.simulation with auto as an option\n "
              "4.refit the existing model with new aquired data:"

              )
 print(choice)
 if int(choice)==1:
  andercou_alexandru_Simulare.simulate()
  data = init_data()
  model = build_model()
  data_separated = separate_train_test_data(data[0], data[1])
  fit(model, data_separated[0], data_separated[1], data_separated[2], data_separated[3])
  model.save("model")
 else:
  if int(choice) == 2:
   data = init_data()
   model = build_model()
   data_separated = separate_train_test_data(data[0], data[1])
   fit(model, data_separated[0], data_separated[1], data_separated[2], data_separated[3])
   model.save("model")
  else:
    if int(choice)==3:
        andercou_alexandru_Simulare.simulate()
    else:
      if int(choice)==4:
        refit()






