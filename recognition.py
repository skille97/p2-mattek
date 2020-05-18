import os
from p2PCA import PCA
import STFTsignal
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt


def loadDatabase ():
    """
    Database is created and information stored in a list of dictionaries

    Returns
    -------
    database : list of dictionaries with the neccessary information

    """
    database = []
    # Open a file
    path = "lyd/"
    dirs = os.listdir( path )
    
    # This prints all of the files and directories
    for file in dirs:
       if file == ".DS_Store": #Mac file
           continue
       songdict = {}
       print (file)
       Zxx = STFTsignal.getSTFTofFile(path + file) #STFT of the file
       #mean, eigen and weights are stored in dictionary songdict
       songdict["mean"], songdict["eigen"], songdict["weights"] = PCA(Zxx)
       songdict["name"] = file
       database.append (songdict)  
    return database

def loadTestSong (filename):
    """
    filename and STFT of the file stored in a dictionary
    
    Parameters
    ----------
    filename : TYPE .wav file
    
    Returns
    -------
    testSong : dictioary with information of filename and its STFT 
    """
    testSong = {}
    #information of analysed song stored in dictionary testSong
    testSong["spectrogram"] = STFTsignal.getSTFTofFile(filename)
    testSong["name"] = filename
    return testSong

def recognition(database, testSong, plot=True, info=True):
    """
    An average score is calculated for every song in database with respect to testsong
    and the most alike song from database is printed
    Parameters
    ----------
    database : database with songs, returned from loadDatabase function

    testSong : TYPE dictionary with keywords "spectrogram" and "name"
    
    plot : TYPE, optional
        DESCRIPTION: Plots the score
                     The default is True.
    """
    #Score for every song in database with respect to testsong
    for i in range(len(database)):
        scores = []
        for j in range(testSong["spectrogram"].shape[1]): #every frame of STFT
            #Score is calculated
            u = np.transpose(database[i]["eigen"]) @ (testSong["spectrogram"][:, j] - database[i]["mean"])
            scores.append(LA.norm(u - database[i]["weights"][:, j]))
        #mean value of the scores
        database[i]["score"] = sum(scores)/len(scores)
        if plot == True:
            print(f"{database[i]['name']} has a score of {database[i]['score']}")
            plt.plot(scores)
            plt.title(database[i]['name'])
            plt.show()

    #The lowest score is found and is the most alike to testSong
    lowsScore = database[0]
    for song in database[1:]:
        if lowsScore["score"] > song["score"]:
            lowsScore = song
    if info == True:        
        print("         ")
        print(f"The song with the lowest score is {lowsScore['name']} with a score of {lowsScore['score']}")
    return lowsScore['name']

if __name__ == '__main__':
    database = loadDatabase()
    testSong = loadTestSong("optagelser/band of horses (optag).wav")
    recognition(database, testSong)