#!/usr/bin/env python3
import serial, time, datetime

def write_file(f_name='error.txt', msg='you didn\'t pass any arguments to write_file'): #error function
	with open('/home/pi/Pilog2020/' + f_name, 'a') as f:
		f.write(msg)

class Sensor:
	def __init__(self, port='/dev/ttyUSB0', baudrate='9600', timeout=5, wait_for=10): #port currently set for raspberry pi
		self.port = port
		self.baudrate = baudrate
		self.timeout = timeout
		self.wait_for = wait_for
	def connect(self, wait_for=5):
		self.wait_for = wait_for
		end_at = time.time() + self.wait_for
		failed_connection = True
		while time.time() <= end_at:
		    try:
		        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
		        self.ser.flushInput()
		        failed_connection = False
		        break
		    except Exception as e:
		        failed_connection = True
		        self.e = e
		if failed_connection:
			write_file(f_name='error.txt', msg='{} {} at {}'.format('error in connect:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
			print('wrote to error.txt! error in connect!')
			quit()
		time.sleep(2)
	def disconnect(self, wait_for=5):
		self.wait_for = wait_for
		self.ser.flushInput()
		end_at = time.time() + self.wait_for
		failed_disconnect = True
		while time.time() <= end_at:
			try:
				self.ser.close()
				failed_disconnect = False
				break
			except Exception as e:
				failed_disconnect = True
				self.e = e
		if failed_disconnect:
			write_file(f_name='error.txt', msg='{} {} at {}'.format('error in disconnect:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
			print('wrote to error.txt! error in disconnect!')
			quit()
		time.sleep(2)
	def do_sample(self, data_names=['Conductivity', 'Temperature'], n_samples=6, interval=5, wait_for=10):
		self.n_samples = n_samples
		self.written_samples = 0
		self.wait_for = wait_for
		sensor_data = 'empty!'
		self.e = 'error'
		end_at = time.time() + self.wait_for
		failed_conductivity = True
		while time.time() <= end_at and self.written_samples < self.n_samples:
			while [data_name not in sensor_data for data_name in data_names]:
				try:
					self.ser.flushInput()
					self.ser.write(bytes('do sample','utf-8'))
					self.ser.write(bytes('\r\n','utf-8'))
					self.ser_bytes = self.ser.readline()
					sensor_data = ' '.join(self.ser_bytes.decode('utf-8').strip().split()[-1*(len(data_names)-1)*2-1::2])
					failed_conductivity = False
					break
				except Exception as e:
					failed_conductivity = True
					self.e = e
			if failed_conductivity:
				write_file(f_name='error.txt', msg='{} {} at {}\n'.format('error in do_sample:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
				print('wrote to error.txt! error in get_sample!')
				quit()
			else:
				if len(sensor_data.split()) == len(data_names):
					write_file(f_name='sensor_data.txt', msg='{} {}'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), ' '.join([str(data_point) for data_tuple in list(zip(list(map(lambda x: x + ':', data_names)), sensor_data.split())) for data_point in data_tuple])))
					print(' '.join([str(data_point) for data_tuple in list(zip(list(map(lambda x: x + ':', data_names)), sensor_data.split())) for data_point in data_tuple]))
					self.written_samples += 1
			time.sleep(interval)
		time.sleep(2)


sensor = Sensor(port='/dev/ttyUSB0', baudrate='9600', timeout=5, wait_for=5) #controls whichever sensor is currently plugged in
sensor.connect(wait_for=5)
#Conductivity
sensor.do_sample(data_names=['Conductivity', 'Temperature'], n_samples=6, interval=3, wait_for=40)
#Oxygen
#sensor.do_sample(data_names=['Oxygen', 'Saturation', 'Temperature'], n_samples=6, interval=3, wait_for=40) #will have a different port once other board is created
sensor.disconnect(wait_for=5)