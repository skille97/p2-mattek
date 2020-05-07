from p2PCA import PCA
import STFTsignal
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

#database = [{mean, eigen, weights, name},{},{}]
#testSong = {} % kommer fra cmd arg
def loadDatabase():
    pass

def loadTestSong(noise):
    pass

def comperToDatabase():
    pass

samplingrate, audio = STFTsignal.audiosignal("lyd/BandofHorses.wav")
_, _, Zxx = STFTsignal.stft_of_signal('hanning', 4096, 0.5, audio, samplingrate)

noiceAudio = audio + np.random.randn(audio.size) * 1000
samplingrate2, audio2 = STFTsignal.audiosignal("lyd/KingsofMetal.wav")
_, _, Zxxnoice = STFTsignal.stft_of_signal('hanning', 4096, 0.5, audio2, samplingrate)

#Zxx = STFTsignal.getSTFTofFile("lyd/BandofHorses.wav")

mean, eigen, weights = PCA(Zxx)

a = []
for i in range(Zxx.shape[1]):
    u = np.transpose(eigen)@(Zxxnoice[:,i] - mean)
    a.append(LA.norm(u-weights[:,i]))

plt.plot(a)
plt.show()



