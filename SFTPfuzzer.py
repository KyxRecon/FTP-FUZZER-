#Simple FTP Fuzzer written in Python (Gattorete@Home)
#Author: KYXRECON

import sys
import socket
import getopt

#Initial variables
evil_buffer = ["A"] 
fuzz_len = 0
fuzzUser = False;
fuzzPass = False;
host = "127.0.0.1"
port = 21

#Show a very cool banner on startup (no cats this time)
def banner():
	print
	print "***************************************************************"
	print "SIMPLE FTP FUZZER "
	print "Find out buffer owerflows in username and password field (FTP)"
	print "Author : 0x8b30cc (Gattorete@Home)"
	print "Licensed under GNU GENERAL PUBLIC LICENSE (GPLv3) "
	print "Version 1.0"
	print "***************************************************************"
	print
	print "Usage: SFTPfuzzer.py  -t <target>  -p <port>"
	print	

#Fill buffer with "A"*fuzz_len
def fillList(fuzz_len):
	i=1
	while (i<=fuzz_len):
		evil_buffer.append("A")		
		i = i+1	

#Fuzz the username field with the evil buffer 
def fuzzUsername(host , port):
	print "[INFO] Fuzzing username field"	
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		connect = s.connect((host,port))
		output = s.recv(1024)
		print "<< " + output
		print "[INFO] Sending evil buffer:  [AAAAAA...]"
		s.send("USER " + "".join(evil_buffer) + "\r\n")		
		output = s.recv(1024)
		print "<< " + output
		print "[INFO] Closing connection..."
		s.close()
	except:
		print "[ERROR] Connection refused. Or server crashed? "		

#Fuzz the password field with the evil buffer 
def fuzzPassword(host, port):
	print "[INFO] Fuzzing password field"	
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		connect = s.connect((host,port))
		output = s.recv(1024)
		print "<< " + output
		print "[INFO] Logging in..."
		s.send("USER " + "evilcat" +"\r\n")
		output = s.recv(1024)
		print "<< " + output
		print "[INFO] Sending evil buffer: [AAAAAA...]"		
		s.send("PASS " + "".join(evil_buffer) + "\r\n")		
		output = s.recv(1024)
		print "<<  "+ output 
		print "[INFO] Closing connection..."
		s.close()
	except:
		print "[ERROR] Connection refused. Or server crashed? "		

def main(host,port):
	if  (arguments_bol == False):
		host = raw_input("RHOST: ") #Ask for target ip
		port = input ("RPORT: ") #Ask for target port
	else:
		print "RHOST: " + host #Show target ip
		print "RPORT: " + str(port)# Show target port
	fuzz_len = input("Fuzz string lenght (A): ") #Ask the lenght of the fuzz srtring (A)
	fillList(fuzz_len) #Fill the evil buffer with "A"*fuzz_len
	
	#Ask if username field will be fuzzed:
	check = False
	while (check == False):
		fuzzUserAnswer = raw_input("Fuzz Username Field? (y/n): ")
		fuzzUserAnswer.lower()
		if (fuzzUserAnswer == "y" or fuzzUserAnswer == "yes"):
			fuzzUser = True
			check = True
		elif (fuzzUserAnswer == "n" or fuzzUserAnswer == "no"):
			fuzzUser = False
			check = True
		else:
			print "[ERROR] Please answer with (y/n)"
	
	#Ask if password field will be fuzzed:
	check = False
	while check == False:
		fuzzPassAnswer = raw_input("Fuzz Password Field? (y/n): ")
		fuzzPassAnswer.lower()
		if (fuzzPassAnswer == "y" or fuzzPassAnswer == "yes"):
			fuzzPass = True
			check = True
		elif  (fuzzPassAnswer == "n" or fuzzPassAnswer == "no"):
			fuzzPass = False
			check = True
		else:
			print "[ERROR] Please answer with (y/n)"
	print ""
	
	if (fuzzUser == True and fuzzPass == True):
		fuzzUsername(host,port)
		fuzzPassword(host,port)
	elif (fuzzUser== True and fuzzPass == False):
		fuzzUsername(host,port)
	elif (fuzzUser == False and fuzzPass == True):
		fuzzPassword(host,port)
	else:
		print "[ERROR] Unknown error"
		
try:
	if len(sys.argv[1:]): #Check for command line options
		arguments_bol = True
		opts, args = getopt.getopt(sys.argv[1:],"t:p:",["target","port"])
		for o,a in opts:
			if o in ("-t", "--target"):
				host = a
			elif o in ("-p","--port"):
				port = int(a)
	else:
		arguments_bol = False	
	banner()
	main(host,port)
except:	
	print "\n[INFO] Quitting..."
