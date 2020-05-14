import os, sys
from p2PCA import PCA
import STFTsignal
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from SignalToNoiseRatio import addNoise_and_STFT

database = []
testSong = {}
name_list = []
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
       name_list.append(file)
       database.append(songdict)

# def loadTestSong (filename, noice):
#     samplingrate, audio = STFTsignal.audiosignal(filename)
#     audio = audio + np.random.randn(audio.size) * noice
    
#     _, _, testSong["spektrogram"] = STFTsignal.stft_of_signal(audio, samplingrate)
#     testSong["name"] = filename

def PCA_and_SNR(audiofile, noiceRange="range(0,max(audio)*2, int(max(audio)*2/100))"):
    ZxxClean = STFTsignal.getSTFTofFile(audiofile)
    samplingrate, audio = STFTsignal.audiosignal(audiofile)
    
    for i in eval(noiceRange):
        
        testSong["spektrogram"] = addNoise_and_STFT(audio, samplingrate, i)
        testSong["name"] = audiofile
        SNR = np.var(ZxxClean)/np.var(addNoise_and_STFT(audio, samplingrate, i))
        recon_song = recognition()
        print(f"SNR value: {SNR}")
        if f'lyd/{recon_song}' != audiofile:
            break
    
def recognition():
    for i in range(len(database)):
        scores = []
        for j in range(testSong["spektrogram"].shape[1]):
            u = np.transpose(database[i]["eigen"]) @ (testSong["spektrogram"][:, j] - database[i]["mean"])
            scores.append(LA.norm(u - database[i]["weights"][:, j]))
        database[i]["score"] = sum(scores)/len(scores)
  #      print(f"{database[i]['name']} has a score of {database[i]['score']}")
        # plt.plot(scores)
        # plt.title(database[i]['name'])
        # plt.show()

    lowsScore = database[0]
    for song in database[1:]:
        if lowsScore["score"] > song["score"]:
            lowsScore = song
    print("         ")
    print(f"The song with the lowset score is {lowsScore['name']} with a score of {lowsScore['score']}")
    return lowsScore['name']


loadDatabase()
'''
['Band of Horses - The Funeral.wav', 
 'Beethoven - Fur Elise (cover).wav', 
 'Beethoven - Für Elise.wav', 
 'Coldplay - Viva La Vida.wav', 
 'Depeche Mode - Enjoy The Silence.wav', 
 'kings of metal.wav', 
 'L.O.C. - Undskyld.wav', 
 'Manowar - Kings of Metal.wav']
'''
PCA_and_SNR(f"lyd/{name_list[4]}")
print(name_list)
