from pymodbus.client import ModbusTcpClient
import logging
import time

from pm2100json import *
from pm2100read import *

DEBUG=False

#-- PM2100 connection information
# Set the IP address and Port of your Modbus TCP device (PLC, RTU, etc.)
SERVER_HOST = '192.168.1.222'  # Replace with the actual IP address
SERVER_PORT = 502             # Default Modbus TCP port
JSON_FILE_PATH='pm2100mapabridged.json'
DATALOG_FILE_PATH='pm2100datalog.csv'

header_setup=[
'noPhase', 'noWires', 'psConfig', 'nVoltage', 'nCurrent', 'nPDF', 'nPR',
'nVTs', 'VTPrimary', 'VTSecondary', 'nCTs', 'CT1ary', 'CT2ary', 'CT1aryN', 'CT2aryN', 'CTMetering', 'VTMetring', 'VTCType'
]

header_reading=[ 'ts',
'cA', 'cB', 'cC', 'cN', 'cG', 'cAvg', 'cuA', 'cuB', 'cuC', 'cuWorst',
'vAB','vBC','vCA','vAvg','vAN','vBN','vCN','vNAvg','vuAB','vuBC','vuCA','vuAvg','vuAN','vuBN','vuCN','vuNAvg',
'apA','apB','apC','apTotal','rpA','rpB','rpC','rpTotal','appA','appB','appC','appTotal',
'pf32','pfA','pfB','pfC','pfTotal','dpfA','dpfB','dpfC','dpfTotal',
'frequency'
]

def datalogging():
    #-- read json register map ----------------
    rmap = pm2120_registermap(JSON_FILE_PATH)
    if DEBUG :
        noblock=0
        for block in rmap:
            category = block['category']
            address = block['address']
            length = block['length']        #- counts of registers
            num_registers = len(block['registers'])

            print(f"Processing category: {category}")
            print(f"  Start Address: {address}")
            print(f"  Contains {num_registers} register definitions.")
            noreg=0
            for reg in block['registers']:
                print(f"    - Register at {reg['addr']} (Type: {reg['type']})")
                noreg=noreg+1
            print(f"noblock={noblock}, noreg={noreg}")
            noblock=noblock+1

    #-- report the size of register map json -----
    print("total json bock[len(rmap)] ", len(rmap))
    for i in range(len(rmap)):        
        print(f"{i}. {rmap[i]['category']}, ", len(rmap[i]['registers']), " registers")
    
    #===================================================================
    #-- Datalog every 5 minutes
    #-- ts : unix epoch
    #===================================================================
    while True :
        #-- connection retry up to three times
        tryout=3
        while(tryout > 0) :
            client = connect_pm2100(ipaddr=SERVER_HOST, portno=SERVER_PORT)
            if client == None:
                tryout=tryout-1
                time.sleep(1)
            else:
                break

        #-- read holding register --
        strval = read_string(client, addr=29, length=20)
        print(f"Meter Name: {strval}")

        #-- close the Modbus TCP connection
        client.close()
        time.sleep(300) #-- sampling every 5 minutes
    #=====================================================================

if __name__ == "__main__":
    datalogging()