from Scraper import Scraper
from datetime import date, timedelta

def main(day=date.today(), exists=None):	
	scraper = Scraper(day, exists)	

	scraper.select("HOUSE", 25, scraper.yesterday, "house_3.csv", True)


main(exists=False)

	


