# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 09:21:29 2025

@author: Lucio
"""

import sys
import redpitaya_scpi as scpi

IP = "rp-f0d3a0.local"
rp = scpi.scpi(IP)

wave_form = 'sine'
freq = 200000
ampl = 1

rp.tx_txt('GEN:RST')

rp.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
rp.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
rp.tx_txt('SOUR1:VOLT ' + str(ampl))

# Enable output
rp.tx_txt('OUTPUT1:STATE ON')
rp.tx_txt('SOUR1:TRig:INT')

rp.close()