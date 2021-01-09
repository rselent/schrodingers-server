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


DEBUG = 2			# DEBUG LEVEL
					# 0 = OFF
					# 1 = BASIC CONSOLE OUTPUT
					# 2 = BASIC + ADVANCED


SOCK4T = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		# IPv4 TCP sock
SOCK6T = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)		# IPv6 TCP sock
TIMEOUT = 0

# Attempt #1 to solve socket errors -- failed D:
SOCK4T.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



def domainInput():
	"""
	Asks user for desired domains to check and saves them in a dictionary.

	Dataflow:
	Prints intro message, asks for initial input >
	Loops through 10 iterations (supporting 10 domains):
		Creates dict key:value pair, using i for key (like index) >
		Checks if input store is empty and if it's the first entry in dict, 
			breaks loop to move on to next func and error out >
		If input store is empty but there are other entries in dict,
			removes empty key:value pair and breaks loop to move on >
		If above conditions aren't triggered, assigns input store as value for
			current key iteration >
		Asks for next input from user for all iterations except the final 10th
			(because of the first input request, outside of loop)
	Returns dictionary, regardless of size
	"""

	inputDict = {}

	print( "\n" * 3, end= '')

	print( "Hello user! Please enter up to 10 domains that you'd like to check.")
	print( "Pressing ENTER without a domain input will end this early", \
		"and advance to the results.")
	print( "\nEnter domain:\t ", end= '')

	urlInput = input()

	for i in range( 10):
		inputDict[i] = [""]

		if DEBUG == 2:
			print( f"input value\t {urlInput}")
		if urlInput == "" and len( inputDict) == 1:
			break
		elif urlInput == "":
			inputDict.popitem()
			break

		inputDict[i] = [urlInput]

		if i < 9:					# only purpose is to keep console input
			urlInput = input("\t\t ")		# vertically aligned

	if DEBUG == 2: 
		print( f"\n\t EXIT CALLED\ndict values\t {inputDict}\n")

	return inputDict



def domainCheck( urlMaybeDict):
	"""
	Checks if all dictionary inputs are potentially valid domains.

	Dataflow (assuming good faith, no errors):
	Iterate through all dictionary key:value pairs:

		Forces lowercase, normalizing input string >
		If string is prepended by 'https://' or 'http://', removes those chars >
		If string is then prepended by 'www.', removes those chars >
		If string has '.' in 4th to last or 3rd to last char (eg: .com or .co.uk) >
		String is probably a valid domain
	"""
	global BIGOOF

	for i, _ in enumerate( urlMaybeDict):

		urlMaybe = urlMaybeDict[i][0]		# copy dict value to temp variable
											# (makes below easier to read)
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

			if DEBUG == 2: print( f"after check\t {urlMaybe}")

			if urlMaybe[-4] == "." or urlMaybe[-3] == ".":
				urlMaybeDict[i][0] = urlMaybe	# reassign cleaned URL to dict
			else:
				BIGOOF = 1
				print( f"ERROR: URL given ({urlMaybe}) does not look valid.\n")
				return				# can we throw an exception instead?
	return urlMaybeDict



def getIP( urlProbablyDict, port= 80, protocol= socket.IPPROTO_TCP):
	"""
	Get IPv4 and IPv6 addresses via DNS lookup
	"""
	global BIGOOF

	for i, _ in enumerate( urlProbablyDict):

		urlProbably = urlProbablyDict[i]		# copy dict value to temp variable

		if urlProbably[0] == "":
			BIGOOF = 1
			print( "ERROR: URL string is empty. Halting DNS lookup\n")
			return					# can we throw an exception instead?
		else:
			ipResult = socket.getaddrinfo( urlProbably[0], port, proto= protocol)
			urlProbably.append( ipResult[1][4][0])		# ipv4
			urlProbably.append( ipResult[0][4][0])		# ipv6

			if DEBUG == 2: 
				print( f"\nip addresses\t{urlProbably}")
				print( f"raw info\t {ipResult}\n")
			
			urlProbablyDict[i] = urlProbably

	return urlProbablyDict



def headRequest( urlDefinitelyDict, useipv6= False):
	"""
	Request HEAD of given address
	"""

	socket.setdefaulttimeout( TIMEOUT)

	for i, _ in enumerate( urlDefinitelyDict):

		urlDefinitely = urlDefinitelyDict[i]		# copy dict value to temp variable
		urlDefinitely.append( False)			# append False bool to [3]
		urlDefinitely.append( False)			# append False bool to [4]

		# not very dry here, but... ¯\_(ツ)_/¯
		try:
			SOCK4T.connect( (urlDefinitely[1], 80))
			urlDefinitely[3] = True				# if it connects, change [3] to True
		except socket.error as oof4:				# if not, print error to console
			print( oof4)

		# unsure about ipv6 implementation
#		if useipv6 == True:
#			try:
#				SOCK6T.connect( (urlDefinitely[2], 80, 0, 0))
#				SOCK6T.shutdown( socket.SHUT_RDWR)
#				SOCK6T.close()
#				urlDefinitely[4] = True
#			except socket.error as oof6:
#				print( oof6)

		urlDefinitelyDict[i] = urlDefinitely

	# yeah, let's not close sockets until after we're all done...
	SOCK4T.shutdown( socket.SHUT_RDWR)
	SOCK4T.close()

	return urlDefinitelyDict



def dispStatus( upDownDict):
	"""
	Display UP/DOWN status
	"""

	if DEBUG >= 1:
		print( "\n", end= '')
		print( "=" * 120)
		print( "\tSERVICE\t\t\t\t\tUP/DOWN")
		print( "-" * 120)
	
	for i, _ in enumerate( upDownDict):

		upDown = upDownDict[i]		# copy dict value to temp variable

		if upDown[3] == True or upDown[4] == True:
			print( f"\t{upDown[0]}\t\t\t\tUP")
		else:
			print( f"\t{upDown[0]}\t\t\t\tDOWN")

	print( "=" * 120, "\n")



if __name__ == "__main__":

	BIGOOF = 0

#	domainDict = {}

	mainInput = domainInput()
	checkedInput = domainCheck( mainInput)

	if BIGOOF == 0:
		gotIP = getIP( checkedInput)
		upDown = headRequest( gotIP, useipv6= False)
		dispStatus( upDown)
	else:
		print( "BIGOOF THROWN. service discovery aborted. please try again with a valid URL.\n")

