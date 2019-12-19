#!/usr/bin/env python3
#slack_api.py
#last update : Dec, 19 2019

import json
import requests
import urllib.parse
import datetime
import csv
import sys
import time

# Check arguments : 
if len(sys.argv) != 3:
	raise SystemExit('Usage: slack_api.py bu input.csv')


#init variables
app=''
id_channel=''
purpose=''
output_file=''
input_file=''
short_app=''
long_app=''
token_file='token.csv'
POST_auth=''
BU=''
#######

#read token
with open(token_file, newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
	for row in spamreader:	
		token=row[0]
POST_auth='Bearer ' + token
#######

# Get BU/PF
BU=sys.argv[1]

# Get input file
input_file=sys.argv[2]

# Get BU
BU=sys.argv[1]


#set output file 
date = datetime.datetime.now()
outputfile=str(date.year)+str(date.month)+str(date.day)+str(date.hour)+str(date.minute)+str(date.second)+'_output.csv'
########

# CHANNEL CREATION
def create_channel(bu, short_app, long_app):
	global id_channel #the function sets the channel_id, once created in slack 
	global purpose    #the function sets the purpose for the application

	main_api = 'https://slack.com/api/channels.create/'
	name='tc_'+BU+'_'+ short_app + '_i'
	purpose='This channel is used to set the migration target of the application "' + long_app + '" in the context of the All in public cloud in 2022 goal'
	url = main_api + '?' + urllib.parse.urlencode({'token': token}) + '&' + urllib.parse.urlencode({'name': name})
	print(url)
	resp = requests.get(url)
	if resp.status_code != 200:
		print(resp.status_code)
	json_data=resp.json()
	print(json_data)

	id_channel = json_data['channel']['id']
	print('id_channel:'+id_channel)

	
# SET PURPOSE
def set_purpose(channel, purpose):
	main_api = 'https://slack.com/api/channels.setPurpose/'
	url = main_api + '?' + urllib.parse.urlencode({'token': token}) + '&' + urllib.parse.urlencode({'channel': id_channel}) + '&' + urllib.parse.urlencode({'purpose': purpose})
	r = requests.get(url)
	if r.status_code != 200:
		print(r.status_code)

	json_data=r.json()
	print(json_data)


def create_csv(file):
	with open(file, 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';',quotechar=';', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['app', 'id_channel'])

def write_csv(file, app, id_channel):
	with open(file, 'a', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';',quotechar=';', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow([app, id_channel])

#POST explanation message 
def post_explanation_msg(channel, text):
	url = 'https://slack.com/api/chat.postMessage'
	payload = {
			'channel':channel,
			"text":text
			}
	headers = {'content-type': 'application/json', 'Authorization':POST_auth}
	response = requests.post(url, data=json.dumps(payload), headers=headers)

#

#MAIN
create_csv(outputfile)
with open(input_file, newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
	for row in spamreader:
		short_app=row[0]
		long_app=row[1]	
		create_channel(BU, short_app, long_app)
		write_csv(outputfile, long_app, id_channel)
		set_purpose(id_channel,purpose)
		msg_explanation = 'Hello, \n We are working on the DTP side at assisting platforms and BU on the migration to public cloud project.\n In this context, we use the Slack tool to define together a target and trajectory, with the use of a decision tree.\n This channel was created to handle the application '+long_app+' , as indicated in the channel name and for which you have been identified within Galax’Is as the « RA ».\n \n This process will take place in two stages \n 1.    Decide on the migration target for the application \n 2.    Collect the elements required to define the effort, resources and means to mobilize in order to reach the target set previously.\n\n Key information to be reported in the final assessment deliverable will be saved in the channel for an extraction. \n # Tags will be used to «mark» those decisions.\n\n Useful links \n Reference document describing the decision tree \n https://myadeo.sharepoint.com/:p:/t/-ADEO-DigitalTechLeadersCommunity/ESa_zFmlQbpEvTSjSxikIO0B95aHhKkNBg7niOycIMsRvQ?e=KWweEf \n General information: channel #tc_general \n For any general question on this initiative: channel #tc_help \n I suggest that you browse the up mentioned document and that we start right away with defining the criteria “business needs”.'
		post_explanation_msg(id_channel, msg_explanation)
		time.sleep(3)
	
