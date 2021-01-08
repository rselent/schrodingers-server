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

DEBUG = 2

SOCK4T = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		# IPv4 TCP sock
SOCK6T = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)		# IPv6 TCP sock
TIMEOUT = 3


# class baseCheck( object):			# setting this here, indicating plans
#									# for later
# 	def __init__( self):
# 		...


def userInput():
	"""
	Ask user for single domain to check (temp, expand later)
	"""

	urlInput = input( "\nEnter domain to check: ")

	if DEBUG == 2: print( "input\t", urlInput)

	return urlInput


def userCheck( urlMaybe= ""):
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

	if urlMaybe == "":
		BIGOOF = 1
		print( BIGOOF, "ERROR: URL string is empty.\n")
		return					# can we throw an exception instead?
	else:
		urlMaybe = urlMaybe.lower()

		if urlMaybe[:8] == 'https://':
			urlMaybe = urlMaybe[8:]
		elif urlMaybe[:7] == 'http://':
			urlMaybe = urlMaybe[7:]
		if urlMaybe[:4] == 'www.':
			urlMaybe = urlMaybe[4:]

		if DEBUG == 2: print( "check\t", urlMaybe)

		if urlMaybe[-4] == "." or urlMaybe[-3] == ".":
			return urlMaybe
		else:
			BIGOOF = 1
			print( BIGOOF, "ERROR: URL given does not look valid.\n")
			return				# can we throw an exception instead?


def getIP( urlProbably= "", port= 80, protocol= socket.IPPROTO_TCP):
	"""
	Get IPv4 and IPv6 addresses via DNS lookup
	"""
	global BIGOOF

	if urlProbably == "":
		BIGOOF = 1
		print( BIGOOF, "ERROR: URL string is empty. Halting DNS lookup\n")
		return					# can we throw an exception instead?
	else:
		ipResult = socket.getaddrinfo( urlProbably, port, proto= protocol)
		ipv4Result = ipResult[1][4][0]
		ipv6Result = ipResult[0][4][0]

		if DEBUG == 2: 
			print( "raw\t", ipResult)
			print( "get\t", ipv4Result, "\t", ipv6Result)

		return ipv6Result, ipv4Result



def headRequest( urlDefinitely= "", useipv6= False):
	"""
	Request HEAD of given address
	"""

	socket.setdefaulttimeout( TIMEOUT)

	try:
		if useipv6 == True:
			SOCK6T.connect( (urlDefinitely[0], 80, 0, 0))
			return True
		else:
			SOCK4T.connect( (urlDefinitely[1], 80))
			return True
	except socket.error as oof:
		print( oof)
		return False
	



def dispStatus( upDownBool, serviceName):
	"""
	Display UP/DOWN status
	"""
	if DEBUG == 1:
		...
	
	if upDownBool == True:
#		print( "Service is UP\n\n")
		return f"\nService {serviceName} is UP\n\n"
	else:
#		print( "Cannot connect to service\n\n")
		return f"\nCannot connect to {serviceName}\n\n"



if __name__ == "__main__":

	BIGOOF = 0

	mainInput = userInput()
	checkedInput = userCheck( mainInput)

	if BIGOOF == 0:
		gotIP = getIP( checkedInput)
		upDown = headRequest( gotIP, useipv6= False)
		print( dispStatus( upDown, checkedInput))
	else:
		print( "BIGOOF THROWN. service discovery aborted. please try again with a valid URL.\n")

