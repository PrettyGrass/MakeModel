#encoding:utf-8

import os
import shutil
import _protocol
import _config
import time

print ("Start Run!")
start_time = time.time()

android_path = os.path.join("", _config._android_folder);
ios_path = os.path.join("", _config._ios_folder);
php_path = os.path.join("", _config._php_folder);

# Delete folder
if(os.path.exists(android_path)):
    print ("Removing "+ android_path + "...")
    shutil.rmtree(android_path)

if(os.path.exists(ios_path)):
    print ("Removing "+ ios_path + "...")
    shutil.rmtree(ios_path)

if(os.path.exists(php_path)):
    print ("Removing "+ php_path + "...")
    shutil.rmtree(php_path)

# Create Android File folder
if not os.path.isdir(android_path):
    print ("Create "+ android_path + "...")
    os.makedirs(android_path)

if not os.path.isdir(ios_path):
    print ("Create "+ ios_path + "...")
    os.makedirs(ios_path)

if not os.path.isdir(php_path):
    print ("Create "+ php_path + "...")
    os.makedirs(php_path)

_protocol.do_search()

cost_time = time.time() - start_time

print ("Build success in " + bytes(cost_time) + "s !")