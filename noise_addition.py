import STFTsignal
from SignalToNoiseRatio import addNoise_and_STFT, power
from scipy.io.wavfile import write
import numpy as np
from recognition import recognition, loadDatabase
      
def PCA_and_SNR(filename, audiofile, noiseRange="range(0,int(max(audio)*2), int(max(audio)*2/200))", latextable=True):
    """
    Noise is added until the audiofile can not be recognised anymore by algorithm.
    
    Parameters
    ----------
    filename : TYPE name of the audiofile
        
    audiofile : TYPE .wav file

    noiseRange : TYPE, optional, str
        DESCRIPTION:  range of added noise
        The default is "range(0,int(max(audio)*2), int(max(audio)*2/200))".
    
    latextable: TYPE bool, optional
        DESCRIPTION: Returns a print formated as a latextable with results from 
                     noise addition.
                     Defaults to True

    """
    testSong = {}
    samplingrate, audio = STFTsignal.audiosignal(audiofile)
    audio = np.float64(audio)
    SNR = power(audio)/power(addNoise_and_STFT(audio, samplingrate, 0)[1])
    if latextable == True:
        print(filename)
        print("""\\begin{table}[H]
    \centering
    \\begin{tabular}{|l|l|l|}
    \hline
    Artist and Title & Score value & SNR\\\\
    \hline
          """)
    for i in eval(noiseRange):
        
        testSong["spectrogram"], noisyAudio = addNoise_and_STFT(audio, samplingrate, i)
        testSong["name"] = audiofile
        
        prevSNR = SNR
        SNR = power(audio)/power(addNoise_and_STFT(audio, samplingrate, i)[1])
        recon_song, lowScore = recognition(database, testSong, plot=None, info=None)
        #print(f'SNR (%): {SNR*100:0.4}')
        if latextable == True:
            print(f'{recon_song} & {lowScore: 0.7} & {SNR*100:0.4}\\\\')
        else:
            print(f'{recon_song}, SNR: {SNR*100:0.4}')
        if f'lyd/{recon_song}' != audiofile or SNR<0.02:
            if latextable != True:
                print(f"""
Actual song: {audiofile}
SNR (%): {prevSNR*100:0.4}
                  """)
            # noisyAudio = np.asarray(noisyAudio, dtype=np.int16)
            # write(f'(noise) {filename}', samplingrate, noisyAudio)
            if latextable == True:
                print("""\hline
\end{tabular}
\caption{Table of how much gaussian noise there can be added to the song""" + filename + """ until the algorithm matches the wrong song.}
\label{tab:  }
\end{table}""")
                print("         ")
            break


if __name__ == '__main__':
    # if main, all the songs in database is analysed (Takes time)
    path = 'lyd/'
    database = loadDatabase()
    for i in database:
        PCA_and_SNR(i["name"], path + i["name"], latextable=None)
    #PCA_and_SNR(database[-1]["name"], path + database[-1]["name"])
    