## silly script that I wrote before I knew about ffuf's recursive features.

import requests

def appendURL(base,page):
	return base+page

pageList=[]
baseUrl = 'http://metadata.services.cityinthe.cloud:1338/'


for i in range(5): # get up to a depth of 5
	response = requests.get(url)
	if response.status_code == 200:
		lastResponse=response.text.splitlines()
		print(lastResponse)
		for j in lastResponse:

	else:
		print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
