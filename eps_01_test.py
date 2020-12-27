#! /usr/bin/python
'''
ESP8266 WIFI MODULE
'''
import serial
import time
import thread

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=2
)
##########################################################

def print_help():
	print """Enter your command:
		t  - AT command test
		l  - AP list
		c  - connect to AP
		ip - IP address
		s  - start server on port 25 (telnet)
		m  - send a message to connected client
		q  - leave AP
		h  - help, print this list
		exit - leave this app
		"""


def wait_for_answer():
	end=0
	counter=0
	while end==0:
		time.sleep(0.5)
		counter = counter + 1
		l = ser.readlines()
		if len(l)>0:
			for x in l:
				xx = str(x)
				if xx.find("OK")==0:
					end=1
					return 1
				print(x)
		if counter == 10:
			print("\nproblem with connection")
			return 0

##########################################################
inc = 1
ser.open()
print_help()
while 1:
	inc = raw_input(">> ")
	#wyswietlenie helpa
	if inc == 'h':
		print_help()
	#opuszczenie aplikacji
	if inc == 'exit':
		ser.close()
		exit()
	#test AT
	if inc == 't':
		#czasami wymaga cipstart
		ser.write("AT\r\n")
		wait_for_answer()
	#lista ap
	if inc == 'l':
		#czasami wymaga cipstart
		ser.write("AT+CIPSTART\r\n")
		time.sleep(0.5)
		#lista ap
		ser.write("AT+CWLAP\r\n")
		wait_for_answer()
	#podlacz do ap
	if inc == 'c':
		print("\nAP name:")
		n = raw_input("<< ")
		print("\nConnecting to %s"%n)
		#zmiana na tryb klienta
		ser.write("AT+CWMODE=1\r\n")
		wait_for_answer()
		#laczenie z AP
		ser.write("AT+CWJAP=\"%s\",\"\" \r\n"%n)
		wait_for_answer()
	#adres ip
	if inc == 'ip':
		ser.write("AT+CIFSR\r\n")
		time.sleep(0.5)
		wait_for_answer()
		
	#serwer na porcie 80
	if inc == 's':
		print("\nStarting server")
		#tryb wielopolaczeniowy (multiple connections mode)
		ser.write("AT+CIPMUX=1\r\n")
		time.sleep(0.5)
		#wlaczenie (1) nasluchiwania na porcie 80
		ser.write("AT+CIPSERVER=1,80\r\n")
		time.sleep(0.5)
		print("\nIam waiting for connection")
		counter=0
		end =0
		while end==0:
			time.sleep(0.5)
			counter = counter + 1
			l = ser.readlines()
			if len(l)>0:
				for x in l:
					print(x)
			if counter == 10:
				end = 1
				print("\n It was only a test...")
				print("\n Server is still working but isnt printing here.")
	#wysylanie odpowiedzi do klienta
	if inc == 'm':
		ser.write("AT+CIPSEND=0,5\r\n")
		time.sleep(0.5)
		ser.write("hej\r\n")

	#odlaczenie od AP
	if inc == 'q':
		print("\nLeaving AP - bye")
		ser.write("AT+CWQAP\r\n")
