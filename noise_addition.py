import STFTsignal
import numpy as np
from SignalToNoiseRatio import addNoise_and_STFT
from scipy.io.wavfile import write
from recognition import loadDatabase, recognition

database = []
testSong = {}
name_list = []

def PCA_and_SNR(audiofile, noiceRange="range(0,max(audio)*2, int(max(audio)*2/100))"):
    ZxxClean = STFTsignal.getSTFTofFile(audiofile)
    samplingrate, audio = STFTsignal.audiosignal(audiofile)
    
    for i in eval(noiceRange):
        
        testSong["spektrogram"], noisyAudio = addNoise_and_STFT(audio, samplingrate, i)
        testSong["name"] = audiofile
        SNR = np.var(ZxxClean)/np.var(addNoise_and_STFT(audio, samplingrate, i)[0])
        recon_song = recognition()
        print(f"SNR value: {SNR}")
        if f'lyd/{recon_song}' != audiofile:
            noisyAudio = np.asarray(noisyAudio, dtype=np.int16)
            write('noisesong.wav', samplingrate, noisyAudio)
            break

loadDatabase()


PCA_and_SNR("lyd/Band of Horses - The Funeral.wav")
