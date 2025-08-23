from time import sleep
import RPi_I2C_driver
import threading

bl_timer = None

def disable_bl():
    global bl_status
    if bl_status:
        lcd.backlight(0)
        bl_status=0

def enable_bl():
    global bl_timer, bl_status
    try:  
        bl_timer.cancel()
    except:
        pass # We don't actually care if this fails
    if not bl_status:
        lcd.backlight(1)
    bl_timer = threading.Timer(1.0,disable_bl)
    bl_timer.start()
    bl_status=1
        
frq=440
q=2.0
db=3.5
pot=1
frq_active=False
q_active=False
db_active=True
symbol_act=chr(126)
bl_status=1

TL=f"{pot} {frq:5} {db:+1.1f} {q:3.1f}"
BL=f"    {symbol_act if frq_active else ' '}Hz  {symbol_act if db_active else ' '}dB  {symbol_act if q_active else ' '}Q "

print('Show the display - should turn off after a sec')
enable_bl()
lcd = RPi_I2C_driver.lcd()
lcd.lcd_clear()
lcd.lcd_display_string(TL, 1)
lcd.lcd_display_string(BL, 2)
sleep(2)

print('Fake some updates and handle the backlight timer')
db_active=False
q_active=False
frq_active=True
enable_bl()
for i in range(10):
    enable_bl()
    frq=i*1000+500
    TL=f"{pot} {frq:5} {db:+1.1f} {q:3.1f}"
    BL=f"    {symbol_act if frq_active else ' '}Hz  {symbol_act if db_active else ' '}dB  {symbol_act if q_active else ' '}Q "
    lcd.lcd_display_string(TL, 1)
    lcd.lcd_display_string(BL, 2)
    enable_bl()
    sleep(0.2)


sleep(2)


db_active=True
q_active=False
frq_active=False
for i in range(10):
    db=i*0.5 - 2.0
    TL=f"{pot} {frq:5} {db:+1.1f} {q:3.1f}"
    BL=f"    {symbol_act if frq_active else ' '}Hz  {symbol_act if db_active else ' '}dB  {symbol_act if q_active else ' '}Q "
    lcd.lcd_display_string(TL, 1)
    lcd.lcd_display_string(BL, 2)
    enable_bl()
    sleep(0.1)

sleep(2)    
db_active=False
q_active=True
frq_active=False
for i in range(10):
    q=i*0.5 + 0.5
    TL=f"{pot} {frq:5} {db:+1.1f} {q:3.1f}"
    BL=f"    {symbol_act if frq_active else ' '}Hz  {symbol_act if db_active else ' '}dB  {symbol_act if q_active else ' '}Q "
    lcd.lcd_display_string(TL, 1)
    lcd.lcd_display_string(BL, 2)
    enable_bl()
    sleep(0.1)
    
sleep(2)
