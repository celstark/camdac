from time import sleep
import RPi_I2C_driver


frq=440
q=2.0
db=3.5
pot=1
frq_active=False
q_active=False
db_active=True
symbol_act=chr(126)

TL=f"{pot} {frq:5} {db:+1.1f} {q:3.1f}"
BL=f"    {symbol_act if frq_active else ' '}Hz  {symbol_act if db_active else ' '}dB  {symbol_act if q_active else ' '}Q "
print(TL)
print(BL)

mylcd = RPi_I2C_driver.lcd()
mylcd.lcd_clear()
mylcd.lcd_display_string(TL, 1)
mylcd.lcd_display_string(BL, 2)
sleep(1)

db_active=False
q_active=False
frq_active=True
for i in range(10):
    frq=i*1000+500
    TL=f"{pot} {frq:5} {db:+1.1f} {q:3.1f}"
    BL=f"    {symbol_act if frq_active else ' '}Hz  {symbol_act if db_active else ' '}dB  {symbol_act if q_active else ' '}Q "
    mylcd.lcd_display_string(TL, 1)
    mylcd.lcd_display_string(BL, 2)
    sleep(0.1)

sleep(1)  
mylcd.backlight(0)
sleep(1)
mylcd.backlight(1)  
db_active=True
q_active=False
frq_active=False
for i in range(10):
    db=i*0.5 - 2.0
    TL=f"{pot} {frq:5} {db:+1.1f} {q:3.1f}"
    BL=f"    {symbol_act if frq_active else ' '}Hz  {symbol_act if db_active else ' '}dB  {symbol_act if q_active else ' '}Q "
    mylcd.lcd_display_string(TL, 1)
    mylcd.lcd_display_string(BL, 2)
    sleep(0.1)

sleep(1)    
db_active=False
q_active=True
frq_active=False
for i in range(10):
    q=i*0.5 + 0.5
    TL=f"{pot} {frq:5} {db:+1.1f} {q:3.1f}"
    BL=f"    {symbol_act if frq_active else ' '}Hz  {symbol_act if db_active else ' '}dB  {symbol_act if q_active else ' '}Q "
    mylcd.lcd_display_string(TL, 1)
    mylcd.lcd_display_string(BL, 2)
    sleep(0.1)
    
sleep(2)
mylcd.backlight(0)