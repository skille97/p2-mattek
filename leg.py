import os, sys
from p2PCA import PCA
import STFTsignal
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt


# Open a file
path = "lyd/"
dirs = os.listdir( path )

# This would print all the files and directories
for file in dirs:
   if file == ".DS_Store":
       continue
   print (file)
   samplingrate, audio = STFTsignal.audiosignal(path + file)
   _, _, Zxx = STFTsignal.stft_of_signal('hanning', 4096, 0.5, audio, samplingrate)
   mean, eigen, weights = PCA(Zxx)


