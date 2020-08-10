from flask import render_template
from app import app
import json
import pandas as pd
import io
import requests
import re

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSW8CE-R5JMsjnzFiDIMKtyko3pySxmAOESAR017msIYcAKeNR7FQIA1oaXh_xSlb9FaMBJhsjH-gfc/pub?output=csv"
s = requests.get(url).content
dfData = pd.read_csv(io.StringIO(s.decode('utf-8')))

@app.route('/')
@app.route('/index')
def index():
	some_data = {'username': 'Sean'}
	return render_template('index.html', data_that_we_put_in_the_template=some_data, title="Test page", data="Index Page")

@app.route('/statemap')
def statemap():
	jsData = ''
	return render_template('statemap.html', title="State Map", js_data=jsData)

	
@app.route('/reward-time')
def test():

	# dfDataHeadline = dfData['Headline'].iloc[:10]
	vDataOut = []
	for i in range(len(dfData)):
		sHeadline = dfData['Headline'].iloc[i]
		
		# Extract the reward amount
		tMatch = re.findall(r'(\d+)', sHeadline)
		if len(tMatch) > 0:
			fReward = int(tMatch[0])
			if sHeadline.lower().find('cent') >= 0:
				fReward = fReward / 100
		
			sDate = dfData['Date of advertisement'].iloc[i]
			iYear = int(sDate[:4])
			
			vDataOut.append({'reward': fReward, 'year': iYear})
			# dfDataOut['reward'].append(iReward)
			# dfDataOut['year'].append(iYear)
	
	jsData = json.dumps(vDataOut)
	
	
	
	return render_template('reward-time.html', title="Rewards over Time", js_data=jsData)

# use pandas to import the data from the google sheet
# https://docs.google.com/spreadsheets/d/e/2PACX-1vQX_EbjYR6hKnfLbnMNDxsbIO0D8edLfXYmGMf87JIGlWSzNSeZ7Mru2m-k2FI_sgRdLzOG0kzGgCdc/pub?output=csv
