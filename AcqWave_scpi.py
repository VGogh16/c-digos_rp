import numpy as np
import matplotlib.pyplot as plt
import redpitaya_scpi as scpi

IP = "rp-f0d3a0.local"
rp = scpi.scpi(IP)

dec = 1                 #dec = 1 -> 122.8 MSps
trig_lvl = -0.001
data_units = 'volts'
data_format = 'ascii'
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

rp.tx_txt('ACQ:SOUR1:DATA?')
buff_string = rp.rx_txt()           # Obtiene señal en ASCII decimal
                                    # Signal length: 16384
buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
buff = np.array(buff_string).astype(np.float64)

plt.plot(buff)
plt.ylabel('Voltage')
plt.show()