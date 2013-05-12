#define an arbitrary length for responses
MAX_LENGTH = 140

#	Truncates a string to fit into MAX_LENGTH, rounding down
#	to the complete word. Also, remove HTML, and add an ellipsis.

def getSummary(string):

	# add an ellipsis if the content exceeds MAX_LENGTH
	if len(string)>MAX_LENGTH:
		string = string[:MAX_LENGTH]	# Yay, Python!
		for i in range(MAX_LENGTH,-1,-1):
			if string[i-1] == ' ':
				string = string[:i-1] + '...'
				break

	#	Walk the string, stripping HTML. Assumes 
	#	that there are no less than or greater than
	#	signs arbitrarily contained in the string.

	for i in range(0,len(string)):
		if string[i] == '<':
			first = i
			for j in range(first,len(string)):
				if string[j] == '>':
					string = string.replace(string[first:j+1],'')
					break

		# If the last character is a < then we
		# don't want to enter the previous loop.
		# (Not sure this is necessary.)
		
		if(i==len(string)-1):
			break

	return string
