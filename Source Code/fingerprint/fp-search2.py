import serial, time, datetime, struct
import sys 

# access serial port on the system; '57600' specifies the baud rate
ser = serial.Serial('/dev/ttyACM0',57600)                          
# global variable which defines header for command packet
pack = [0xef01, 0xffffffff, 0x1]                                   

# function definition
def printx(l):                                                     
	# for loop 'for every 'i' in l'
	for i in l:                                                
		# pring hex equivalent of 'i'
		print hex(i),                                      
	# print space ' '
	print ''                                                   


# function definition
def readPacket():                                                  
	# pause execution for 1 second
	time.sleep(1)                                              
	# Get the number of bytes in the output buffer (integer)
	w = ser.inWaiting()                                        
	# empty array definition 
	ret = []                                                   
	# if condition ;  if length of w is greater than or equal to 9
	if w >= 9:                                                 
		# partial read to get length; read upto 9 bytes and store in 's'
		s = ser.read(9)                                    
		# Extends the ret array by unpacking the 9-byte string's' in the format 'HIBH' and appending it to the array
		ret.extend(struct.unpack('!HIBH', s))              
		# 'ln' holds the last byte/item in the array ret[]
		ln = ret[-1]                                       
		
		# pause execution for 1 second
		time.sleep(1)                                      
		# Get the number of bytes in the output buffer (integer)
		w = ser.inWaiting()                                
		# if condition ;  if length of w is greater than or equal to ln
		if w >= ln:                                        
			# serial read to get length of ln and store in 's'
			s = ser.read(ln)                           
			# data format: 
			form = '!' + 'B' * (ln - 2) + 'H'          
			# Extends the ret array by unpacking the string 's' in the format 'form' and appending it to the array
			ret.extend(struct.unpack(form, s))         
	# returns the array ret[]
	return ret                                                 



# function definition (argument:data);data is variable field in the packet
def writePacket(data):                                             
	# (len(data) gives the length of the data packet; 2 defines the checksum bytes
	pack2 = pack + [(len(data) + 2)]                           
	# concatentaing the last 2 bytes of 'pack2' i.e. checksum bytes and data and storing in variable 'a'
	a = sum(pack2[-2:] + data)                                 
	# string packaging in a compatible format:  to write first 4 common fields to module, we must pack into HIBH format; variable fields depending on particular function, which are converted into byte array ('B' * len(data)); finally a checksum (H)
	pack_str = '!HIBH' + 'B' * len(data) + 'H'                 
	# complete string 
	l = pack2 + data + [a]                                     
	# string packaging of pack_str in the format ' 	
	s = struct.pack(pack_str, *l)                              
	# write packed string 's' to serail port defined
	ser.write(s)                                               

# function definition
def verifyFinger():                                                
        # 0x13 is the instruction code for veryifypwd
        data = [0x13, 0x0, 0, 0, 0]                                
        # writePacket function() called
        writePacket(data)                                          
        # readPacket() function called and the data read is stored in 's'
        s = readPacket()                                           
        # returns 4th byte in the array 's'as return parameter (confirmation code) defined is of 1 byte
        return s[4]                                                

# function definition
def genImg():                                                      
        # 0x1 is the instruction code for genImg
        data = [0x1]                                               
        # writePacket function() called
        writePacket(data)                                          
        # readPacket() function called and the data read is stored in 's'
        s = readPacket()                                           
        # returns 4th byte in the array 's'as return parameter (confirmation code) defined is of 1 byte
        return s[4]                                                

# function definition:generate the character firl from the original image and store in CharBuffer1/CharBuffer2
def img2Tz(buf):                                                   
        # 0x2 is the instruction code for genImg; buf is the BufferID (character file buffer number)
        data = [0x2, buf]                                          
        # writePacket function() called
        writePacket(data)                                          
        # readPacket() function called and the data read is stored in 's'
        s = readPacket()                                           
        # returns 4th byte in the array 's'as return parameter (confirmation code) defined is of 1 byte
        return s[4]                                                

# function definition: search the whole finger library for the template that matches the one in CharBuffer1 or CharBuffer2
def search():                                                      
        # 0x4 is the instruction code for search; 0x1 is the buffer ID; 0X0 0X0 define start page (2 bytes); 0x0 0x5 define end page number (2 bytes)
        data = [0x4, 0x1, 0x0, 0x0, 0x0, 0x5]                      
        # writePacket function() called
        writePacket(data)                                          
        # readPacket() function called and the data read is stored in 's'
        s = readPacket()                                           
        # slices 4 bytes from left and 1 byte from the right in the array 's' and returns the Page Id (2 bytes)
        return s[4:-1]                                             

# function definition:Upload template file to upper computer
def UpChar():                                                   
        # 0x2 is the instruction code for genImg; buf is the BufferID (character file buffer number)
        data = [0x8, 0x2]                                          
        # writePacket function() called
        writePacket(data)                                          
        # readPacket() function called and the data read is stored in 's'
        s = readPacket()                                           
        # returns 4th byte in the array 's'as return parameter (confirmation code) defined is of 1 byte
        return s

if(0):
	# if condition: upon verifyFinger() being called
	if verifyFinger():                                                 
		# prints on terminal
		print 'Verification Error'                                 
		# program stops due to error
		sys.exit(-1)                                               

	# __main__ code
	# prints on terminal
	print 'Put finger',                                                
	# flush buffer to terminal before sleep
	sys.stdout.flush()                                                 

	# pause execution for 1 second
	time.sleep(1)	                                                   
	# Try getting fingerprint 5 times before giving up
	for _ in range(5):                                                 
		# genImg() function called and the value returned is stored in 'g'
		g = genImg()                                               
		# if successfull in getting finger then break
		if g == 0:                                                 
			# execution breaks
			break                                              
		#time.sleep(1)                          
		

		# show progress
		print '.',                                                 
		# forces it to "flush" the buffer, meaning that it will write everything in the buffer to the terminal
		sys.stdout.flush()                                         

	# newline
	print ''                                                           
	# forces it to "flush" the buffer, meaning that it will write everything in the buffer to the terminal
	sys.stdout.flush()                                                 
	# did not get any fingerprint, exit
	if g != 0:                                                         
		# program stops due to error                           
		sys.exit(-1)                                               

	# img2Tz returns 0 on success. exit on failure
	if img2Tz(1):                                                      
		# prints on terminal
		print 'Conversion Error'                                   
		# program stops due to error 
		sys.exit(-1)                                               

	# search for obtained fingerprint in stored templates
	r = search()                                                       
											
	# search was successfull and template score between 0 and 1
	if r[0] == 0 and r[2] in [0,1]:                                    
		#exit codes were used in fingerprint based login on my ubuntu machine

		sys.exit(0)
	sys.exit(1)
else:
	print '[{}]'.format(', '.join(hex(x) for x in UpChar()))
	print '[{}]'.format(', '.join(hex(x) for x in readPacket()))
	
