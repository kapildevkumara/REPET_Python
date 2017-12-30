from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np
import xlsxwriter
from scipy import signal
from scipy import stats

# STFT matrix with window length w and overlap 50%
w = 2**12
rate, data = wavfile.read('S1.wav')
d = len(data)
# The Beat value obtained from Part 1 File
Beat = 249

f, t, X = signal.stft(data, fs=rate, window='hann', nperseg=w, noverlap=w/2, nfft=None, detrend=False, return_onesided=True, boundary='zeros', padded=True, axis=-1)
# a = len(t) = int((d/(len(f)-1))+1)
i=0
# (int(a/Beat)) should be changed to (int(a/Beat)+1)
STFT = np.ones([len(f), Beat*(int(len(t)/Beat))], complex)
for i in range(0,len(f)):
    j=0
    for j in range(0, Beat*(int(len(t)/Beat))):
     STFT[i][j] = X[i][j]
     j=j+1
    i=i+1
STFT_Abs = np.absolute(STFT)
S_S = STFT.reshape(len(f),Beat,(int(len(t)/Beat)), order='F')
S = np.absolute(S_S)
Mean = stats.mstats.gmean(S, 2)
V_bar = np.ones(np.shape(S))
M = np.zeros(np.shape(S))
         
i=j=k=0 
for i in range(0, len(f)):
 j=0
 for j in range(0, Beat):
  k=0
  for k in range(0, int(len(t)/Beat)):
   V_bar[i][j][k] = np.absolute(np.log(np.divide(S[i][j][k],Mean[i][j])))
   if(V_bar[i][j][k]<1):
    M[i][j][k]=1
   else:
    M[i][j][k]=0
   k=k+1
  j=j+1
 i=i+1

X1 = np.shape(S)
X1 = np.multiply(S_S,M)
X1_Linear = X1.reshape(len(f),Beat*(int(len(t)/Beat)), order='F') 
 
Time, X_Filtered_1 = signal.istft(X1_Linear, rate, window='hann', nperseg=w, noverlap=w/2, nfft=None, input_onesided=True, boundary=True, time_axis=-1, freq_axis=-2)

wavfile.write('S_1.wav', rate, X_Filtered_1)
