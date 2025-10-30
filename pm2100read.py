from pymodbus.client import ModbusTcpClient
import sys, struct
from datetime import datetime

#-- Data Types of pymodbus
# INT16, UINT16, INT32, UINT32, INT64, UINT64, FLOAT32, FLOAT64, STRING, BITS
DEBUG=False

#-----------------------------------------------------------------
def read_string(client, addr=29, length=20):
    """Read temperature value from Modbus sensor."""
    # Many sensors store float values across 2 registers
    ra = client.read_holding_registers(address=addr, count=length)
    
    if not ra.isError():
        # Decode the registers as a 64-bit integer
        strval = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.STRING
        )
        return strval
    return None

#-----------------------------------------------------------------
# IEC 60870-5 Standard
def read_datetime(client, addr):
    """Read temperature value from Modbus sensor."""
    # Many sensors store float values across 2 registers
    ra = client.read_holding_registers(address=addr, count=4)

    if not ra.isError():
        year_pack=struct.pack('>H', ra.registers[0])
        year_unpack=struct.unpack('>H', year_pack)[0]
        year= (year_unpack & 0x003F) + 2000

        monthday_pack = struct.pack('>H', ra.registers[1])
        monthday_unpack=struct.unpack('>H', monthday_pack)[0]
        day=monthday_unpack & 0x001F    # 0b0000 0000 0001 1111
        month=(monthday_unpack & 0x0F00) >> 8  # 0b0000 1111 0000 0000

        hoursmin_pack=struct.pack('>H', ra.registers[2])
        hoursmin_unpack = struct.unpack('>H', hoursmin_pack)[0]
        minutes=hoursmin_unpack & 0x001F
        hours=(hoursmin_unpack & 0x1F00) >> 8

        msecs_pack=struct.pack('>H', ra.registers[3])
        msecs_unpack = struct.unpack('>H', msecs_pack)[0]
        milliseconds=msecs_unpack
        seconds = int(milliseconds / 1000000)
        # milliseconds = milliseconds - seconds * 1000000

        # datetimelist=[year,month,day,hours, minutes,seconds, milliseconds]
        dt = datetime(year, month, day,hours, minutes, seconds)
        # return datetimelist
        return dt
    return None

#-----------------------------------------------------------------
def read_register_int16(client, addr):
    ra = client.read_holding_registers(address=addr, count=1)
    
    if not ra.isError():
        # Decode the registers as a 16-bit integer
        int16val = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.INT16
        )
        return int16val
    return None

#-----------------------------------------------------------------
def read_register_uint16(client, addr):
    ra = client.read_holding_registers(address=addr, count=1)
    
    if not ra.isError():
        # Decode the registers as a 16-bit unsigned integer
        uint16val = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.UINT16
        )
        return uint16val
    return None

#-----------------------------------------------------------------
def read_register_int32(client, addr):
    ra = client.read_holding_registers(address=addr, count=2)
    
    if not ra.isError():
        # Decode the registers as a 32-bit integer
        int32val = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.INT32
        )
        return int32val
    return None

#-----------------------------------------------------------------
def read_register_uint32(client, addr):
    ra = client.read_holding_registers(address=addr, count=2)
    
    if not ra.isError():
        # Decode the registers as a 32-bit unsigned integer
        uint32val = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.UINT32
        )
        return uint32val
    return None

#-----------------------------------------------------------------
def read_register_int64(client, addr):
    ra = client.read_holding_registers(address=addr, count=4)
    
    if not ra.isError():
        # Decode the registers as a 64-bit integer
        int64val = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.INT64
        )
        return int64val
    return None

def read_registers_int64(client, addr, counts):
    ra = client.read_holding_registers(address=addr, count=4*counts)
    
    if not ra.isError():
        # Decode the registers as 64-bit integer
        int64vals = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.INT64
        )
        return int64vals
    return None

#-----------------------------------------------------------------
def read_register_uint64(client, addr):
    ra = client.read_holding_registers(address=addr, count=4)
    
    if not ra.isError():
        # Decode the registers as a 64-bit unsigned integer
        uint64val = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.UINT64
        )
        return uint64val
    return None

#-----------------------------------------------------------------
def read_register_float32(client, addr):
    ra = client.read_holding_registers(address=addr, count=2)
    
    if not ra.isError():
        # Decode the registers as a 32-bit float
        float32val = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.FLOAT32
        )
        return float32val
    return None

def read_registers_float32(client, addr, counts):
    ra = client.read_holding_registers(address=addr, count=2*counts)
    if not ra.isError():
        # Decode the registers as 32-bit float
        float32vals = client.convert_from_registers(
                registers=ra.registers,
                data_type =client.DATATYPE.FLOAT32
        )
        return float32vals
    
    return None

#-----------------------------------------------------------------
def read_register_float64(client, addr):
    ra = client.read_holding_registers(address=addr, count=4)
    
    if not ra.isError():
        # Decode the registers as a 64-bit float
        float64val = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.FLOAT64
        )
        return float64val
    return None

def read_registers_float64(client, addr, counts):
    ra = client.read_holding_registers(address=addr, count=4*counts)
    
    if not ra.isError():
        # Decode the registers as a 64-bit float
        float64vals = client.convert_from_registers(
            registers=ra.registers,
            data_type =client.DATATYPE.FLOAT64
        )
        return float64vals
    return None

#==================================================================
def connect_pm2100(ipaddr, portno) :
    client = ModbusTcpClient(ipaddr)
    if not client.connect():
        print("ERROR: Could not connect to the Modbus TCP server.")
        return None
    else:
        print("Connection established successfully.")
        return client
#==================================================================

#------------------------------------------------------------------
if DEBUG :
    client = connect_pm2100(ipaddr='192.168.1.222', portno=502)
    if client == None:
        exit

    strval = read_string(client, addr=29, length=20)
    print(f"Meter Name: {strval}")

    strval = read_string(client, addr=49, length=20)
    print(f"Meter Model: {strval}")

    strval = read_string(client, addr=69, length=20)
    print(f"Manufacturer: {strval}")

    float32val = read_register_float32(client, addr=2017)
    print(f"Nominal Voltage: {float32val}V")

    float32vals = read_registers_float32(client, addr=2999, counts=10)
    print(f"Current: {float32vals}")

    float32vals = read_registers_float32(client, addr=3019, counts=16)
    print(f"Voltage: {float32vals}")

    int64vals = read_registers_int64(client, addr=3303, counts=12)
    print(f"Accumulated Energy Permanent : {int64vals}")

    datetimelist = read_datetime(client, addr=131)
    print(f"Date of Manufacture : {datetimelist}")

    client.close()