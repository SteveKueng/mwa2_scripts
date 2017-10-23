#!/usr/bin/env python
""" munkiwebadmin utils.py """

import subprocess
import urllib2
import requests
from Foundation import *


BUNDLE_ID = 'com.github.stevekueng.munkiwebadmin'

class GurlError(Exception):
    pass

class HTTPError(Exception):
    pass

def set_pref(pref_name, pref_value):
    """Sets a preference, writing it to
        /Library/Preferences/com.github.stevekueng.munkiwebadmin.plist.
        This should normally be used only for 'bookkeeping' values;
        values that control the behavior of munki may be overridden
        elsewhere (by MCX, for example)"""
    try:
        CFPreferencesSetValue(
            pref_name, pref_value, BUNDLE_ID,
            kCFPreferencesAnyUser, kCFPreferencesCurrentHost)
        CFPreferencesAppSynchronize(BUNDLE_ID)
    except Exception:
        pass

def pref(pref_name):
    """Return a preference. Since this uses CFPreferencesCopyAppValue,
    Preferences can be defined several places. Precedence is:
        - MCX
        - /var/root/Library/Preferences/com.github.stevekueng.munkiwebadmin.plist
        - /Library/Preferences/com.github.stevekueng.munkiwebadmin.plist
        - default_prefs defined here.
    """
    default_prefs = {
        'ServerURL': 'http://munkiwebadmin',
        'authKey': '',
    }
    pref_value = CFPreferencesCopyAppValue(pref_name, BUNDLE_ID)
    if pref_value is None:
        pref_value = default_prefs.get(pref_name)
        # we're using a default value. We'll write it out to
        # /Library/Preferences/<BUNDLE_ID>.plist for admin
        # discoverability
        set_pref(pref_name, pref_value)
    if isinstance(pref_value, NSDate):
        # convert NSDate/CFDates to strings
        pref_value = str(pref_value)
    return pref_value

def send_data(url, data):
    s = requests.Session()
    s.headers.update({'Authorization': pref('authKey')})
    response = s.post(pref('ServerURL') + url, data=data)
    response.connection.close()
    return response

def mwa_available():
    """ check if server available """
    try:
        urllib2.urlopen(pref('ServerURL'), timeout=1)
        return True
    except urllib2.HTTPError, e:
        if str(e.code) == "401":
            return True
        else:
            return False
    except urllib2.URLError as err: 
        return False

def get_comnputer_name():
    '''Uses system profiler to get hardware info for this machine'''
    cmd = ['/usr/sbin/scutil', '--get', 'ComputerName']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, dummy_error) = proc.communicate()
    return output