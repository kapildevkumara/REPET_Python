from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np
import xlsxwriter
from scipy import signal
from scipy import stats

rate, data = wavfile.read('S1.wav')
# STFT matrix with window length = w and overlap 50%
w = 2**10
d = len(data)

f, t, X = signal.stft(data, fs=rate, window='hann', nperseg=w, noverlap=w/2, nfft=None, detrend=False, return_onesided=True, boundary='zeros', padded=True, axis=-1)

# f, t, X = signal.stft(data, fs=rate, window='hann', nperseg=w, noverlap=w/2, nfft=None, detrend=False, return_onesided=True, boundary='zeros', padded=True, axis=-1)

STFT_Abs =  np.absolute(X)
STFT_Abs_Sq = np.square(STFT_Abs)

# Writing in Excel Sheet to view the elements of A
workbook = xlsxwriter.Workbook('K2.xlsx')
worksheet = workbook.add_worksheet('Autocorrelation_STFT_Data')
c=0
A = np.correlate(STFT_Abs_Sq[0][:], STFT_Abs_Sq[0][:], mode='full')
for c in range(0,len(f)):
 y = np.correlate(STFT_Abs_Sq[c][:], STFT_Abs_Sq[c][:], mode='full')
 worksheet.write_column(0,c,y)
 c=c+1
 A = np.column_stack((A,y))
A = np.delete(A, 0, 1)

worksheet = workbook.add_worksheet('Auto_Corr')
r = len(t)
for r in range(len(t),2*len(t)):
  A[r-1][:] = np.divide(A[r-1][:], r+1-len(t))
  worksheet.write_row(-len(t)+r, 0, (A[r-1][:]))
  r=r+1
workbook.close() 

Avg = np.sum(A, axis = 1)
sample = np.arange(2*len(t)-1)

plt.fill_between(sample, Avg, color='k') 
plt.xlabel('Delay')
plt.ylabel('Amplitude')
plt.savefig('Beat.png', dpi=100)
plt.show()
