from p2PCA import PCA
import STFTsignal
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

samplingrate, audio = STFTsignal.audiosignal("lyd/BandofHorses.wav")
noiceAudio = audio + np.random.randn(audio.size) * 0
_, _, Zxx = STFTsignal.stft_of_signal('hanning', 4096, 0.5, audio, samplingrate)

samplingrate2, audio2 = STFTsignal.audiosignal("lyd/BandofHorses.wav")
_, _, Zxxnoice = STFTsignal.stft_of_signal('hanning', 4096, 0.5, audio2, samplingrate2)

#Zxx = STFTsignal.getSTFTofFile("lyd/BandofHorses.wav")

mean, eigen, weights = PCA(Zxx)s

a = []
for i in range(Zxx.shape[1]):
    u = np.transpose(eigen)@(Zxxnoice[:,10] - mean)
    a.append(LA.norm(u-weights[:,i]))

plt.plot(a)
plt.show()



