from Scraper import Scraper
from Results import Results
import requests
from datetime import date, datetime, timedelta	

## Runs the scraping for the day
def Scraping(day=date.today(), exists=None):
	scraper = Scraper(day, exists)
	scraper.selectBest()
	json = scraper.writeJSON()

	return json	

	#samples = scraper.sample("SENATE", 25, scraper.yesterday, "senate_3.csv", True)

## Runs the data analysis for the day
def Analyze(fileName, createFiles=False):
	results = Results(fileName)
	results.get_responses()
	results.combine(createFiles)
	results.get_pearson(createFiles)	
	results.Visualize()


Scraping()
Analyze("./Test3/Results_3.csv")
	


