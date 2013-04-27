#!/usr/bin/python

import recieveMail
import processing
import time
import configLoader

while True:
	print('###### ' + time.strftime("%d.%m.%y %H:%M:%S") + ' ######')
	nAgora = processing.newAgora()
	recMail = recieveMail.mailMon()
	
	recMail.getMails()
	
	while nAgora.hasMails() == True:
		print(time.strftime("%d.%m.%y %H:%M:%S") + 'next mail')
		nAgora.process()
	
	time.sleep(configLoader.conf.getValue('daemonDelay'))
