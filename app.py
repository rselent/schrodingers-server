# Schrödinger's Server
# by Raymond Selent
#
# Purpose: register and ping URL, and display UP/DOWN status
#		   (this is expected to change over time)
#
# Requirements: Python (3.9)
#
#
#
# ==========================================================
# ==========================================================


import socket


DEBUG = 1			# DEBUG LEVEL
					# 0 = OFF
					# 1 = BASIC CONSOLE OUTPUT
					# 2 = BASIC + ADVANCED


SOCK4T = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		# IPv4 TCP sock
SOCK6T = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)		# IPv6 TCP sock
TIMEOUT = 3


# class baseCheck( object):			# putting this here for later
#
# 	def __init__( self):
# 		...


def domainInput():
	"""
	Ask user for single domain to check (temp, expand later)
	"""
	global domainDict

	print( "\n" * 3, end= '')

	print( "Hello user! Please enter up to 10 domains that you'd like to check.")
	print( "Pressing ENTER without a domain input will end this early", \
		"and advance to the results.")
	print( "\nEnter domain:\t", end= '')
	urlInput = input()

#	for i in range( 10):
#		urlInput = input()




	if DEBUG == 2: print( "input value\t", urlInput)

	return urlInput


def domainCheck( urlMaybe= ""):
	"""
	Checks if given input is a potentially valid domain.

	Dataflow (error-less):
	Forces lowercase, normalizing input string >
	If string is prepended by 'https://' or 'http://', removes those chars >
	If string is then prepended by 'www.', removes those chars >
	If string has '.' in 4th to last or 3rd to last char (eg: .com or .co.uk) >
	String is probably a valid domain
	"""
	global BIGOOF
	global domainDict

	if urlMaybe == "":
		BIGOOF = 1
		print( "ERROR: URL string is empty.\n")
		return					# can we throw an exception instead?
	else:
		urlMaybe = urlMaybe.lower()

		if urlMaybe[:8] == 'https://':
			urlMaybe = urlMaybe[8:]
		elif urlMaybe[:7] == 'http://':
			urlMaybe = urlMaybe[7:]
		if urlMaybe[:4] == 'www.':
			urlMaybe = urlMaybe[4:]

		if DEBUG == 2: print( "after check\t", urlMaybe)

		if urlMaybe[-4] == "." or urlMaybe[-3] == ".":
			return urlMaybe
		else:
			BIGOOF = 1
			print( "ERROR: URL given does not look valid.\n")
			return				# can we throw an exception instead?


def getIP( urlProbably= "", port= 80, protocol= socket.IPPROTO_TCP):
	"""
	Get IPv4 and IPv6 addresses via DNS lookup
	"""
	global BIGOOF
	global domainDict

	if urlProbably == "":
		BIGOOF = 1
		print( "ERROR: URL string is empty. Halting DNS lookup\n")
		return					# can we throw an exception instead?
	else:
		ipResult = socket.getaddrinfo( urlProbably, port, proto= protocol)
		ipv4Result = ipResult[1][4][0]
		ipv6Result = ipResult[0][4][0]

		if DEBUG == 2: 
			print( "ip addresses\t", ipv4Result, "\t", ipv6Result)
			print( "raw info\t", ipResult)

		return ipv6Result, ipv4Result



def headRequest( urlDefinitely= "", useipv6= False):
	"""
	Request HEAD of given address
	"""

	socket.setdefaulttimeout( TIMEOUT)

	try:
		if useipv6 == True:
			SOCK6T.connect( (urlDefinitely[0], 80, 0, 0))
			SOCK6T.shutdown( socket.SHUT_RDWR)
			SOCK6T.close()
			return True
		else:
			SOCK4T.connect( (urlDefinitely[1], 80))
			SOCK4T.shutdown( socket.SHUT_RDWR)
			SOCK4T.close()
			return True
	except socket.error as oof:
		print( oof)
		return False
	



def dispStatus( upDownBool, serviceName):
	"""
	Display UP/DOWN status
	"""

	structure = []

	if DEBUG >= 1:
		print( "\n", end= '')
		print( "=" * 120)
#		print( "\tSERVICE\t\t\t\tIPv4/IPv6\t\tUP/DOWN")
		print( "\tSERVICE\t\t\t\t\tUP/DOWN")
		print( "-" * 120)
	
		if upDownBool == True:
			print( f"\t{serviceName}\t\t\t\tUP")
#			return f"\nService {serviceName} is UP\n\n"
		else:
			print( f"\t{serviceName}\t\t\t\tDOWN")
#			return f"\nCannot connect to {serviceName}\n\n"

		print( "=" * 120, "\n")



if __name__ == "__main__":

	BIGOOF = 0

	domainDict = {}

	mainInput = domainInput()
	checkedInput = domainCheck( mainInput)

	if BIGOOF == 0:
		gotIP = getIP( checkedInput)
		upDown = headRequest( gotIP, useipv6= False)
		dispStatus( upDown, checkedInput)
	else:
		print( "BIGOOF THROWN. service discovery aborted. please try again with a valid URL.\n")

