from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

rate, audio = read("piano-C4.wav")

fourier = np.fft.fft(audio)
fourier = np.abs(fourier)

freq = np.fft.fftfreq(len(fourier), d=1/rate)

plt.plot(freq[5:4000], fourier[5:4000])
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.savefig("C4freq.pdf")

#t = np.linspace(0, len(audio)/rate, len(audio))
#plt.plot(t, audio)
#plt.xlabel("Time [s]")
#plt.savefig("C4audio.pdf")
