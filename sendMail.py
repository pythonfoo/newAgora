import smtplib
import random
import time
import configLoader

class pageSender(object):
	def __init__(self):
		#http://de.wikipedia.org/wiki/Header_(E-Mail)
		#http://docs.python.org/library/email-examples.html
		#http://docs.python.org/library/smtplib.html
		self.smtpServer = configLoader.conf.getValue('smtpServer') 
		self.smtpUser = configLoader.conf.getValue('smtpUser')
		self.smtpPassword = configLoader.conf.getValue('smtpPass')
		self.smtpSender = configLoader.conf.getValue('smtpSender')
		self.smtpTls = configLoader.conf.getValue('smtpTls') # True
		self.smtpAuth = configLoader.conf.getValue('smtpAuth') # True
	
		# for random subject, just do it once!
		#32
		#65-90
		#97-122
		self.sequenze = []#['a', 'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p', ' ', ' ']
		self.sequenze.append(' ')
		self.sequenze.append(' ')
		
		for i in range(65, 90):
			self.sequenze.append(chr(i))
			
		for i in range(97, 122):
			self.sequenze.append(chr(i))
	
	def getHeader(self, reciepient):
		#reply-to
		
		# create random subjects, just because we can ;)
		subject = ''
		for i in range(random.randint(4, 16)):
			subject += random.choice(self.sequenze)
		
		message = ''
		#'Date: Mon, 4 Dec 2006 15:51:37 +0100' + '\n'
		message += time.strftime("Date: %a, %d %b %Y %H:%M:%S") + '\n'
		message += 'From: ' + self.smtpSender + '\n'
		message += 'To: ' + reciepient + '\n'
		message += 'MIME-Version: 1.0' + '\n'
		message += 'Content-type: text/html; charset=UTF-8' + '\n'
		message += 'Subject: ' + subject + '\n'
		message += '\n'
		
		return message
	
	def send(self, reciepient, content):
		try:
			print('reciepient: ' + reciepient)
			message =  self.getHeader(reciepient) + content

			session = smtplib.SMTP(self.smtpServer)
			#session.set_debuglevel(1)
			if self.smtpTls == True:
				session.starttls()
			else:
				session.connect()
			
			# if your SMTP server doesn't need authentications,
			# you don't need the following line:
			if self.smtpAuth == True:
				session.login(self.smtpUser, self.smtpPassword)
				
			session.sendmail(self.smtpSender ,reciepient , message)
			session.quit()
			return True
		except Exception, ex:
			print("Write Error 4 sender: " + str(ex))
			return False
