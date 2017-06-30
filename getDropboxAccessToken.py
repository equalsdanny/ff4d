#!/usr/bin/python
# Copyright (c) 2014 Sascha Schmidt <sascha@schmidt.ps>
# Copyright (c) 2017 Danylo Vashchilenko <dan.vashchilenko@gmail.com> (contributor)
# http://blog.schmidt.ps
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
import sys, json, urllib, urllib2, httplib, dropbox
import requests

print ""
print "********************************************************************************"
print "* This script helps you to fetch an access token for your Dropbox application. *"
print "*                                                                              *"
print "* Copyright 2014 by Sascha Schmidt <sascha@schmidt.ps>                         *"
print "* http://blog.schmidt.ps                                                       *"
print "********************************************************************************"
print ""

app_key = raw_input("1.) Enter your 'App key': ").strip()
app_secret = raw_input("2.) Enter your 'App secret': ").strip()
authorize_url = "https://www.dropbox.com/oauth2/authorize?response_type=code&client_id=" + app_key

print "3.) Now open this url and confirm the requested permission."
print ""
print authorize_url
print ""
code = raw_input("4.) Enter the given access code': ").strip()

try:
  args = {"code"          : code,
          "grant_type"    : "authorization_code",
          "client_id"     : app_key,
          "client_secret" : app_secret}
  result = requests.post("https://api.dropboxapi.com/oauth2/token", data=args)
  access_token = result.json()['access_token']
  headers = {'Authorization' : 'Bearer ' + access_token}
except Exception, e:
  print "Could not finish the Dropbox authorization flow. (" + str(e) + ")\n"
  sys.exit(-1)

print ""
print "This access token allows your app to access your dropbox:"
print access_token
print ""

# Validate the access_token and show some user informations.
try:
  response = requests.post('https://api.dropboxapi.com/2/users/get_current_account', headers=headers)
  account_info = response.json()
  response = requests.post('https://api.dropboxapi.com/2/users/get_space_usage', headers=headers)
  space_usage = response.json()
except Exception, e:
  print "Could not validate the new access token. (" + str(e) + ")\n"
  sys.exit(-1)

print "- Your account -"
print "ID             : " + account_info['account_id']
print "Display name   : " + account_info['name']['display_name']
print "Email          : " + account_info['email']
print "Country        : " + account_info['country']
print "Referral link  : " + account_info['referral_link']
print "Space used     : " + str(space_usage['used']/1024/1024/1024) + " GB"
print "Space allocated: " + str(space_usage['allocation']['allocated']/1024/1024/1024) + " GB"
print ""
