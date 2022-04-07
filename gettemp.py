#!/usr/bin/python
import os
import sys
import mysql.connector
from datetime import date, datetime

# Calculate 2's complement
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

cmd = "i2cget -y 1 0x4d 0 b" #command for getting data from sensor

x = os.popen(cmd) #run command and save output to x

unsignedtemp = int(x.read(), 16) #change popen data to readable hex value

temp = twos_comp(unsignedtemp, 8) #Take twos complement of value to account for negative temperatures

temp = round(temp, 2)

try:
    cpufile = open("/sys/class/thermal/thermal_zone0/temp", "r") #open core temp file
except:
    print("File Failed to Open")
    quit()

cpu = int(cpufile.read()) #read core temp
cpu = round(cpu/1000, 2) #make core temp readible

try:
    data = mysql.connector.connect(user='datalog', password='diViqIgan1G3', host='127.0.0.1', database='datalogger')
    send = data.cursor()
    timestamp = datetime.now()
    query = ("INSERT INTO temperature (cputemp, roomtemp, timestamp) VALUES (%s, %s, %s)")
    querydata = (cpu, temp, timestamp)
    send.execute(query, querydata)
    data.commit()
except:
    print("MySQL Error")
    quit()

data.close()