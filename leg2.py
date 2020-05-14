import os, sys
from p2PCA import PCA
import STFTsignal
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from SignalToNoiseRatio import addNoise_and_STFT

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
       

# def loadTestSong (filename, noice):
#     samplingrate, audio = STFTsignal.audiosignal(filename)
#     audio = audio + np.random.randn(audio.size) * noice
    
#     _, _, testSong["spektrogram"] = STFTsignal.stft_of_signal(audio, samplingrate)
#     testSong["name"] = filename
    
def PCA_and_SNR(audiofile, noiceRange="range(0,max(audio)*2, int(max(audio)*2/100))"):
    ZxxClean = STFTsignal.getSTFTofFile(audiofile)
    samplingrate, audio = STFTsignal.audiosignal(audiofile)
    testSong["spektrogram"] = addNoise_and_STFT(audio, samplingrate, 1000)
    testSong["name"] = audiofile
    
    
    SNR = [np.var(ZxxClean)/np.var(addNoise_and_STFT(audio, samplingrate, i)) for i in eval(noiceRange)]
    
    return SNR

def recognition():
    for i in range(len(database)):
        scores = []
        for j in range(testSong["spektrogram"].shape[1]):
            u = np.transpose(database[i]["eigen"]) @ (testSong["spektrogram"][:, j] - database[i]["mean"])
            scores.append(LA.norm(u - database[i]["weights"][:, j]))
        database[i]["score"] = sum(scores)/len(scores)
        print(f"{database[i]['name']} has a score of {database[i]['score']}")
        plt.plot(scores)
        plt.title(database[i]['name'])
        plt.show()

    lowsScore = database[0]
    for song in database[1:]:
        if lowsScore["score"] > song["score"]:
            lowsScore = song
    print("         ")
    print(f"The song whit the lowset score is {lowsScore['name']} whit a score of {lowsScore['score']}")


loadDatabase()
PCA_and_SNR("lyd/Band of Horses - The Funeral.wav")
recognition()