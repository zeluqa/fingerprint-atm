import pdb # Untuk melakukan debugging
import sys
sys.path.append("./../server")
sys.path.append("./../fingerprint")
sys.path.append("./../smartcard")
sys.path.append("./../server")
sys.path.append("./../display")
sys.path.append("./../input")

import server
import display
import input

KEYPAD_CLEAR = 12
BUTTON_CONFIRM = 1
saved_pin = [1,2,3,4,5,6]

def pin_verify():
	# Melakukan verifikasi PIN, return 1 bila berhasil, 0 bila gagal
	i = 0
	in_key = 0
	in_but = 0
	pin_buffer = [0,0,0,0,0,0]
	
	while (in_but == 0):
		display.pin()
		in_key = input.keypad()
		if (in_key != 0):
			if (in_key == KEYPAD_CLEAR):
				i = 0
			else:
				if(i < 6):
					pin_buffer[i] = in_key
					i += 1
		
		in_but = input.button()
		pdb.set_trace() # Breakpoint untuk debugging
		if(in_but == BUTTON_CONFIRM):
			if(pin_buffer == saved_pin):
				pin_valid = True
			else:
				pin_valid = False
			
			return pin_valid
			
def verify_finger():
	# Melakukan verifikasi sidik jari, return 1 bila berhasil, 0 bila gagal
	display.fingerprint()
	if(fingerprint.verify()):
		success = True
	else:
		success = False
		
	return success
	
def regist_finger():
	# Melakukan proses registrasi sidik jari
	display.regist()
	fingerprint.regist()
	smartcard.write()
	return
	
def main_menu():
	return
	
def check_balance():
	return
	
def withdraw():
	return

pin_verify();