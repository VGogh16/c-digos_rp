# In[1]:
import pyvisa
from struct import unpack
#import pylab
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# In[2]: busca recursos VISA (Osciloscopio, etc.)
rm = pyvisa.ResourceManager()
rm.list_resources()
rm.list_resources()[0]
scope = rm.open_resource(rm.list_resources()[0])
# In[]: Limpia Queue y enciende canales a usar
scope.write('*CLS')
scope.write(":SELECT:CH1 on")
# scope.write(":SELECT:CH2 on")
#scope.write(":SELECT:CH3 on")
#scope.write(":SELECT:CH4 on")
#scope.write(":SELECT:CONTROL CH4")

# In[]:
scope.write('DATA:SOUrce CH1')
scope.write('WFMO:ENC BINARY')
scope.write('WFMO:BYT_N 1')
scope.write('DATA SNAP')
scope.write('TRIGger:TYPE EDGE')
scope.write('TRIGger:EDGE:SLOpe RISE')
scope.write('TRIGger:MODe NORMAL')
#scope.write("TRIGger:MAI:LEV 0.005")
# In[]:
os.chdir('C:\\Detectores proyecto')
# fopen = open("ECG_Pomposo.bin","wb")
Head = open('Config_Met27.1.txt', 'w')    

scope.write('DATA:SOUrce CH1')
ymult = (scope.query('WFMPRE:YMULT?'))
xincr = (scope.query('WFMPRE:XINCR?'))
yzero = (scope.query('WFMPRE:YZERO?'))
yoff = (scope.query('WFMPRE:YOFF?'))

Head.write('Sample Time: ')
Head.write(xincr)
Head.write(' \n')
Head.write('Channel 1: ')
Head.write(' \n')
Head.write('Y1:')
Head.write(ymult)
Head.write('Level 1:')
Head.write(yzero)
Head.write('Offset 1:')
Head.write(yoff)
Head.write(' \n')

Head.close()

# In[]:
scope.write('HORizontal:RECOrdlength 1e4')
scope.write('DATA:SOU CH1;:DATA:WIDTH 1;:DATA:ENC RPB;:DATA:START 1;:DATA:STOP 1e4;:ACQ:STOPA SEQ')
scope.write("ACQ:STATE ON")

 # In[5]:
# os.chdir('/Users/laboratorio/Documents/Software/SiPM_single'
# C:\Users\Luc\Documents\Datos
# C:\Users\lucio\Documentos\MEGA\Python\ECG
#os.chdir('D:/Software/data')


# os.chdir('C:/Users/Lucio/Documentos/MEGA/Python/EMG')
fopen1 = open("DetRad_E1_27_1V.bin","wb")
# fopen2 = open("CH2_MET.bin","wb")
ndatos=50

waveA=[]
# waveA2=[]

cuenta = 0
TInicio = time.time()


for i in range(ndatos):
    while '1' in scope.query("ACQ:STATE?"):
        time.sleep(1)
    scope.write('DATA:SOU CH1')
    scope.write('CURVE?')
    data=scope.read_raw()
    hl=2+int(data[1])  
    signal=data[hl:-1]
    waveA.append(signal)

    CharSlow = signal+b'\r' + b'\n'
    fopen1.write(CharSlow)       # Guarda señal actual
    
    
    # scope.write('DATA:SOU CH2')
    # scope.write('CURVE?')
    # data2=scope.read_raw()
    # hl2=2+int(data2[1])  
    # signal2=data2[hl2:-1]
    # waveA2.append(signal2)
    # CharSlow2 = signal2+b'\r' + b'\n'
    # fopen2.write(CharSlow2)       # Guarda señal actual
 
    adc=np.array(unpack('%sB'%len(signal),signal))
    plt.plot(adc)
    
    cuenta += 1
    print(cuenta)
    scope.write("ACQ:STATE ON")
TFin = time.time()
TTransc = (TFin-TInicio)/60
TSeg = TTransc
print("Fin de captura en.. "+str(TSeg)+" minutos")

plt.show()
fopen1.close()
# fopen2.close()
# In[]:
# plt.figure(2)
# for i in range(ndatos):
#     adc=np.array(unpack('%sB'%len(waveA[i]),waveA[i]))
#     # plt.subplot(211)
#     plt.plot(adc)

# In[]
# datos = ndatos

# for row in range(ndatos):
#     CharSlow = waveA[row]+b'\r' + b'\n'
#     fopen.write(CharSlow)
# fopen.close()
# print("Datos Fast guardados")


