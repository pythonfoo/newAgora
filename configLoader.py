import os

class configLoader(object):
	def __init__(self):
		pT = None
		
		# conf.local for developers ;)
		if os.path.exists('newagora.conf.local'):
			pT = open('newagora.conf.local', 'r')
		else:
			pT = open('newagora.conf', 'r')
		
		lines = pT.readlines()
		pT.close()
		self.configDic = {}
		
		for lineRaw in lines:
			line = lineRaw.strip()
			
			if line != '' and line.find('#') != 0:
				tmpSplit = line.split('=')
				
				key = tmpSplit[0].strip()
				valTmp = tmpSplit[1].strip()
				
				val = None
				
				if valTmp.lower() == 'true' or valTmp.lower() == 'false':
					val = bool(valTmp)
				elif '.' in valTmp and valTmp.replace('.', '').isdigit():
					val = float(valTmp)
				elif valTmp.isdigit() == True:
					val = int(valTmp)
				else:
					val = valTmp
				
				self.configDic[key] = val
				#print(self.configDic)
				
	def getValue(self, key, default=''):
		# OLD method!
		#if self.configDic.has_key(key) == False:
		if not key in self.configDic:
			print ('NONE!')
			return default
		else:
			return self.configDic[key]

		
conf = configLoader()

# Make it optional to save the passwords in PLAINTEXT in the config file
if conf.getValue("askForPop3Pw", False):
	import getpass
	conf.configDic['popPass'] = getpass.getpass("Password for SMTP: ")
	
if conf.getValue("askForSmtpPw", False):
	import getpass
	conf.configDic['smtpPass'] = getpass.getpass("Password for SMTP: ")

			
if __name__ == "__main__":
	print( conf.configDic )
	print( conf.getValue("maxLines", 23) )
	print( conf.getValue("nf", "nf") )
	
