#!/usr/bin/python
#
# dBus Gnome notificator
# reads the mail from stdin and sends a dBus message
# for use with evolution or procmail
# From: http://oz4.org/
# License: public domain, do whatever you like - 
#          it would be nice if you could link back

import email
import email.Header
import pynotify
from sys import stdin

##
## C O N F I G
##
ms=10000  # time to display the alert, in ms
icon="email" # full path to icon OR gnome icon stock name, try 'email'
maxbody = 200 # max 200 chars in body
maxsubject = 50 # max 50 chars in subject
maxsender = 50 # max 50 chars for sender name
##
##

#pynotify will fail if there's an unknown tag...
def striptags(string):
    string = string.replace('&', '&amp;')
    string = string.replace('<', '&lt;')
    string = string.replace('>', '&gt;')
    string = string.replace('"', '&quot;')
    return string

s = stdin.read()
msg = email.message_from_string(s)

if msg.is_multipart():
    for part in msg.walk():
        if part.get_content_type()=="text/plain":
            body = " ".join(part.get_payload(None,True).splitlines())
else:
    body = " ".join(msg.get_payload(None, True).splitlines())
if len(body) > maxbody:
    body = body[:maxbody]
body = striptags(body)

msbsub = msg["subject"]
print msbsub, msg

subject = email.Header.decode_header(" ".join(msbsub.splitlines()))
subject = email.Header.make_header(subject)
subject = striptags(unicode(subject))
if len(subject)>maxsubject:
    subject = subject[:maxsubject]

sender = email.Header.decode_header( email.Utils.parseaddr(msg["from"])[0] )
sender = email.Header.make_header(sender)
sender = striptags(unicode(sender))
if len(sender)>maxsender:
    sender = sender[:maxsender]

title = "New mail from: " + sender
body = "<b>" + subject +"</b>\n<small>" + body + "</small>"

if pynotify.init("Notifier"):
    n = pynotify.Notification(title, body, icon)
    n.set_timeout(ms)
    n.show()
else:
    print "there was a problem with pynotify"
