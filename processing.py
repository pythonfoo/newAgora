#!/usr/bin/python

import sendMail
import urllib2
import re
import os
import shutil
import configLoader
from modules.pageLoader import pageLoader

class newAgora(object):
	def __init__(self):
		self._pSend = sendMail.pageSender()
		self._pLoader = pageLoader()
	
		self.pageDir = configLoader.conf.getValue('pageDir') #"pages/"
		self.mailDir = configLoader.conf.getValue('mailDir') #"mails/"
		self.mailBackupDir = configLoader.conf.getValue('mailBackupDir') #"mails_back/"
		self.backupMails = configLoader.conf.getValue('backupMails')
		self.maxLinksPerMail = configLoader.conf.getValue('maxLinksPerMail') #2
			
		self.HEADERS = "From To Subject".split()

		# headers you're actually interested in
		self.rx_headers  = re.compile('|'.join(self.HEADERS), re.IGNORECASE)

		self.rx_from  = re.compile('From', re.IGNORECASE)
		self.rx_subject  = re.compile('Subject', re.IGNORECASE)
		#self.rx_findLinks = re.compile('(((news|(ht|f)tp(s?))\://){1}\S+)', re.IGNORECASE)
		self.rx_findLinks =  re.compile('((http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)', re.IGNORECASE)

		self.version = '0.2'
	
	def hasMails(self):
		dirList = os.listdir(self.mailDir)
		
		cnt = 0
		for fil in dirList:
			if fil.endswith('.eml'):
				cnt += 1
		
		if cnt > 0:
			return True
		else:
			return False
	
	def getMailFileName(self):
		dirList = os.listdir(self.mailDir)
		mailList = []
		
		for fil in dirList:
			if fil.endswith('.eml'):
				mailList.append(fil)
		
		if len(mailList) == 0:
			return ''
		
		return mailList[0]
			
	def getMailFileLines(self, filename):
		pT = open(self.mailDir + filename, 'r')
		lines = pT.readlines()
		pT.close()
		return lines
		
	def removeMail(self, mailFileName):
		if mailFileName != '':
			if self.backupMails == True:
				print('move: ' + self.mailDir + mailFileName +'->'+ self.mailBackupDir + mailFileName)
				shutil.move(self.mailDir + mailFileName, self.mailBackupDir + mailFileName)
			else:
				print('delete: ' + self.mailDir + mailFileName)
				os.remove(self.mailDir + mailFileName)

	def getContent(self, link):
		# own module with cache and stuff!
		return self._pLoader.getContent(link)
	
	def processHelp(self, userMailAddress):
		content = 'Hello '+ userMailAddress +'\n'
		fh = open('README.md')
		content += fh.read()
		fh.close()
		
		#TODO: nice template to speak direktly to the user?
		
		return '<pre>'+ content + '</pre>'
	
	def processRequest(self, linesFromMail):
		contents = []
		allLinks = re.findall(self.rx_findLinks, '\n'.join(linesFromMail))
		print('links:' , allLinks)
					
		countContent = 0
		for link in allLinks:
			countContent += 1
			
			if countContent > self.maxLinksPerMail:
				contents.append("Only " + str(self.maxLinksPerMail) + ' Links per request, please!')
				break
			else:
				#TODO: pack links into format X, encrypt with public key, etc
				
				contents.append(self.getContent(link[0]))
				#print contents[len(contents)-1]
				#x = raw_input(link[0] + '| break')
				
		#x = raw_input('WARNING')
		return contents
	
	def processRegistration(self, sender, linesFromMail):
		#TODO: get payload for gpg key, check database and so on
		#attachment.py
		#gnupg.py
		#userDb.py
		pass
	
	def process(self, mailFile = ''):
		if mailFile == '':
			mailFile = self.getMailFileName()
		
		if mailFile == '':
			return False
			
		lines = self.getMailFileLines(mailFile)
		
		sender = ' '.join(filter(self.rx_from.match, lines))
		sender = sender.strip()
		if sender != '':
			#print('sender: '+sender)
			sender =  sender.lower().replace('from: ', '')
			if '<' in sender:
				sender = sender.split('<')[1].replace('>', '').strip()
			print('sender: ' + sender)
		
		#sender = ' '.join(filter(rx_mail.match, sender))
		#print('sender: '+sender)
		command = ' '.join(filter(self.rx_subject.match, lines)).lower().replace('subject: ','').strip()
		
		print('cmd: ' + command)
		#x = raw_input('|sender cmd')
		#writeState(pageTemplate, msgnum)
		doSend = False
		sendOk = False
		hasCommand = False
		
		# collection list for stuff to send
		contents = []
		if command == 'help':
			contents.append(self.processHelp(sender))
			doSend = True
			hasCommand = True
			
		elif command == 'request':
			contents = self.processRequest(lines)
			doSend = True
			hasCommand = True
			
		elif command == 'register':
			hasCommand = True
			
			resultRegistration = self.processRegistration(sender, lines)
			if resultRegistration == None:
				#TODO: nice mail template
				contents.append('succesfully registered')
			else:
				contents.append('registration failed\n' + resultRegistration)
				
			doSend = True
			
		if doSend == True:
			for content in contents:
				#sendOk = self._pSend.send(sender, '\n<hr>\n'.join(contents) )
				sendOk = self._pSend.send(sender, content)
				
		if hasCommand == False or (doSend == True and sendOk == True):
			self.removeMail(mailFile)


if __name__ == "__main__":
	# process a single mail file (with multiple contents)
	# WITHOUT loading it (only files that already exist in the "mails" folder!
	
	import time
	startTime = time.time()
	na = newAgora()
	na.process()
	print("duration: " + str(time.time() - startTime) )

