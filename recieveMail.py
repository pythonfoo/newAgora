#!/usr/bin/python

import poplib
import sys
import re
import time
import configLoader

class mailMon(object):
	def __init__(self):
		self.popServer = configLoader.conf.getValue('popServer')
		self.popUser = configLoader.conf.getValue('popUser')
		self.popPass = configLoader.conf.getValue('popPass')
		self.mailDir = configLoader.conf.getValue('mailDir')
		self.pop3Ssl = configLoader.conf.getValue('pop3Ssl')

		# the number of message body lines to retrieve
		self.maxLines = configLoader.conf.getValue('maxLines')

		#rx_mail = re.compile('\b[A-Z0-9._-]+@[A-Z0-9][A-Z0-9.-]{0,61}[A-Z0-9]\.[A-Z.]{2,6}\b', re.IGNORECASE)

		pT = open('pageTemplate.html', 'r')
		self.pageTemplate = pT.read()
		pT.close

		self.logFile = open(configLoader.conf.getValue('logFile'), 'a')
		
	def writeLog(fHandle, text):
		fHandle.write(time.strftime("%d.%m.%y %H:%M:%S :") + text + '\n')
	
	def writeState(pageTemplate, inMailbox):
		try:
			pageHandle = open('state.html', 'w')
		
			pageTemplate = pageTemplate.replace('{inMailbox}', str(inMailbox))
		
			pageTemplate = pageTemplate.replace('{modDate}', time.strftime("%d.%m.%y %H:%M:%S"))
			pageTemplate = pageTemplate.replace('{totalMails}', 'n/a')
			pageTemplate = pageTemplate.replace('{totalPages}', 'n/a')
		
			pageHandle.write(pageTemplate)
			pageHandle.close()
		
		except Exception, ex:
			print("Write Error 4 State: " + str(ex))

	def writeMailFile(self, maildir, lines):
		pageHandle = open(maildir + str(time.time()) + '.eml', 'w')
		pageHandle.write('\n'.join(lines))
		pageHandle.close()	
		
	def getMails(self):
		#print('start')
		#try:
		if True == True:
			# connect to POP3 and identify user
			if self.pop3Ssl == True:
				pop = poplib.POP3_SSL(self.popServer)
			else:
				pop = poplib.POP3(self.popServer)
			
			pop.user(self.popUser)

			# authenticate user
			pop.pass_(self.popPass)

			# <strong class="highlight">get</strong> general information (msg_count, box_size)
			stat = pop.stat(  )

			# print some information
			#print("Logged in as %s@%s" % (popUser, popServer))
			#print("Status: %d message(s), %d bytes" % stat)

			bye = 0
			count_del = 0
			for n in range(stat[0]):
				msgnum = n+1
				print('******* ' + str(msgnum) + ' *******')
				# retrieve headers
				response, lines, bytes = pop.top(msgnum, self.maxLines)
				#print response
				print('####################')
				#for ln in lines:
				#	print ln
				self.writeMailFile(self.mailDir, lines)
				#x = raw_input('break')
				# print message info and headers you're interested in
				'''
				print("Message %d (%d bytes)" % (msgnum, bytes))
				print("-" * 30)
				print("\n".join(filter(rx_headers.match, lines)))
				print("-" * 30)
				'''
		
				pop.dele(msgnum)
				count_del += 1
	
			# summary
			if count_del > 0:
				print("Deleting %d message(s) in mailbox %s@%s" % (count_del, self.popUser, self.popServer))

			# close operations and disconnect from server
			#print("Closing POP3 session")
			pop.quit()
		'''
		except poplib.error_proto, detail:

			# possible error
			print("POP3 Protocol Error:", detail)
		except Exception, ex:
			print("Write Error4 global UNKNOWN: " + str(ex))
		'''

		#print('end')
