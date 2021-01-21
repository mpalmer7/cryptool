# need training data...
# tensorflow (from google) library for machine learning
# cykit learn


import os
try:  # TODO - replace with setuptools
    import tensorflow as tf
except ModuleNotFoundError:
    print("Module requires Google TensorFlow, will attempt to install.")
    os.system('pip3 install --upgrade tensorflow')

#from tensorflow import keras
#import numpy as np

#print(tf.__version__)



cipher_names = ["b64", "binary", "hashsearch", "morse", "substitution_types", "singlebyteXOR"]
