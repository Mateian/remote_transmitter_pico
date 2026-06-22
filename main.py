from machine import Pin, SPI
from nrf24l01 import NRF24L01
import time

spi = SPI(0, baudrate=4000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(20))
nrf = NRF24L01(spi, Pin(16, Pin.OUT), Pin(17, Pin.OUT), payload_size=8)

nrf.set_channel(76)
nrf.set_power_speed(0x06, 0x00)
nrf.open_tx_pipe(b"TTTTT")

print("Telecomanda RC pornita. Trimite comenzi in continuu...")

butoane = {
    "L": Pin(2, Pin.IN, Pin.PULL_UP),
    "R": Pin(3, Pin.IN, Pin.PULL_UP),
    "F": Pin(4, Pin.IN, Pin.PULL_UP),
    "DROP": Pin(5, Pin.IN, Pin.PULL_UP),
}

def trimite(text):
    payload = text.encode("utf-8")
    payload += b'\x00' * (8 - len(payload))
    
    try:
        nrf.send(payload)
        print("Trimis:", text)
    except:
        pass

drop_sent = False

while True:
    if butoane["DROP"].value() == 0:
        if not drop_sent:
            trimite("DROP")
            drop_sent = True
    else:
        drop_sent = False
    
    for comanda, pin in butoane.items():
        if comanda != "DROP":
            if pin.value() == 0:
                trimite(comanda)
            
    # pauza
    time.sleep_ms(30)
