import serial, time, datetime

def write_file(f_name='error.txt', msg='you didn\'t pass any arguments to write_file'):
	with open(f_name, 'a') as f:
		f.write(msg)

class Sensor:
	def __init__(self, port='/dev/ttyUSB0', baudrate='9600', timeout=5, wait_for=10):
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
			write_file(f_name='error.txt', msg='{} {} at {}\n'.format('error in connect:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
			print('wrote to error.txt! error in connect!')
			quit()
		time.sleep(2) #gives time for sensor to boot up if not connecting
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
			write_file(f_name='error.txt', msg='{} {} at {}\n'.format('error in disconnect:',self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
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
					sensor_data = ' '.join(self.ser_bytes.decode('utf-8').strip().split()[-3::2]) + '\n'
					failed_conductivity = False
					break
				except Exception as e:
					failed_conductivity = True
					self.e = e
			if failed_conductivity:
				write_file(f_name='error.txt', msg='{} {} at {}\n'.format('error in do_sample:', self.e, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
				print('wrote to error.txt! error in Conductivity.get_sample!') #can be removed in final version
				quit()
			else:
				if len(sensor_data.split()) == 2:
					write_file(f_name='sensor_data.txt', msg='{} Conductivity: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), sensor_data.split()[0], sensor_data.split()[1]))
					print('{} Conductivity: {} Temperature: {}\n'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), sensor_data.split()[0], sensor_data.split()[1]))
					self.written_samples += 1
			time.sleep(interval)
		time.sleep(2)


sensor = Sensor(port='/dev/ttyUSB0', baudrate='9600', timeout=5, wait_for=5)
sensor.connect(wait_for=5)
#Conductivity
#sensor.do_sample(data_names=['Conductivity', 'Temperature'], n_samples=6, interval=3, wait_for=40) #checks that both data sets are being compiled
#Oxygen
sensor.do_sample(data_names=['Oxygen', 'Saturation', 'Temperature'], n_samples=6, interval=3, wait_for=40)
sensor.disconnect(wait_for=5) #disconnects sensor at end of program
