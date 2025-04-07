import numpy as np
import matplotlib.pyplot as plt
import redpitaya_scpi as scpi

IP = "rp-f0d3a0.local"
rp = scpi.scpi(IP)

# In[]: Signal generator
wave_form = 'sine'
freq = 100000
ampl = 1

rp.tx_txt('GEN:RST')

rp.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
rp.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
rp.tx_txt('SOUR1:VOLT ' + str(ampl))

# Enable output
rp.tx_txt('OUTPUT1:STATE ON')
rp.tx_txt('SOUR1:TRig:INT')

# rp.close()

# In[]: Signal Acquisition @122.8 MSps

dec = 1                 #dec = 1 -> 122.8 MSps
trig_lvl = -0.001
data_units = 'raw'
data_format = 'bin'
acq_trig = 'CH1_PE'

rp.tx_txt('ACQ:RST')

rp.tx_txt(f"ACQ:DEC:Factor {dec}")
rp.tx_txt(f"ACQ:DATA:Units {data_units.upper()}")
rp.tx_txt(f"ACQ:DATA:FORMAT {data_format.upper()}")

rp.tx_txt(f"ACQ:TRig:LEV {trig_lvl}")

rp.tx_txt('ACQ:START')
rp.tx_txt(f"ACQ:TRig {acq_trig}")

# while 1:
#     rp.tx_txt('ACQ:TRig:STAT?')
#     if rp.rx_txt() == 'TD':
#         break

## ! OS 2.00 or higher only ! ##
while 1:
    rp.tx_txt('ACQ:TRig:FILL?')
    if rp.rx_txt() == '1':
        break
    
## Reads RAW data from redpitaya
rp.tx_txt('ACQ:SOUR1:DATA?')
buff_byte = rp.rx_arb()
buff = np.frombuffer(buff_byte, dtype='>i2')    # Obtiene señal en RAW en binario
                                                # Signal length: 16384
#buff = [struct.unpack('!h', bytearray(buff_byte[i:i+2]))[0] for i in range(0, len(buff_byte), 2)]

plt.plot(buff)
plt.ylabel('Voltage')
plt.show()