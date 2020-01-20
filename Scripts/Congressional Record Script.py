import requests
import json
import sys 
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from datetime import date



def main():

	### Helper function to get the HTML link for a granule given its summary link
	def getHTM(link):
		r = requests.get(link)
		o = r.json()
		download = o.get("download")
		txtLink = download.get("txtLink")
		return txtLink


	house = []
	senate =[]


	### Pulls the most recent issue of the CR everyday
	today = date.today().strftime("%Y-%m-%d")
	print(today)
	api_key = "lZhfHdqsylDdCK7Rkb8v7BArGTrOcpUQCZ8ZQGU7"
	startDate = today+"T00:00:00Z"

	packageParameters = {
	    "api_key": api_key,
	    "offset": 0,
	    "pageSize": 10
	}

	granuleParameters = {
		"api_key": api_key,
	    "offset": 0,
	    "pageSize": 200
	}

	

	response = requests.get("https://api.govinfo.gov/collections/CREC/"+startDate, params=packageParameters)

	print("Status Code: "+str(response.status_code))
	object = response.json()


	# We want to pull 1 new record per day to analyze
	# Congress doesn't always meet so there could be days of 0 new records
	if object.get("count") == 0:
		print("No record for the day")
		return
	if object.get("count") == 1:
		print("Got the record for the day!")
	else:
		print("Error: More than 1 record pulled")
		return


	packages = object.get("packages")
	packageID = packages[0].get("packageId")




	### Pulls the list of granules for the congressional issue
	### Adds each HOUSE and SENATE item to the respective list
	response = requests.get("https://api.govinfo.gov/packages/"+packageID+"/granules", params=granuleParameters)

	print("Status Code: "+str(response.status_code))
	object = response.json()

	count = object.get("count")
	print("Granule Total: "+str(count))

	granules = object.get("granules")

	for g in granules:
		granuleClass = g.get("granuleClass")
		granuleLink = g.get("granuleLink")+"?api_key="+api_key
		txtLink = getHTM(granuleLink)+"?api_key="+api_key			
		request = requests.get(txtLink)
		html = request.text
		soup = BeautifulSoup(html, "html.parser")
		text = soup.text

		if (granuleClass) == "HOUSE":			
			house.append(text)		
			continue
		if (granuleClass) == "SENATE":			
			senate.append(text)
			continue

	#print(house[10])




if __name__ == "__main__":
	main()

