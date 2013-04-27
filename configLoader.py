#!/usr/bin/python

import os

class configLoader(object):
	def __init__(self):
		self.boolStrings = ("true", "false", "yes", "no")
		self.configDic = {}
		
		self.loadConfig()

	def loadConfig(self):
		pT = None
		
		# conf.local for developers ;)
		if os.path.exists('newagora.conf.local'):
			pT = open('newagora.conf.local', 'r')
		else:
			pT = open('newagora.conf', 'r')
		
		lines = pT.readlines()
		pT.close()
		
		for lineRaw in lines:
			line = lineRaw.strip()
			
			if '=' in line and line.find('#') != 0:
				tmpSplit = line.split('=')
				
				key = tmpSplit[0].strip()
				valTmp = tmpSplit[1].strip()
				
				val = None
				
				if valTmp.lower() in self.boolStrings:
					val = self.str2bool(valTmp)
				elif '.' in valTmp and valTmp.replace('.', '').isdigit():
					val = float(valTmp)
				elif valTmp.isdigit() == True:
					val = int(valTmp)
				else:
					val = valTmp
				
				self.configDic[key] = val
	
	def str2bool(self, trueStr):
		return trueStr.lower() in ("true", "yes", "t", "1")
				
	def getValue(self, key, default=''):
		if not key in self.configDic:
			print ('NONE!')
			return default
		else:
			return self.configDic[key]


# initialize itself for instand availability after import
conf = configLoader()

# make it optional to save the passwords in PLAINTEXT in the config file
if conf.getValue("askForPop3Pw", False):
	import getpass
	conf.configDic['popPass'] = getpass.getpass("Password for POP3: ")
	
if conf.getValue("askForSmtpPw", False):
	import getpass
	conf.configDic['smtpPass'] = getpass.getpass("Password for SMTP: ")


# test if your config is ok
if __name__ == "__main__":
	print( conf.configDic )
	print( conf.getValue("maxLines", 23) )
	print( conf.getValue("nf", "nf") )
	
