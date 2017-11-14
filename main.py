# -*- coding: utf-8 -*-
import sre, urllib2, sys, BaseHTTPServer, smtplib
from smtplib import SMTP_SSL
import datetime
from time import sleep
from config import *

def parseAddress(input):
        if input[:7] != "http://":
                if input.find("://") != -1:
                        print "Error: Cannot retrive URL, address must be HTTP"
                        sys.exit(1)
                else:
                        input = "http://" + input
        return input


def retrieveWebPage(ADDRESS):
        try:
                web_handle = urllib2.urlopen(ADDRESS)
        except urllib2.HTTPError, e:
                error_desc = BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
                print "Cannot retrieve URL: HTTP Error Code", e.code
                sys.exit(1)
        except urllib2.URLError, e:
                print "Cannot retrieve URL: " + e.reason[1]
                sys.exit(1)
        except:
                print "Cannot retrieve URL: unknown error"
                sys.exit(1)
        return web_handle

def mailsend():
    debuglevel = 1
    smtp = SMTP_SSL()
    smtp.set_debuglevel(debuglevel)
    smtp.connect(SMTP_ADDR, SMTP_PORT)
    smtp.login(SMTP_LOGIN, SMTP_PASSWORD)
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    message_text = MAIL_MSG_BODY
    msg = ("From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s"
            % (FROM_FIELD, TO_ADDRESS, SUBJ, date, message_text))

    smtp.sendmail(FROM_FIELD, TO_ADDRESS, msg)
    smtp.quit()

website_handle = retrieveWebPage(ADDRESS)
website_text = website_handle.read()
matches = sre.findall(WORD, website_text)

#DEBUG
# if matches:
#     print MSG_IF_MATCH
# else:
#     print MSG_IF_NOT_MATCH

finish = False

while not finish:
    if matches:
        # print MSG_IF_MATCH
        mailsend()
        finish = True
    else:
        sleep(DELAY_CHECK)
