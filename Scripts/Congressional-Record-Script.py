import requests
import json
import sys 
import nltk
import re
from nltk.tokenize import sent_tokenize
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from datetime import date




def main(day=date.today().strftime("%Y-%m-%d")):

	### Helper function to get the HTML link for a granule given its summary link
	def getHTM(link):
		r = requests.get(link)
		o = r.json()
		download = o.get("download")
		txtLink = download.get("txtLink")
		return txtLink


	house = []
	senate =[]


	### Set parameters to use api URL	
	print("Date: "+day)
	api_key = "lZhfHdqsylDdCK7Rkb8v7BArGTrOcpUQCZ8ZQGU7"	
	startDate = day+"T00:00:00Z"

	packageParameters = {
	    "api_key": api_key,
	    "offset": 0,
	    "pageSize": 1
	}

	granuleParameters = {
		"api_key": api_key,
	    "offset": 0,
	    "pageSize": 200
	}

	
	### Pulls the entire package containing the Congressional Record for the day

	response = requests.get("https://api.govinfo.gov/collections/CREC/"+startDate, params=packageParameters) #Gets a list of Congressional Record issues given the date

	print("Status Code: "+str(response.status_code)) #200 means no error occurred
	object = response.json() #Returns api response as a json object


	# We want to pull 1 new record per day to tokenize
	# Congress doesn't always meet so there could be days of 0 new records
	if object.get("count") == 0:
		print("No record for the day")
		return
	if object.get("count") != 1 and packageParameters["pageSize"] != 1:
		print("Error: More than 1 record pulled")
		return
	else:
		print("Got the record for the day!")		


	packages = object.get("packages") #Gets list of packages from the json object - should only be one
	packageID = packages[0].get("packageId")




	### Pulls the list of granules for the congressional issue
	### Adds each HOUSE and SENATE item to the respective list

	response = requests.get("https://api.govinfo.gov/packages/"+packageID+"/granules", params=granuleParameters)

	print("Status Code: "+str(response.status_code)) # 200 means no error occurred
	object = response.json()

	count = object.get("count")
	print("Granule Total: "+str(count))

	granules = object.get("granules")

	for g in granules:
		granuleClass = g.get("granuleClass") #check if it's house or senate
		granuleLink = g.get("granuleLink")+"?api_key="+api_key #get the link to be able to view the contents
		txtLink = getHTM(granuleLink)+"?api_key="+api_key #view the content in html format to make parsing easier	
		request = requests.get(txtLink) 
		html = request.text #gets the text of the granule in html format		
		soup = BeautifulSoup(html, "html.parser") #removes the html tags with parser		
		raw = soup.text.replace("\n", "") #removes extra line breaks
		text = re.sub(" +", " ", raw) #removes extra white space


		if (granuleClass) == "HOUSE":
			sentences = sent_tokenize(text) #split into sentences

			for s in sentences: #length filter to remove all sentences 5 words or less
				res = len(re.findall(r'\w+', s))
				if res <= 5:
					sentences.remove(s)

			house.extend(sentences)			
			continue
		if (granuleClass) == "SENATE":	
			sentences = sent_tokenize(text) #split into sentences
			
			for s in sentences: #length filter to remove all sentences 5 words or less
				res = len(re.findall(r'\w+', s))
				if res <= 5:
					sentences.remove(s)
	
			senate.extend(sentences)
			continue

	
	## Create text files with each sentence as a line
	f = open("CR-"+day+"-SENATE"".txt", "w+")
	f.writelines("%s\n" % item for item in senate)
	f.close()

	f = open("CR-"+day+"-HOUSE"".txt", "w+")
	f.writelines("%s\n" % item for item in house)
	f.close()


if __name__ == "__main__":
	main()

