import STFTsignal
import numpy as np
from SignalToNoiseRatio import addNoise_and_STFT
from scipy.io.wavfile import write
from recognition import loadDatabase, recognition

database = []
testSong = {}
name_list = []

def PCA_and_SNR(audiofile, noiceRange="range(0,max(audio)*2, int(max(audio)*2/100))"):
    """
    Noise is added until the audiofile can not be recognised anymore by algorithm.
    When the audiofile is not recognised anymore, an .wav file is created with the
    added amount of noise
    
    Parameters
    ----------
    audiofile : TYPE .wav file

    noiseRange : TYPE, optional, str
        DESCRIPTION:  range of added noise
        The default is "range(0,max(audio)*2, int(max(audio)*2/100))".
    
    Returns
    -------
    A file with noise added is created ("noisesong.wav")

    """
    ZxxClean = STFTsignal.getSTFTofFile(audiofile)
    samplingrate, audio = STFTsignal.audiosignal(audiofile)
    
    for i in eval(noiceRange):
        
        testSong["spectrogram"], noisyAudio = addNoise_and_STFT(audio, samplingrate, i)
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