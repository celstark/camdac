from camilladsp import CamillaClient
import sys

'''
Simple program to read the current configuration and save it in several formats.
Pass in a name prefix and it'll save the prefix_full.yml, prefix_full.json
and it'll print Equalizer APO style filter-format. 
'''

# Connect to Camilla
port=1234
try:
    cdsp = CamillaClient("127.0.0.1",port)
    cdsp.connect()
except:
    print("Issue connecting to CamillaDSP")
    sys.exit()
    
prefix='RunningConfig'
if len(sys.argv) > 1:
    prefix = sys.argv[1]
    
config_raw=cdsp.config.active_raw()
with open(f'{prefix}_full.yml','w') as file:
    file.write(config_raw)

config_json=cdsp.config.active_json()
with open(f'{prefix}_full.json','w') as file:
    file.write(config_json)

config=cdsp.config.active()
n=0
for filt in config['filters']:
    if config['filters'][filt]['type'] == 'Biquad':
        n+=1
        if config['filters'][filt]['parameters']['type']=='Peaking':
            type='PK'
        elif config['filters'][filt]['parameters']['type']=='Lowshelf':
            type='LS'
        elif config['filters'][filt]['parameters']['type']=='Highshelf':
            type='HS'    
        else:
            pass
        freq=config['filters'][filt]['parameters']['freq']
        gain=config['filters'][filt]['parameters']['gain']
        q=config['filters'][filt]['parameters']['q']
        s=f'Filter {n}: ON {type} Fc {freq:.0f} Hz Gain {gain} dB Q {q}'
        print(s)
        
        
        
        
    


