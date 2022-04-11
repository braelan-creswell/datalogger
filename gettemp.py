#!/usr/bin/python3
import os
import sys
import smbus
import mysql.connector
from datetime import date, datetime

bus = smbus.SMBus(1) #i2c bus 1
i2caddr = 0x4d #i2c address for sensor

# Calculate 2's complement
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

unsignedtemp = bus.read_byte(i2caddr) #read data from sensor

temp = twos_comp(unsignedtemp, 8) #Take twos complement of value to account for negative temperatures

temp = round(temp, 2) #round to 2 decimal place

try:
    cpufile = open("/sys/class/thermal/thermal_zone0/temp", "r") #open core temp file
except:
    print("File Failed to Open")
    quit()

cpu = int(cpufile.read()) #read core temp
cpu = round(cpu/1000, 2) #make core temp readible

try:
    data = mysql.connector.connect(user='datalog', password='diViqIgan1G3', host='127.0.0.1', database='datalogger') #open connection to MySQL
    send = data.cursor()
    timestamp = datetime.now() #take timestamp
    query = ("INSERT INTO temperature (cputemp, roomtemp, timestamp) VALUES (%s, %s, %s)") #build sql query
    querydata = (cpu, temp, timestamp) #variables to insert into sql
    send.execute(query, querydata) #Run query
    data.commit() #ensure data is saved in database
except:
    print("MySQL Error") #handle failure
    quit()

data.close() #disconnect from MySQL

