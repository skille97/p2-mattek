import STFTsignal
from SignalToNoiseRatio import addNoise_and_STFT, power
from scipy.io.wavfile import write
import numpy as np
from recognition import recognition, loadDatabase
      
def PCA_and_SNR(audiofile, noiseRange="range(0,int(max(audio)*2), int(max(audio)*2/100))"):
    """
    Noise is added until the audiofile can not be recognised anymore by algorithm.
    When the audiofile is not recognised anymore, an .wav file is created with the
    added amount of noise
    
    Parameters
    ----------
    audiofile : TYPE .wav file

    noiseRange : TYPE, optional, str
        DESCRIPTION:  range of added noise
        The default is "range(0,int(max(audio)), int(max(audio)/100))".
    
    Returns
    -------
    A file with noise added is created ("noisesong.wav")

    """
    testSong = {}
    ZxxClean = STFTsignal.getSTFTofFile(audiofile)
    samplingrate, audio = STFTsignal.audiosignal(audiofile)
    audio = np.float64(audio)
    SNR = power(audio)/power(addNoise_and_STFT(audio, samplingrate, 0)[1])
    for i in eval(noiseRange):
        
        testSong["spectrogram"], noisyAudio = addNoise_and_STFT(audio, samplingrate, i)
        testSong["name"] = audiofile
        
        prevSNR = SNR
        SNR = power(audio)/power(addNoise_and_STFT(audio, samplingrate, i)[1])
        
        recon_song = recognition(database, testSong, plot=None, info=None)
        if f'lyd/{recon_song}' != audiofile or SNR<0.02:
            print(f"""
Actual song: {audiofile}
SNR (%): {prevSNR*100:0.4}
                  """)
            noisyAudio = np.asarray(noisyAudio, dtype=np.int16)
            write('noisesong.wav', samplingrate, noisyAudio)
            break

if __name__ == '__main__':
    # if main, all the songs in database is analysed (Takes time)
    path = 'lyd/'
    database = loadDatabase()
    for i in database:
        PCA_and_SNR(path + i["name"])