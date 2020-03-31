from scipy.io.wavfile import read
from scipy.signal import stft
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

rate, audio = read("piano-C4.wav")

fourier = np.fft.fft(audio)
fourier = np.abs(fourier)

freq = np.fft.fftfreq(len(fourier), d=1/rate)

plt.figure()
plt.plot(freq[5:4000], fourier[5:4000])
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.savefig("C4freq.pdf")

time = np.linspace(0, len(audio)/rate, len(audio))
plt.figure()
plt.plot(time, audio, 'r')
plt.xlabel("Time [s]")
plt.savefig("C4audio.pdf")

# window=['rectangular','hanning','hamming','blackman']

def stftplot(window,windowlength,overlap,inputsignal):
    for i in window:
        f,t,Zxx = stft(inputsignal, fs=rate, window=i, nfft=len(audio) ,nperseg=windowlength, noverlap=windowlength*overlap, boundary='zeros',axis=-1)     
        plt.figure()
        plt.pcolormesh(t, f, np.abs(Zxx), vmin=0,)
        plt.title(f'STFT Magnitude, window: {i:}')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')

        plt.savefig(f'spectrogramC4{window}.jpg', dpi=150)
    return f, t, Zxx

overlap= 0.5
f,t,Zxx=stftplot(['hanning'],200,overlap,audio)

plt.figure()
plt.plot(f[5:4000], fourier[5:4000]) 

print(Zxx[0]) #Zxx[0] består af frekvensindhold til frame 0

print((time[-1])/(1/rate*200*(1-overlap))) #Sådan beregnes antal af frames
