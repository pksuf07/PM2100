from pymodbus.client import ModbusTcpClient
from pm2100json import *
from pm2100datatype import *
import time
import csv

DEBUG=False
header=[
    'ts',
    'cA', 'cB', 'cC', 'cN', 'cG', 'cAvg', 'cuA', 'cuB', 'cuC', 'cuWorst',
    'vAB','vBC', 'vCA', 'vLAvg', 'vAN', 'vBN', 'vCN', 'vNAvg', 'vuAB', 'vuBC', 'vuCA', 'uvLWorst', 'vuAN', 'vuBN', 'vuCN', 'vuNWorst',
    'apA', 'apB', 'apC', 'apTotal', 'rpA', 'rpB', 'rpC', 'rpTotal', 'appA', 'appB', 'appC', 'appTotal',
    'pfA', 'pfB', 'pfC', 'pfTotal', 'dpfA', 'dpfB', 'dpfC', 'dpfTotal', 'freq'
]
#-------------------------------------------------------------------------------
def connect_pm2100(address, portno, tryout=3):
    retry=0
    client = ModbusTcpClient("192.168.1.215")
    while True:
        if client.connect():
            return client
        else:
            if retry <= tryout:
                time.sleep()
                retry=retry+1
            else:
                print(f"Terminating process after {tryout} retry!")
                return None
    
#-------------------------------------------------------------------------------
def read_float32_files(client, address, counts):
    """Read temperature value from Modbus sensor."""
    # Many sensors store float values across 2 registers
    ra = client.read_holding_registers(address=address, count=counts)
    if not ra.isError():
        # Decode the registers as a 32-bit float
        values = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.FLOAT32
        )
        return values 
    return None

#-------------------------------------------------------------------------------
def main():
    #-- read json register map -------------------------------------------------
    registermap=pm2120_registermap("pm2100mapabridged.json")

    #-- log data in csv format -------------------------------------------------
    with open('datalog.csv', 'at', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(header)
    f.close()


    while True :
        #-- connect to power monitor modules -----------------------------------
        client=connect_pm2100('192.168.1.215', portno=502)
        if client==None :
            exit

        #-- read register value from pm2100 ------------------------------------
        regarray=[]
        ts=time.time()      #-- timestamp ---------------------------------
        regarray.append(ts)
        for block in registermap:
            category = block['category']
            address = block['address']
            num_registers = len(block['registers'])

            print(f"Processing category: {category}")
            print(f"  Start Address: {address}")
            print(f"  Contains {num_registers} register definitions.")
        
            values = read_float32_register_files(client, address-1, num_registers*2)
            if type(values) == list :
                regarray = regarray + values
            else:
                regarray.append(values)
            print(values)

            if DEBUG :
                # Iterating over the nested 'registers' list
                for reg in block['registers']:
                    print(f"    - Register at {reg['addr']} (Type: {reg['type']})")

 
        print(regarray)
        #-- log data in csv format -----------------------------------------
        with open('datalog.csv', 'at', newline='') as f:
            writer=csv.writer(f)
            writer.writerow(regarray)
        f.close()
        
        #-- sleep for 5 minutes
        time.sleep(300)


#================================================================================
if __name__ == "__main__":
    main()