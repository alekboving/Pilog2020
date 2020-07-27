import serial, time, datetime

class Sensor:
    def __init__(self, name='Generic Sensor Class'):
        print('instance of {} created'.format(name))
    def connect(self, port='COM6', baudrate='9600', timeout=5):
        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            self.ser.flushInput()
            return True
        except Exception as e:
            print('failed to connect')
            with open('error.txt', 'a') as f:
                f.write('{} at {}'.format(e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            quit()   
    def disconnect(self):
        try:
            self.ser.close()
            return True
        except Exception as e:
            print('failed to disconnect')
            with open('error.txt', 'a') as f:
                f.write('{} at {}'.format(e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            quit()

class ConductivitySensor(Sensor):
    def do_sample(self, n_samples=6, interval=10):
        for _ in range(n_samples):
            cond_and_temp = ''
            while 'Conductivity:' not in cond_and_temp and 'Temperature:' not in cond_and_temp:
                try:
                    self.ser.write(bytes('do sample','utf-8'))
                    self.ser.write(bytes('\r\n','utf-8'))
                    self.ser_bytes = self.ser.readline()
                    cond_and_temp = ' '.join(self.ser_bytes[:-2].decode('utf-8').strip().split()[-4:]) + '\n'
                except Exception as e:
                    print('failed do_sample')
                    with open('error.txt', 'a') as f:
                        f.write('{} at {}'.format(e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
                    quit()
            with open('cond_and_temp.txt', 'a') as f:
                f.write('{} Conductivity: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), cond_and_temp.split()[1], cond_and_temp.split()[3]))
            time.sleep(interval)

class OxygenSensor(Sensor):
    def other_command(self):
        print('I will do the command for the oxygen sensor')


start_time = time.time() + 10
conductivity = ConductivitySensor('Conductivity Sensor')
conductivity_connected, conductivity_closed = False, False
while not conductivity_connected and time.time() >= start_time:
    conductivity_connected = conductivity.connect(port='/dev/cu.usbserial-1410', baudrate='9600', timeout=5)
    print('tried connecting')
conductivity.do_sample(n_samples=6, interval=10)
while not conductivity_closed and time.time() >= start_time:
    conductivity_closed = conductivity.disconnect()
    print('tried closing')