#!/usr/bin/python
import email
msg = email.message_from_file(open('mails_back/1325988074.59.eml'))
print len(msg.get_payload())
attachment = msg.get_payload()[0]
print attachment.get_content_type()
print attachment.__dict__


#>>> open('attachment.png', 'wb').write(attachment.get_payload(decode=True))
