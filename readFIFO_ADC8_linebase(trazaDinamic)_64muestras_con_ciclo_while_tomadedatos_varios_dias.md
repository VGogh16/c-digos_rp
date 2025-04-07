
#  D:\redpitaya\tmp\3_stopwatch_modif\readFIFO_ADC_lineabase_dinamic_32muestras\


#Le damos permisos de modificación al archivo readfifo.bit
#!chmod 755 readfifo_linebase_32.bit
#!ls
--                   B7%B6              B5        B4        B3      B2       B1          B0

                                 nrst      cntrl_clk              rd_en_out wr_en_out
                                       
leds <=  ADC_counter(24 downto 23) & gpioIN(3) & gpioIN(2) & empty & full & gpioIN(1) & gpioIN(0);


# Proyecto vivado localizado en D:\redpitaya\tmp\3_stopwatch_modif\readFIFO_ADC_lineabase_dinamic_32muestras\

scp .\system_wrapper.bit root@192.168.100.10:/root/RedPitaya/readfifo_linebaseDinamic.bit

# Para el copiado del archivo a rp es 
# scp readFIFO_64.bit root@rp-f04e41:~/RedPitaya

# Dar permisos de editor con chmod 777 para poder activar el archivo en 
# terminal

# archivo bitstream read_FIFO64muestras.bit, localizado en /root/RedPitaya
## ejecutar la operacion siguiente antes del inicio de ejecución del código python

## cat  readFIFO_ADC64muestras.bit > /dev/xdevcfg

## se ejecuta el programa a 64 muestras y con un buffer de 512 datos en vez de 1024

## wr_en_out <= gpioIN(0);
## rd_en_out <= gpioIN(1);
## cntrl_clk    <= gpioIN(2);
## nrst           <= gpioIN(3);
## --               <= gpioIN(4);   Control modo de adquisición
## --               <= gpioIN(5);   Control modo de adquisición
## --               <= gpioIN(6);
## --               <= gpioIN(7);

| gpioIN(5-4) | ADC_FIFO    || clock_FIFO    | Description   |
|-------------|-------------||---------------|---------------|
|   ``00``    | ADC_DATA    || ``sysClkOut`` | Traza Cascada |
|   ``01``    | ADC_DATA    || ``sysClk``    | Free Cascada  |
|   ``10``    | ADC_Counter || ``sysClkOut`` | Traza Counter |
|   ``11``    | ADC_Counter || ``sysClk``    | Free Counter  |

|    Base Address      |    AXI         ||   Size   |
|----------------------|----------------||----------|
|   ``0x4120_0000``    | AXI_control    || ``64K``  |
|   ``0x4200_0000``    | AXI_gencontrol || ``4K``   |
|   ``0x4121_0000``    | AXI_umbral     || ``64K``  |

# Umbral Dinámico
## Estas instrucciones establecen el umbral desde el prompt 


```python
from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10
regset = MMIO(0x41210000, 0xC)
regset.write32(0,0xFF) # 
print(regset.read32(0x0))
```

    255



```python
regset = MMIO(0x41210000, 0xC)
print(regset.read32(0x08))
```

    0


# gpioIN(5-4) 11 ADC_Counter sysClk   (FreeCounter)


```python
TrazaCascada = 0x00
FreeCascada  = 0x10
TrazaCounter = 0x20
FreeCounter  = 0x30

modo = FreeCounter
# MMIO = Memory-mapped I/O(Input/Output) 
# MMIO almacena una dirección en un  espacio fisico dentro de la memoria ram, ademas la memoria y los registros 
#obtenidos por (I/O) son mapeados o asociados a valores de direccion

# dependiendo de la dirección se dara la orden de escribir o leer, esta seleccion dependera de la dirección que tenga como entrada 
# cuando accedemos a la dirección 4120 0000 estamos accediendo al axi de control 
# cuando accedemos a la dirección 4200 0000 estamos accediendo al axi de gencount
# con el comando write32 
from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10
regset = MMIO(0x41200000, 0xc)
regset.write32(0,modo | 0x08) # 

```


```python
from periphery import MMIO
import numpy as np


TrazaCascada = 0x00
FreeCascada  = 0x10
TrazaCounter = 0x20
FreeCounter  = 0x30

modo = TrazaCounter

regset = MMIO(0x41200000, 0xc)
regset.write32(0, modo | 0x08) # 
```


```python
regset = MMIO(0x41200000, 0xc)
regset.write32(0, modo | 0x01 ) # wr_en = 1
```


```python
import time
regset = MMIO(0x41200000, 0xc)
regset.write32(0, modo | 0x08) # reset
regset.write32(0, modo | 0x01) # wr_en = 1
time.sleep(1)
regset.write32(0, modo | 0x02) # rd_en = 1

datos = []
for i in range(1030):
    regset.write32(0, modo | 0x02)# rd_en = 1
    regset.write32(0, modo | 0x06)# cntrl_clk rd_en = 1
    dato = 0x3FFF & regset.read32(0x08) # en mascara los 14 bits menos significativos
    datos.append(dato)
    print(hex(dato))



# Propuesta Inicial leer la FIFO en forma sincrona
## regset = empty & full & 14BitsADC


```python
from periphery import MMIO
import numpy as np

TrazaCascada = 0x00
FreeCascada  = 0x10
TrazaCounter = 0x20
FreeCounter  = 0x30

modo = TrazaCounter

ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10
regset = MMIO(0x41200000, 0xc)
regset.write32(0, modo | 0x08) # 

```


```python
import time
import matplotlib.pyplot as plt
%matplotlib inline
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


```


```python
import time
regset = MMIO(0x41200000, 0xc)
#regset.write32(0,0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
#regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
#time.sleep(1)
#regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;  0x30 | 0x30 | 
TrazaCascada = 0x00
FreeCascada  = 0x10
TrazaCounter = 0x20
FreeCounter  = 0x30
modo = TrazaCounter

datos = []
for i in range(2):
    datos = []
    regset.write32(0, modo | 0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
    regset.write32(0, modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_ou 0x30 | t = 1;   
    #regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
    #regset.write32(0,0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
    dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
    while(dato != 0x10000 ):
        dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos signif 0x30 | icativos
        regset.write32(0, modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; w 0x30 | r_en_out = 1;
    
    tmp = regset.read32(0x08)
    dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
    while(dato != 0x20000 ):
        regset.write32(0, modo | 0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
        regset.write32(0, modo | 0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
        datos.append(tmp)
        print(hex(tmp))
        tmp = regset.read32(0x08)
        dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
    print("==================================================")
    print(i)
    
    

```

   



```python
import time
import matplotlib.pyplot as plt
%matplotlib inline

from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10

TrazaCascada = 0x00
FreeCascada  = 0x10
TrazaCounter = 0x20
FreeCounter  = 0x30
modo = TrazaCounter

regset = MMIO(0x41200000, 0xc)
regset.write32(0, modo | 0x08) # 


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


regset = MMIO(0x41200000, 0xc)
#regset.write32(0,0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
#regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
#time.sleep(1)
#regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;

datos = []
for i in range(5):
    datos = []
    regset.write32(0, modo | 0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
    regset.write32(0, modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;   
    #regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
    #regset.write32(0,0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
    dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
    while(dato != 0x10000 ):
        dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
        regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
    
    tmp = regset.read32(0x08)
    dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
    intDatos = []
    while(dato != 0x20000 ):
        regset.write32(0, modo | 0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
        regset.write32(0, modo | 0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
        datos.append(tmp)
        #print(hex(tmp))
        tmp = regset.read32(0x08)
        dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
        tmp = 0x3FFF & tmp # en mascara los 14 bits menos significativos
        valor=twos_comp(tmp,14)
        intDatos.append(valor)
    plt.figure(i)
    plt.plot(intDatos[0:500])
    plt.title('Prueba del Modo FreeCounter')
    plt.ylabel('Unidades ADC')
    plt.xlabel('Numero de muestras')
    #plt.stem(intDatos[10:164])
    print("==================================================")
    print(i)
    
```






```python
import time
import matplotlib.pyplot as plt
%matplotlib inline

from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10

TrazaCascada = 0x00
FreeCascada  = 0x10
TrazaCounter = 0x20
FreeCounter  = 0x30
modo = FreeCounter
#modo = TrazaCounter
regset = MMIO(0x41200000, 0xc)
regset.write32(0, modo | 0x08) # 


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


regset = MMIO(0x41200000, 0xc)
#regset.write32(0,0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
#regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
#time.sleep(1)
#regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;

datos = []
for i in range(5):
    datos = []
    regset.write32(0, modo | 0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
    regset.write32(0, modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;   
    #regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
    #regset.write32(0,0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
    dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
    while(dato != 0x10000 ):
        dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
        regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
    
    tmp = regset.read32(0x08)
    dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
    intDatos = []
    while(dato != 0x20000 ):
        regset.write32(0, modo | 0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
        regset.write32(0, modo | 0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
        datos.append(tmp)
        #print(hex(tmp))
        tmp = regset.read32(0x08)
        dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
        tmp = 0x3FFF & tmp # en mascara los 14 bits menos significativos
        valor=twos_comp(tmp,14)
        intDatos.append(valor)
    plt.figure(i)
    plt.plot(intDatos[100:500])
    #plt.stem(intDatos[10:164])
    print("==================================================")
    print(i)
    
```

# Fija el umbral de adquisición


```python
from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10
regset = MMIO(0x41210000, 0xC)
#regset.write32(0,0x210) #    <----------- Valor de umbral, disparo, trigger 0x210 = 528, 0x1FF = 511  0X208=520 0X190=400
regset.write32(0,0x90) #    <----------- Valor de umbral, disparo, trigger 0xBBB = 3000 0x1388 = 5000   0x104 = 260
resolucion = 0.1220703125 #si la escala de voltaje es de +-1 v
#resolucion = 0.06103515625  #si la escala de voltaje es de +1 v
voltaje = int(regset.read32(0x0))*resolucion 
print('en unidades adimensionales tenemos el valor de ')
print(regset.read32(0x0))
print('En escala de voltaje el valor correspondiente es ' + str(voltaje) + str(' mv'))

# el umbral de disparo podemos verlo por los valores maximos o minimos donde se seccionan los 16 puntos en el modo trazacouenter
# en hexadecimal el 260 es 0x104
#276 es 0x114
#290 es 0x122
#368 es 0x170
#400 es 0x190
#65  es 0x41
#96  es 0x60
#128 es 0x80
#80 es 0x50
#(FSVR)el rango de voltaje a escala completa es de +-1v (lv) y +- 20v (hv)
#la resolucion de un ADC se obtiene de la función 
#Resolucion = 1/2^{n}
#resolucion = FSVR/2^{n}
#resolucion = 2000 mv/2 ^{14}= 2000mv/16384 = 0.1220703125 mv

#hay que multiplicar la resolucion*valor de umbral para obtener el equivalente en mv
#el valor de disparo debe estar entre 30mv a 60mv esto es el rango del punto maximo de la señal

```

    en unidades adimensionales tenemos el valor de 
    144
    En escala de voltaje el valor correspondiente es 17.578125 mv



```python
import time
import matplotlib.pyplot as plt
import pandas as pd
%matplotlib inline
import numpy as np
from scipy.stats import norm
import statistics

from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10

TrazaCascada = 0x00
FreeCascada  = 0x10
TrazaCounter = 0x20
FreeCounter  = 0x30
#modo = TrazaCounter
modo = TrazaCascada
#modo = FreeCounter
#modo = FreeCascada
regset = MMIO(0x41200000, 0xc)
regset.write32(0, modo | 0x08) # 

#definimos el nombre del archivo
#nombre_archivo = "toma_32muestras_detector_silicio4.csv"

#definimos la cantidad de columnas que se van a almacenar

#crear un dataframe vacio para almacenar los datos
df = pd.DataFrame()

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


regset = MMIO(0x41200000, 0xc)
#regset.write32(0,0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
#regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
#time.sleep(1)
#regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;

datos = []

i=0
while True:
    datos = []
    regset.write32(0, modo | 0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
    regset.write32(0, modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;   
    #regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
    #regset.write32(0,0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
    dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
    while(dato != 0x10000 ):
        dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
        regset.write32(0,modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
    
    tmp = regset.read32(0x08)
    dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
    intDatos = []   
    while(dato != 0x20000 ):
        regset.write32(0, modo | 0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
        regset.write32(0, modo | 0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
        datos.append(tmp)
        #print(hex(tmp))
        tmp = regset.read32(0x08)
        dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
        tmp = 0x3FFF & tmp # en mascara los 14 bits menos significativos
        valor=twos_comp(tmp,14)
        intDatos.append(valor)
    
    #almacenar los datos de redpitaya en un archivo csv para lecturas externas en redpitaya
    df_datos =pd.DataFrame(intDatos)
    timestamp=int(time.time())
    df_datos.to_csv('datos_SiPM_64muestras_while_continuo_{}.csv'.format(timestamp), header=False, index=False)
    #i=+1
    
    
    #En este espacio estamos calculando la linea base del ruido, para ello e calcula la media, la desviacion estandar del 
    #corrimiento de datos
    std = np.std(intDatos[:])
    mu = np.mean(intDatos[:])
    
    print("================")
    



    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-3-84ffd1b255df> in <module>()
         55     dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
         56     while(dato != 0x10000 ):
    ---> 57         dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
         58         regset.write32(0,modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
         59 


    /usr/local/lib/python3.5/dist-packages/periphery/mmio.py in read32(self, offset)
         98 
         99         offset = self._adjust_offset(offset)
    --> 100         self._validate_offset(offset, 4)
        101         return struct.unpack("=L", self.mapping[offset:offset+4])[0]
        102 


    /usr/local/lib/python3.5/dist-packages/periphery/mmio.py in _validate_offset(self, offset, length)
         75         return offset + (self._physaddr - self._aligned_physaddr)
         76 
    ---> 77     def _validate_offset(self, offset, length):
         78         if (offset+length) > self._aligned_size:
         79             raise ValueError("Offset out of bounds.")


    KeyboardInterrupt: 


### segmento de codigo de las graficas
### la toma de datos empezo 2:08 pm /2/junio/viernes/2022

### la toma de datos termino a las 11:22 am /5/junio/lunes/2022


```python
   
     #Los datos deben superar el valor del ruido 
    linea_base = mu + 2*std
    #impresion de valor de la media
    print("La media de la señal de ruido es:", mu)
    #impresion de valor de la media
    print("La desviación estándar de la señal es:", std)
    # Imprimir la línea base del ruido
    print("el umbral debe superar el valor del ruido con valor de :", linea_base)
   
    #############################################################################
     #presentacion de graficas plot, stem y el histograma de valores
    plt.figure(i)
  
    fig1,(ax1,ax2) = plt.subplots(1,2,figsize=(15,5))
    ax1.plot(intDatos[:], color = 'g')
    #ax1.set_ylim(20,100)
    ax1.grid(True)
    ax1.set_xlabel('Numero de datos')
    ax1.set_ylabel('Unidades ADC')
    ax1.set_title('Perfiles de pulsos a 64 datos muestrasles')
    #ax2.plot(df[220:255],color ='purple')
    ax2.stem(intDatos[:],linefmt = 'g-',markerfmt = 'ko')
    #ax2.hist(intDatos[:], bins =16 )
    ax2.grid(True)
    #ax2.set_ylim(,)
    ax2.set_xlabel('Numero de datos')
    ax2.set_ylabel('Unidades ADC')
    ax2.set_title('Valores Discretos a 64 muestras')

    plt.show()
    print("==================================================")
    print(i)
```

# este es es un ejemplo de como graficar el fenomeno de distintas formas 


```python
import time
import matplotlib.pyplot as plt
import pandas as pd
%matplotlib inline
import numpy as np
from scipy.stats import norm

from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10

TrazaCascada = 0x00
FreeCascada  = 0x10
TrazaCounter = 0x20
FreeCounter  = 0x30
#modo = TrazaCounter
#modo = TrazaCascada
#modo = FreeCounter
modo = FreeCascada
regset = MMIO(0x41200000, 0xc)
regset.write32(0, modo | 0x08) # 


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


regset = MMIO(0x41200000, 0xc)
#regset.write32(0,0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
#regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
#time.sleep(1)
#regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;

datos = []
for i in range(5):
    datos = []
    regset.write32(0, modo | 0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
    regset.write32(0, modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;   
    #regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
    #regset.write32(0,0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
    dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
    while(dato != 0x10000 ):
        dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
        regset.write32(0,modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
    
    tmp = regset.read32(0x08)
    dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
    intDatos = []
    while(dato != 0x20000 ):
        regset.write32(0, modo | 0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
        regset.write32(0, modo | 0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
        datos.append(tmp)
        #print(hex(tmp))
        tmp = regset.read32(0x08)
        dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
        tmp = 0x3FFF & tmp # en mascara los 14 bits menos significativos
        valor=twos_comp(tmp,14)
        intDatos.append(valor)
    #almacenar los datos de redpitaya en un archivo csv para lecturas externas en redpitaya
    df_datos =pd.DataFrame(intDatos)
    df_datos.to_csv('datos_ruido_sistema.csv', header=True, index=False)
    #--------------------------
    plt.figure(i)
    fig =plt.figure()
    plt.plot(intDatos[:])
    plt.title('ruido') 
    plt.xlabel('numero de datos')
    plt.ylabel('Unidades Adimensionales')
    #_------------------------------------------
    fig1 = plt.figure()
    plt.hist(intDatos[:],bins=20)
    plt.title('histograma')
    plt.xlabel('numero de datos')
    plt.ylabel('Unidades ADC')
    #---------------------------------------------------------------
    fig2 = plt.figure()
    plt.title('tren de 16 puntos')
    plt.xlabel('numero de datos')
    plt.stem(intDatos[0:100])
    plt.show()
    print("==================================================")
    print(i)
    
```


```python
import time
import matplotlib.pyplot as plt
%matplotlib inline

from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10

TrazaCascada = 0x00
FreeCascada  = 0x10
TrazaCounter = 0x20
FreeCounter  = 0x30
modo = TrazaCounter
#modo = TrazaCascada
#modo = FreeCounter
#modo = FreeCascada

regset = MMIO(0x41200000, 0xc)
regset.write32(0, modo | 0x08) # 


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


regset = MMIO(0x41200000, 0xc)
#regset.write32(0,0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
#regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
#time.sleep(1)
#regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;

datos = []
for i in range(5):
    datos = []
    regset.write32(0, modo | 0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
    regset.write32(0, modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;   
    #regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
    #regset.write32(0,0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
    dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
    while(dato != 0x10000 ):
        dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
        regset.write32(0, modo | 0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
    
    tmp = regset.read32(0x08)
    dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
    intDatos = []
    while(dato != 0x20000 ):
        regset.write32(0, modo | 0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
        regset.write32(0, modo | 0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
        datos.append(tmp)
        #print(hex(tmp))
        tmp = regset.read32(0x08)
        dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
        tmp = 0x3FFF & tmp # en mascara los 14 bits menos significativos
        valor=twos_comp(tmp,14)
        intDatos.append(valor)
    plt.figure(i)
    plt.plot(intDatos[:])
    plt.show()
    #plt.stem(intDatos[10:164])
    print("==================================================")
    print(i)
```


```python
twos_comp(0x100,14)
```

# Hasta acá revisado


```python
import time
import matplotlib.pyplot as plt
%matplotlib inline

from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10
regset = MMIO(0x41200000, 0xc)
regset.write32(0,0x08) # 


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


regset = MMIO(0x41200000, 0xc)
#regset.write32(0,0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
#regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
#time.sleep(1)
#regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;

datos = []
for i in range(5):
    datos = []
    regset.write32(0,0x08) # nrst = 1; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 0;
    regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;   
    #regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
    #regset.write32(0,0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
    dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
    while(dato != 0x10000 ):
        dato = 0x10000 & regset.read32(0x08) # en mascara los 14 bits menos significativos
        regset.write32(0,0x01) # nrst = 0; cntrl_clk = 0; rd_en_out = 0; wr_en_out = 1;
    
    tmp = regset.read32(0x08)
    dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
    intDatos = []
    while(dato != 0x20000 ):
        regset.write32(0,0x02) # nrst = 0; cntrl_clk = 0; rd_en_out = 1; wr_en_out = 0;
        regset.write32(0,0x06) # nrst = 0; cntrl_clk = 1; rd_en_out = 1; wr_en_out = 0;
        datos.append(tmp)
        #print(hex(tmp))
        tmp = regset.read32(0x08)
        dato = 0x20000 & tmp # en mascara los 14 bits menos significativos
        tmp = 0x3FFF & tmp # en mascara los 14 bits menos significativos
        valor=twos_comp(tmp,14)
        intDatos.append(valor)
    plt.figure(i)
    plt.plot(intDatos[128:256])
    plt.stem(intDatos[128:256])
    print("==================================================")
    print(i)
    
```


```python
import time

import matplotlib.pyplot as plt
%matplotlib inline

plt.plot(intDatos[1:640])
plt.stem(intDatos[1:640])
```


```python
import time
import matplotlib.pyplot as plt
%matplotlib inline
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

intDatos = []
for i in range(len(datos)):
    valor=twos_comp(datos[i],14)
    intDatos.append(valor)
plt.plot(intDatos[1:90])
plt.stem(intDatos[1:90])
plt.title("Señal de prueba a 10MHz (100 ns)")

```


```python
import time
regset = MMIO(0x41200000, 0xc)
#regset.write32(0,0x08) # reset
#regset.write32(0,0x01) # wr_en = 1
regset.write32(0,0x08) # reset
regset.write32(0,0x01) # wr_en = 1
time.sleep(2)
regset.write32(0,0x02) # rd_en = 1

datos = []
for i in range(8192):
    regset.write32(0,0x02)# rd_en = 1
    regset.write32(0,0x06)# cntrl_clk rd_en = 1
    dato = 0x3FFF & regset.read32(0x08)
    datos.append(dato)
    print(hex(dato))
```


```python
import time
import matplotlib.pyplot as plt
%matplotlib inline
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

intDatos = []
for i in range(len(datos)):
    valor=twos_comp(datos[i],14)
    intDatos.append(valor/8192)
plt.plot(intDatos)
plt.stem(intDatos)
plt.title("Señal de prueba a 10MHz (100 ns)")
```


```python
plt.plot(intDatos[128:512])
plt.stem(intDatos[128:512])
plt.title("Señal de prueba a 10MHz (100 ns)")
```


```python
datos[0]
```


```python
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val 

for i in range(16):
    intDecimal = twos_comp(i, 4)
    print('{} {}'.format(i,intDecimal) )

```


```python
import time
regset = MMIO(0x41200000, 0xc)
regset.write32(0,0x01) # wr_en = 1
regset.write32(0,0x09) # nrst = 1
regset.write32(0,0x01) # wr_en = 1
time.sleep(1)

for i in range(20):
    regset.write32(0,0x02)# rd_en = 1
    regset.write32(0,0x06)# cntrl_clk rd_en = 1
    print(hex(regset.read32(0x08)))


```


```python
import time
regset = MMIO(0x41200000, 0xc)
regset.write32(0,0x09) # nrst = 1
regset.write32(0,0x01) # wr_en = 1
regset.write32(0,0x09) # nrst = 1
regset.write32(0,0x01) # wr_en = 1
#time.sleep(1)
datos=[]
for i in range(100):
    #print(regsetAXI_CONTROL.read32(0x08))
    regset.write32(0,0x02)# rd_en = 1
    regset.write32(0,0x06)# cntrl_clk rd_en = 1
    print(hex(regset.read32(0x08)))



```


```python
import time

regsetAXI_CONTROL = MMIO(0x42000000, 0xc)
regsetAXI_CONTROL.write32(0,0x02) # SCLR counter
regsetAXI_CONTROL.write32(0,0x01) # ENA counter

regset = MMIO(0x41200000, 0xc)
regset.write32(0,0x01) # wr_en = 1
regset.write32(0,0x09) # nrst = 1
regset.write32(0,0x01) # wr_en = 1
time.sleep(1)

for i in range(20):
    regset.write32(0,0x02)# rd_en = 1
    regset.write32(0,0x06)# cntrl_clk rd_en = 1
    print(hex(0x3FFF & regset.read32(0x08)))
    
    
```


```python
import time
import matplotlib.pyplot as plt
%matplotlib inline

regsetAXI_CONTROL = MMIO(0x42000000, 0xc)
regsetAXI_CONTROL.write32(0,0x02) # SCLR counter
regsetAXI_CONTROL.write32(0,0x01) # ENA counter

regset = MMIO(0x41200000, 0xc)
regset.write32(0,0x01) # wr_en = 1
regset.write32(0,0x09) # nrst = 1
regset.write32(0,0x01) # wr_en = 1

while( not(regset.read32(0x08) & 0x010000) == 0x010000): # wait full == 1
    break

i = 0
datos=[]
while( not(regset.read32(0x08) & 0x020000) == 0x020000): # wait empty == 1
    regset.write32(0,0x02)# rd_en = 1
    regset.write32(0,0x06)# cntrl_clk rd_en = 1
    i += 1
    datos.append(0xFFFF & regset.read32(0x08))
    #print(hex(0xFFFF & regset.read32(0x08)))
plt.plot(datos[1:128])
#print("= = = = = =  = =")
#print(i)
```


```python
plt.plot(datos[1:128])

```


```python
#name = 'Niroshan'
#age  = 25;
#print(f"Hello I'm {name} and {age} years young")
```

# Toma de datos con el generador de pulso Aligent 81101A

# proyecto vidado localizado en D:\redpitaya\tmp\3_stopwatch_modif\readFIFO_ADC
# archivo bitstream readfifo_adc3.bit, localizado en /root/RedPitaya
## ejecutar antes de probar el código python
## cat readfifo_adc3.bit > /dev/xdevcfg


```python
# MMIO = Memory-mapped I/O(Input/Output) 
# MMIO almacena una dirección en un  espacio fisico dentro de la memoria ram, ademas la memoria y los registros 
#obtenidos por (I/O) son mapeados o asociados a valores de direccion

# dependiendo de la dirección se dara la orden de escribir o leer, esta seleccion dependera de la dirección que tenga como entrada 
# cuando accedemos a la dirección 4120 0000 estamos accediendo al axi de control 
# cuando accedemos a la dirección 4200 0000 estamos accediendo al axi de gencount
# con el comando write32 
from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10

regset = MMIO(0x41200000, 0xc)

regset.write32(0,0x08) # reset Observar que responda la tarjeta
```


```python
# Adquiere un par de datos
import time
regset = MMIO(0x41200000, 0xc)
regset.write32(0,0x08) # reset
regset.write32(0,0x01) # wr_en = 1
time.sleep(1)
regset.write32(0,0x02) # rd_en = 1

datos = []
for i in range(100):
    regset.write32(0,0x02)# rd_en = 1
    regset.write32(0,0x06)# cntrl_clk rd_en = 1
    dato = 0x3FFF & regset.read32(0x08)
    datos.append(dato)
    print(hex(dato))

```


```python
import matplotlib.pyplot as plt

# Generar algunos datos de ejemplo
x = [i for i in range(100)]
y = [i ** 2 for i in range(100)]

# Crear el gráfico
fig, ax = plt.subplots()
ax.plot(x, y)

# Habilitar la herramienta de zoom
ax.set_title('Haz zoom en el gráfico')
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_xlim([0, 100])
ax.set_ylim([0, 10000])
ax.set_autoscale_on(False)  # desactivar el escalado automático para que el zoom sea más preciso
ax.grid(True)
ax.set_axisbelow(True)
zoom = plt.axes([0.2, 0.5, 0.25, 0.25])  # crear un nuevo eje para la herramienta de zoom
axzoom = plt.axes()  # crear otro eje para almacenar el área de zoom

# Agregar la herramienta de zoom al gráfico
zoom_button = plt.widgets.Button(zoom, '+')
def zoom_in(event):
    axzoom.set_xlim([20, 40])
    axzoom.set_ylim([500, 2000])
zoom_button.on_clicked(zoom_in)

# Mostrar el gráfico
plt.show()
```

# Pruebas de código


```python
import time
import matplotlib.pyplot as plt
%matplotlib inline
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


```


```python
import time
import matplotlib.pyplot as plt
data=[]
data1=[]
for i in range(16):
    val = twos_comp(twos_comp(i, 4),4)
    val1 = twos_comp(i,4)
    data.append(val)
    data1.append(val1)
plt.plot(data)
plt.plot(data1)
```


```python
a=twos_comp(-3,4)
b=twos_comp(-2,4)

if a > b :
    print('a es mayor')
else:
    print('b es mayor')
```

# Fija el umbral de adquisición

|    Base Address      |    AXI         ||   Size   |
|----------------------|----------------||----------|
|   ``0x4120_0000``    | AXI_control    || ``64K``  |
|   ``0x4200_0000``    | AXI_gencontrol || ``4K``   |
|   ``0x4121_0000``    | AXI_umbral     || ``64K``  |


```python
from enum import Enum
import numpy as np
import json
import os
#from pynq import DefaultIP
#from pynq.ps import CPU_ARCH, ZU_ARCH
import struct

def _float2int(value: float) -> int:
    """Pack a single precision floating point into a 32-bit integer"""
    return int.from_bytes(struct.pack('f', np.single(value)), 'little')

```


```python
hex(_float2int(-1.0))
```


```python
hex(_float2int(1.0))
```


```python
from periphery import MMIO
import numpy as np
ADDRESS_RANGE = 0x10
ADDRESS_OFFSET = 0x10
regset = MMIO(0x41210000, ADDRESS_RANGE)
regset.write32(0,0xFFFF) # 
regset.write32(1,0x3f80) # 

print(regset.read32(0x0000))
print(regset.read32(0x0001))

```


```python
variable = -1.0
direccion=hex(id(variable))
print(direccion)
map(direccion)

```


```python
from periphery import MMIO
import numpy as np
IP_BASE_ADDRESS = 0x41210000
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x04

mmio = MMIO(IP_BASE_ADDRESS, ADDRESS_RANGE)

data = 0xABCD1234
mmio.write32(ADDRESS_OFFSET, data)
for i in range(0x10):
    #result = mmio.read32(ADDRESS_OFFSET)
    #print(hex(result))
    result = mmio.read32(i)
    print(hex(result))

```