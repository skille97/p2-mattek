import STFTsignal
from SignalToNoiseRatio import addNoise_and_STFT
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from numpy import linalg as LA
import os
from p2PCA import PCA
import numpy as np

database = []
testSong = {}

def loadDatabase ():
    # Open a file
    path = "lyd/"
    dirs = os.listdir( path )
    
    # This would print all the files and directories
    for file in dirs:
       if file == ".DS_Store": #Mac file
           continue
       songdict = {}
       print (file)
       samplingrate, audio = STFTsignal.audiosignal(path + file)
       _, _, Zxx = STFTsignal.stft_of_signal(audio, samplingrate)
       songdict["mean"], songdict["eigen"], songdict["weights"] = PCA(Zxx)
       songdict["name"] = file
       database.append (songdict)
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
        
        testSong["spektrogram"], noisyAudio = addNoise_and_STFT(audio, samplingrate, i)
        testSong["name"] = audiofile
        SNR = np.var(ZxxClean)/np.var(addNoise_and_STFT(audio, samplingrate, i)[0])
        recon_song = recognition()
        print(f"SNR value: {SNR}")
        if f'lyd/{recon_song}' != audiofile:
            noisyAudio = np.asarray(noisyAudio, dtype=np.int16)
            write('noisesong.wav', samplingrate, noisyAudio)
            break

def recognition():
    for i in range(len(database)):
        scores = []
        for j in range(testSong["spektrogram"].shape[1]):
            u = np.transpose(database[i]["eigen"]) @ (testSong["spektrogram"][:, j] - database[i]["mean"])
            scores.append(LA.norm(u - database[i]["weights"][:, j]))
        database[i]["score"] = sum(scores)/len(scores)

    lowsScore = database[0]
    for song in database[1:]:
        if lowsScore["score"] > song["score"]:
            lowsScore = song
    print("         ")
    print(f"The song with the lowest score is {lowsScore['name']} with a score of {lowsScore['score']}")
    return lowsScore['name']

if __name__ == '__main__':    
    loadDatabase()
    PCA_and_SNR("lyd/Band of Horses - The Funeral.wav")