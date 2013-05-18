from smartcard.System import readers
from smartcard.util import toASCIIString
import array
from subprocess import call
import os

def new_connection():
	r=readers()
	connection = r[0].createConnection()
	connection.connect()
	return connection


def read():
	c = new_connection()
	allData = []
	for i in range (4,15,4):
		SELECT = [0xff, 0xb0, 0x00, i, 0x10]
		data, sw1, sw2 = c.transmit( SELECT )
		allData = allData + data
		if (254 in data):
			break
	return allData
def sendAPDU(APDU):
	c = new_connection()
	c.transmit( APDU )

def buzzerOn():
	APDU = [0xff, 0x00, 0x52, 0xff, 0x00]
	sendAPDU(APDU)
def buzzerOff():
	APDU = [0xff, 0x00, 0x52, 0x00, 0x00]
	sendAPDU(APDU)

def write(data):
	erase()
	c = new_connection()
	data = list(array.array('B',data))
	command = [0xff, 0xd6, 0x00]
	
	for i in range(0,len(data),4):
		page = 4 + i/4
		if(page > 15):
			break
		apdu = []
		apdu[:] = command[:]
		apdu.append(page)
		apdu.append(0x04)
		try:
			apdu.append(data[i])
		except IndexError:
			apdu.append(0)
		try:
			apdu.append(data[i+1])
		except IndexError:
			apdu.append(0)
		try:
			apdu.append(data[i+2])
		except IndexError:
			apdu.append(0)
		try:
			apdu.append(data[i+3])
		except IndexError:
			apdu.append(0)
		c.transmit(apdu)
def erase():
	c = new_connection()
	command = [0xff, 0xd6, 0x00]
	
	for i in range(0,47,4):
		apdu = []
		apdu[:] = command[:]
		apdu.append(4+(i/4))
		apdu.append(0x04)
		apdu.append(0)
		apdu.append(0)
		apdu.append(0)
		apdu.append(0)
		c.transmit(apdu)
def execute():
	raw = dataToAscii(read())
	data = raw.split(";")
	program = data[0]
	params = data[1:]
	eval("nfc_"+program+"(params)")

def nfc_echo(params):
	for param in params:
		print param
def nfc_http(params):
	call(["google-chrome", params[0]])

	
def dataToAscii(data):
	s = []
	for c in data:
		if(c != 0):
			s.append(c)
		
	return toASCIIString(s)

