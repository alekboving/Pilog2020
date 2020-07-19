import serial
from datetime import datetime

try: #checks to see if sensor is connected
    ser = serial.Serial('COM6')
    ser.flushInput()
except:
    print("error sensor not connected")

file = open("Boving_aanderaa.txt","w") #clearing data from previous session
file.close()

while True: #infinite loop until broken manually or error with sensor
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8") #decoding bytes into a readable format
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S") #formatting date and time
        file=open('Boving_aanderaa.txt','a') #opening file
        x = decoded_bytes.split()
        print((x[3],float(x[4]),x[5],float(x[6])))
        file.write('| %19s | %13s %5.4f | %12s %5.3f | \n' % (dt_string,x[3],float(x[4]),x[5],float(x[6])))
    except:
        print("error")
        break
