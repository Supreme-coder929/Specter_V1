# VERY IMPORTANT !!!!
# BEFORE RUNNING THIS SCRIPT YOU MUST EITHER MAKE A ENVIORNMENT FILE DEFINING THE TWILIO AUTH TOKEN AND SID ACCOUNT INFORMATION FOR SMS TO WORK
# YOU MUST ALSO DEFINE YOUR OWN EMAIL FOR THE EMAIL FUNCTION ALL VARIABLES THAT CAN BE DEFINED ARE DOWN BELOW.
# YOU CAN CHANGE THE ENVIORMENT VARIABLES TO PLAIN TEXT OR MAKE AN ENVIORNMENT VARIABLE FOR IT
# I USED MY OWN ENVIORNMENTS VARIABLES BUT REMEMBER YOU CAN CHANGE THEM TO YOUR SPECIFICATIONS
#
# I, THE AUTHOR OF THIS SCRIPT IS NOT RESPONSIBLE FOR ANYTHING YOU DO WITH THIS.
# USE AT YOUR OWN CAUTION
#
#
# MORE WILL BE ADDED TO IT 
#
#
# THIS SCRIPT MAY NOT BE THAT GOOD BUT IT WAS JUST FOR ME TO TEST MY CODING SKILLS IM STILL A INTERMEDIATE 


# Need modules

import nmap3
import subprocess
import os
import sys
import pyperclip
import requests
import time
import socket
import simplejson as json
import pprint
import datetime
import re
import argparse
import pyfiglet
from termcolor import colored, cprint
from colorama import Fore, Back, Style
import smtplib
from dotenv import load_dotenv, find_dotenv
from twilio.rest import Client


load_dotenv(find_dotenv(".env_var"))



# Important Variables


nmap = nmap3.Nmap()
nmapTec = nmap3.NmapScanTechniques()



translatePort = {
	20:'ftp',
	21:'ftp',
	22:'ssh',
	25:'smtp',
	53:'dns',
	69:'tftp',
	80:'http',
	88:'Kerberos',
	102:'Iso-tsap',
	110:'POP3',
	123:'ntp',
	135:'Microsoft-EPMAP',
	137:'netBIOS-ns',
	139:'netBIOS-ssn',
	179:'bgp',
	443:'https',
	445:'microsoft-ds',
	512:'exec',
	514:'shell',
	1099:'rmiregistry',
	1524:'ingreslock',
	500:'ISAKMP',
	902:'VMware-Server',
	1725:'steam',
	2049:'nsf',
	2121:'ccproxy-ftp',
	3306:'mySql',
	5432:'postgresql',
	3398:'RDP',
	4664:'Google-Desktop',
	5900:'vnc',
	6000:'X11',
	6667:'irc',
	6681:'BitTorrent',
	6999:'BitTorrent',
	8009:'ajp13',
	8180:'unknown',
	12345:'NetBus',
	18006:'Back Orifice',
	27374:'Sub7'

}


# Variables

scanOption = ''
ipTarget = ''
valid = ''
IPformat = re.compile(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')
ports = ''
scanner = ''


# Email Variables

emailADDRESS = os.getenv('EMAIL_ADDRESS')
emailPASSWORD = os.getenv('EMAIL_PASSWORD')
subject = ''
message = ''
targetEMAIL = ''
fullMessage = ''
EMAILformat = re.compile(r'^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$')
validEmail = ''

# SMS Variables

AccountSID = os.getenv('TWILIO_ACCOUNT_SID')
AuthToken = os.getenv('TWILIO_AUTH_TOKEN')
client = ''
target_number = ''
from_number = ''
message = ''
correctInput = ''


# NMAP OUTPUT VARIABLES

outputNmap = ''
outputJson = ''


# Python Scanner Variables

sockStart = ''
resultOut = ''
timepythonScan = (Fore.GREEN + str(datetime.datetime.today()))
beginPort = ''
endPort = ''
openPort = ''

# Webscrape Variables

url = ''
autoWordlist = '/usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt'

# Custom Webscrape Variables

url_custom = ''
customWordlist = ''


# Time Variables

timeNmap = (Fore.RED + str(datetime.datetime.today()))


##########

def OperatingSystemCheck():
	cprint('\t [+] Checking Operating System... \n', 'green')
	time.sleep(1)
	if sys.platform == 'win32':
		sys.exit(cprint("\t[!] Windows Detected! Specter V1 is not compatible with Windows 32 BIT", 'red'))  

	if sys.platform == 'win64':
		sys.exit(cprint("\t[!] Windows Detected! Specter V1 is not compatible with Windows 64 BIT ", 'red'))  

	else:
		cprint("\t[+] Unix/Linux Kernel Detected...\n", 'green')
		time.sleep(0.5)
		os.system('clear')  


if os.geteuid() != 0:
   sys.exit(Fore.RED + 'Must have root priv to run this script.')

OperatingSystemCheck()



print(f"{colored(pyfiglet.figlet_format('Specter V1', font='slant'), 'green', attrs=['bold'])}")													 								

print(f'''

------------------- Description -------------------------

Current Version: 1.0.0 - New Release
Credits: MistyMan
License: MIT License

---------------------------------------------------------


''')


def sendSMS(Account_SID, Auth_Token, client, targetPhoneNumber, fromNumber, message):
	try:
		print('Welcome to the SMS Client')
		print('Enter the target Phone Number')
		print('You must also enter the region number like +1 for US')
		targetPhoneNumber = input('--> ')
		print('Enter the sender number.')
		print('Meaning your number')
		fromNumber = input('--> ')
		print('Finally enter your message.')
		message = input('--> ')


		client = Client(Account_SID, Auth_Token)



		client.messages.create(

			to=str(targetPhoneNumber),
			from_=str(fromNumber),
			body=str(message)

			)

		print(f'''

		---	Message Details ---

			TARGET = {targetPhoneNumber}
			SENDER = {fromNumber}
			MESSAGE = {message}


			''')
		print('Message Sent')

	except KeyboardInterrupt:
		emailMenu()

	except:
		print('Make sure you have edited any variables correctly. \nRemember you need a phone number trial in twilio trial/upgraded account \n You must also verify the number your sending to if you have a trial account')
		

	

def sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, Subject, Message, targetEmail, fullmessage, emailValid, OutputValid):
	try:
		print('Welcome to the SMTP Email Client.')
		print('All emails will go through TLS')
		print('Enter the target email.')
		targetEmail = input('Target Email: ')
		try:
			OutputValid = emailValid.search(targetEmail.strip())
			print('Valid Email Address: ' + str(OutputValid.group()))
		except:
			print(f'Invalid Email Address: {targetEmail}')
			sys.exit('Vaild Email Address Syntax - abc@123.com')


		with smtplib.SMTP('smtp.mailgun.com', 587) as smtp:
			smtp.ehlo()
			smtp.starttls()
			smtp.ehlo()

			# Login To Address
			smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

			# Make Email
			print('Enter the Title of the Email.')
			Subject = input('Title: ')
			print('Enter the body of the Email. ')
			Message = input('Body: ')
			
			fullmessage = f'Subject: {Subject}\n\n{Message}'

			# Send Email
			smtp.sendmail(EMAIL_ADDRESS, str(targetEmail), fullmessage)
	  		
			print('Email has been sent')
			print('It will take about 1-2 minutes for it to send')
	except KeyboardInterrupt:
		emailMenu()



def customWordlistScrape(customWordlist, urlc):
	try:
		print('Welcome to the custom wordlist bruteforcer')
		print('Enter full path of wordlist.')
		customWordlist = input('--> ')
		if os.path.exists(str(customWordlist.strip())):
			cprint('[+] Checking if file path exists', 'yellow')
			time.sleep(0.5)
			cprint('[+] File does exist', 'yellow')
		else:
			cprint('[+] Checking if file path exists', 'yellow')
			time.sleep(0.5)
			cprint('[-] Folder does not exist', 'red')
			sys.exit(cprint('\tWrong File Path', 'red'))
		time.sleep(0.5)
		print('Enter the full url.')
		urlc = input('URL --> ')
		
		os.system('clear')

		cprint("----- BRUTEFORCING DIRECTORIES -----", 'red')

		if not urlc.endswith('/'):
			urlc = urlc+"/"

		with open(customWordlist, 'rt') as wordlists:
		        word = wordlists.readlines()
		        for i in word:
		            host = urlc+i.strip("\n")
		            r = requests.get(host)

		            if i.startswith('#'):
		                continue

		            if i.strip() == '':
		            	continue

		            if r.status_code == 200:
		                print(f"[{colored('+', 'green')}] {host} \t{colored(r.status_code, 'green')}")
		            elif r.status_code == 302:
		                print(f"[{colored('*', 'yellow')}] {host} \t{colored(r.status_code, 'yellow')}")
		            else:
		                pass
	except KeyboardInterrupt:
		scrapeMenu()

def autoWordlistScrape(wordlist, url):
	try:
		print("You must install secLists folder from github if you want this to work.")
		print("Checking if folder exists...")
		if os.path.exists('/usr/share/wordlists/seclists'):
			cprint('Scanning File system...', 'yellow')
			time.sleep(0.5)
			cprint('[+] Folder does exist', 'yellow')
		else:
			cprint('Scanning FIle system...')
			time.sleep(0.5)
			cprint('[-] Folder does not exist', 'red')
		time.sleep(0.5)
		print('Enter the full url.')
		url = input('URL --> ')
		
		os.system('clear')

		cprint("----- BRUTEFORCING DIRECTORIES -----", 'red')

		if not url.endswith('/'):
			url = url+"/"

		with open(wordlist, 'rt') as wordlists:
		        word = wordlists.readlines()
		        for i in word:
		            host = url+i.strip("\n")
		            r = requests.get(host)

		            if i.startswith('#'):
		                continue

		            if i.strip() == '':
		            	continue    

		            if r.status_code == 200:
		                print(f"[{colored('+', 'green')}] {host} \t{colored(r.status_code, 'green')}")
		            elif r.status_code == 302:
		                print(f"[{colored('*', 'yellow')}] {host} \t{colored(r.status_code, 'yellow')}")
		            else:
		                pass
	except KeyboardInterrupt:
		scrapeMenu()                



def specificPortScan(validateIP, output, targetIP, sock, result, timeComplete, begin, end, tranPort, portOpen):
	print('Enter the target IP address.')
	targetIP = input('IP: ')
	try:
		output = validateIP.search(targetIP.strip())
		print('Valid IP Address Chosen: ' + str(output.group()))
		time.sleep(0.4)
	except:
		print(f'Invalid IP Address: {targetIP}')
		sys.exit('Vaild IP Syntax - x.x.x.x')
	print('Enter the port to start and end.')
	begin = input('BEGIN: ')
	end = input('END:')
	try:
		print('NOTE: Python Scan can be buggy. I would recommend using nmapScan while I try to make it a little more accurate and faster.')
		print('NOTE: If PythonScan does find a PORT it will display accurate results. Im just going to try to make it find more if there are any.')
		for port in range(int(begin), int(end)):
			for key, value in tranPort.items():
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socket.setdefaulttimeout(0.5)
				result = sock.connect_ex((targetIP, port))
				if result == 0:
					if str(key) in str(port):
						if str(key) == str(port):
								portOpen = print(Fore.YELLOW + f'[{port}]' + Fore.GREEN + ' is open - ' + str(value))
				sock.close()


	except KeyboardInterrupt:
		print('Exiting Scan...')
		scanMenu()

	except socket.gaierror:
		print('Hostname could not be found.')
		sys.exit('Exiting Program')

	except socket.error:
		print(f'Problem with connecting to {targetIP}')
		sys.exit('Exiting Program')

	print(timeComplete)
	print('\033[39m')

def quitePortScan(validateIP, output, targetIP, sock, result, timeComplete):

	print('Enter the target IP address.')
	targetIP = input('IP: ')
	try:
		output = validateIP.search(targetIP.strip())
		print('Valid IP Address Chosen: ' + str(output.group()))
		time.sleep(0.4)
	except:
		print(f'Invalid IP Address: {targetIP}')
		sys.exit('Vaild IP Syntax - x.x.x.x')

	try:
		print('NOTE: Python Scan can be. I would recommend using nmapScan while I try to make it faster.')
		for port in range(1,1024):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket.setdefaulttimeout(0.5)
			result = sock.connect_ex((targetIP, port))
			if result == 0:
				print(Fore.YELLOW + f'[{port}]' + Fore.GREEN + ' is open')
			sock.close()


	except KeyboardInterrupt:
		print('Exiting Scan..')
		scanMenu()

	except socket.gaierror:
		print('Hostname could not be found.')
		sys.exit('Exiting Program')

	except socket.error:
		print(f'Problem with connecting to {targetIP}')
		sys.exit('Exiting Program')

	print(timeComplete)
	print('\033[39m')
	



def pythonScan(validip, outputip):
	global scanOption

	print('''

	------- Options -------

	> quitePortScan
	> specificPortScan


		''')
	while True:
		print('Pick a option.')
		scanOption = input("> ")
		if scanOption.strip() == 'quitePortScan':
			topPortScan(IPformat, valid, ipTarget, sockStart, resultOut, timepythonScan)
		elif scanOption.strip() == 'specificPortScan':
			specificPortScan(IPformat, valid, ipTarget, sockStart, resultOut, timepythonScan, beginPort, endPort, translatePort, openPort)
			# specificPortScan(IPformat, valid)
	


def nmapScan(validateIP, output, nmapOutput, jsonOutput, nmapTime):
	global scanOption
	global targetIP

	print('''

	------- Options -------

	> FullScan
	> HeavyScan
	> StealthScan
	> LightScan


		''')

	print('Enter the target IP address.')
	targetIP = input('IP: ')
	try:
		output = validateIP.search(targetIP.strip())
		print('Valid IP Address Chosen: ' + str(output.group()))
		time.sleep(0.4)
	except:
		print(f'Invalid IP Address: {targetIP}')
		sys.exit('Vaild IP Syntax - x.x.x.x')
	try:
		while True:
			print('NOTE: Nmap scans can take up to 1-2 minutes depending on scan type.')
			print('Choose Option Mode')
			scanOption = input("> ")
			if scanOption.strip() == "HeavyScan":
				nmapOutput = nmap.nmap_version_detection(str(targetIP))
				jsonOutput = json.dumps(nmapOutput, indent=4)
				print(jsonOutput)
				print(f'Scan Time Complete --> {nmapTime}')
				print('\033[39m')
				#pprint.pprint(nmapOutput, indent=4)
			elif scanOption.strip() == "StealthScan":
				nmapOutput = nmap.scan_top_ports(str(targetIP), args="-sS")
				jsonOutput = json.dumps(nmapOutput, indent=4)
				print(jsonOutput)
				print(f'Scan Time Complete --> {nmapTime}')
				print('\033[39m')
				#pprint.pprint(nmapOutput, indent=4)
			elif scanOption.strip() == "LightScan":
				nmapOutput = nmap.scan_top_ports(str(targetIP), args="-f")
				jsonOutput = json.dumps(nmapOutput, indent=4)
				print(jsonOutput)
				print(f'Scan Time Complete --> {nmapTime}')
				print('\033[39m')
			elif scanOption.strip() == "FullScan":
				nmapOutput = nmap.scan_top_ports(str(targetIP), args="-p- -A -sV")
				jsonOutput = json.dumps(nmapOutput, indent=4)
				print(jsonOutput)
				print(f'Scan Time Complete --> {nmapTime}')
				print('\033[39m')
				#pprint.pprint(nmapOutput, indent=4)
	except KeyboardInterrupt:
		scanMenu()



def scanMenu():
	# Global Needed Variables
	global scanOption

	try:
		print(f'''

		------- {colored('Options', 'magenta')} -------

		> {colored('nmapScan', 'blue')}
		> {colored('pythonScan', 'blue')}


			''')
		while True:
			print("Pick your options.")
			scanOption = input('> ')
			if scanOption.strip() == 'nmapScan':
				nmapScan(IPformat, valid, outputNmap, outputJson, timeNmap)
			elif scanOption.strip() == 'pythonScan':
				pythonScan(IPformat, valid)
	except KeyboardInterrupt:
		main()


def scrapeMenu():
	global scanOption

	try:
		print(f'''

		-------- {colored('Options', 'magenta')} --------

		> {colored('customWordlistScrape', 'blue')}
		> {colored('autoWordlistScrape', 'blue')}


			''')

		while True:
			print('Pick your options.')
			scanOption = input('> ')
			if scanOption.strip() == 'customWordlistScrape':
				customWordlistScrape(customWordlist, url_custom)
			elif scanOption.strip() == 'autoWordlistScrape':
				autoWordlistScrape(autoWordlist, url)
	except KeyboardInterrupt:
		main()


def emailMenu():
	global scanOption

	try:
		print(f'''

		------ Options -----

		> SMS
		> Email


			''')
		print('Pick your options.')
		while True:
			scanOption = input("> ")
			if scanOption.strip() == 'SMS':
				sendSMS(AccountSID, AuthToken, client, target_number, from_number, message)
			elif scanOption.strip() == 'Email':
				sendEmail(emailADDRESS, emailPASSWORD, subject, message, targetEMAIL, fullMessage, EMAILformat, validEmail)
	except KeyboardInterrupt:
		main()


time.sleep(0.5)

def main():
	try:
		print('''\n

---------------------- Options ----------------------------

NOTE: More options in the future

> scan
> scrape
> socialEngineer

-----------------------------------------------------------

			''')
		while True:
			print("Pick your options.")
			option = input("> ")
			if option.strip() == 'scan':
				scanMenu()
			elif option.strip() == 'scrape':
				scrapeMenu()
			elif option.strip() == 'socialEngineer':
				emailMenu()
	except KeyboardInterrupt:
		sys.exit('\nExiting Program.')


if __name__ == '__main__':
	main()




	
