from Scraper import Scraper
from datetime import date, timedelta
import pickle


def main(day=date.today().strftime("%Y-%m-%d"), createNew=None):
	try:	
		pickle_in = open("scraper.pickle","rb")
		previous_scraper = pickle.load(pickle_in)
	except:
		pickle_in = None
		previous_scraper = None
	finally:
		if pickle_in != None:
			pickle_in.close()

	if createNew == None:
		createNew = (previous_scraper == None) or (previous_scraper.date != day)

	if createNew:
		print("Creating new scraper")
		try:
			scraper = Scraper(day)
			pickle_out = open("scraper.pickle","wb")
			pickle.dump(scraper, pickle_out)
			pickle_out.close()
		except:
			print("Error creating scraper")
			scraper = previous_scraper
	else:
		print("Today's scraper already exists")
		scraper = previous_scraper


	samples = Scraper.sample(5, scraper.senateAll, True)


main()

	


