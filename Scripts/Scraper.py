import requests
import json
import string
import csv
import numpy as np
import sys 
import nltk
#nltk.download('punkt')
import re
from nltk.tokenize import sent_tokenize
import spacy
from textblob import TextBlob
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from datetime import date, timedelta

class Scraper:

	api_key = "lZhfHdqsylDdCK7Rkb8v7BArGTrOcpUQCZ8ZQGU7"

	## Everything is done on initialization
	def __init__(self, date):
		self.house = []
		self.senate = []

		self.houseContext = []
		self.senateContext = []

		self.houseNewsInsert = []
		self.senateNewsInsert = []

		self.houseLinks = []
		self.senateLinks = []

		self.houseScore = None
		self.senateScore = None

		self.houseAll = None
		self.senateAll = None

		self.date=date
		
		### Set parameters to use api URL	
		date, packageParameters, granuleParameters = self.setParameters(date)	
		
		### Pulls the entire package containing the Congressional Record for the day
		packageID = self.pullRecord(date, packageParameters)
		
		### Pulls the list of granules for the congressional issue
		granules = self.pullGranules(packageID, granuleParameters)

		### Adds each HOUSE and SENATE item to the respective list
		self.addSentences(granules)

		### Score all the sentences
		self.scoreAll()

		### Combine arrays for output
		self.stackAll()

		print("Scraper Created")


	## Gets the html link for the given granule link
	@staticmethod
	def getHTM(link):
		r = requests.get(link)
		o = r.json()
		download = o.get("download")
		txtLink = download.get("txtLink")
		return txtLink

	## Gets the pdf link for the given pdf link
	@staticmethod
	def getPDF(link):
		r = requests.get(link)
		o = r.json()
		download = o.get("download")
		pdfLink = download.get("pdfLink")
		return pdfLink

	## Sets the day, api key, and params to use for requests
	@staticmethod
	def setParameters(day):		
		print("Date: "+day)
		api_key = Scraper.api_key	
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

		return startDate, packageParameters, granuleParameters


	## Pull the record for the given date
	@staticmethod
	def pullRecord(date, param):
		print("https://api.govinfo.gov/collections/CREC/"+date+"?offset=0&pageSize=1&api_key="+Scraper.api_key)
		response = requests.get("https://api.govinfo.gov/collections/CREC/"+date, params=param) #Gets a list of Congressional Record issues given the date

		print("Status Code: "+str(response.status_code)) #200 means no error occurred
		object = response.json() #Returns api response as a json object


		# We want to pull 1 new record per day to tokenize
		# Congress doesn't always meet so there could be days of 0 new records
		if object.get("count") == 0:
			print("No record for the day")
			raise Exception()
			return
		if object.get("count") != 1 and param["pageSize"] != 1:
			print("Error: More than 1 record pulled")
			raise Exception()		
			return
		else:
			print("Got the record for the day!")		


		packages = object.get("packages") #Gets list of packages from the json object - should only be one
		packageID = packages[0].get("packageId")

		return packageID


	## Get all the granules for the given package
	@staticmethod
	def pullGranules(package, param):
		response = requests.get("https://api.govinfo.gov/packages/"+package+"/granules", params=param)

		print("Status Code: "+str(response.status_code)) # 200 means no error occurred
		object = response.json()

		count = object.get("count")
		print("Granule Total: "+str(count))

		granules = object.get("granules")
		print("https://api.govinfo.gov/packages/"+package+"/granules?api_key=lZhfHdqsylDdCK7Rkb8v7BArGTrOcpUQCZ8ZQGU7&offset=0&pageSize=200")

		return granules


	## Iterate through the granule list and add sentences, context, inserts, and links to house and senate
	def addSentences(self, granules):		
		if len(self.house) != 0 or len(self.senate) != 0:
			print("Sentences already added")
			return		

		for g in granules:
			granuleClass = g.get("granuleClass") #check if it's house or senate
			granuleLink = g.get("granuleLink")+"?api_key="+Scraper.api_key #get the link to be able to view the contents
			pdfLink = self.getPDF(granuleLink)+"?api_key="+Scraper.api_key #save the pdf link for the final deliverable
			txtLink = self.getHTM(granuleLink)+"?api_key="+Scraper.api_key #view the content in html format to make parsing easier	
			request = requests.get(txtLink) 
			html = request.text #gets the text of the granule in html format		
			soup = BeautifulSoup(html, "html.parser") #removes the html tags with parser		
			raw = soup.text.replace("\n", "") #removes extra line breaks
			text = re.sub(" +", " ", raw) #removes extra white space


			if (granuleClass) == "HOUSE":

				sentences = sent_tokenize(text) #split into sentences
				del sentences[0] #Remove header section for each granule
				
						

				for s in sentences: 				
					#res = len(re.findall(r'\w+', s))
					res = sum([i.strip(string.punctuation).isalpha() for i in s.split()]) #length filter to remove all sentences 5 words or less
					#res = len(s.split())
					match = self.filter(s)
					if res > 6 and match == None:
						self.house.append(s)
						context, insert = Scraper.cutContext(s, sentences) #Keep the context 5 sentences before and after and add shorter excerpts for newsletter
						context = "".join(context) #Combine back into 1 string	
						insert = "".join(insert) #Combine back into 1 string														
						self.houseContext.append(context)
						self.houseNewsInsert.append(insert)
						self.houseLinks.append(pdfLink)
				

			if (granuleClass) == "SENATE":	
				sentences = sent_tokenize(text) #split into sentences
				del sentences[0] #Remove header section for each granule
				
				
				
				for s in sentences: 
					#res = len(re.findall(r'\w+', s))
					res = sum([i.strip(string.punctuation).isalpha() for i in s.split()]) #length filter to remove all sentences 5 words or less
					#res = len(s.split())
					match = self.filter(s)
					if res > 6 and match == None:
						self.senate.append(s)
						context, insert = Scraper.cutContext(s, sentences) #Keep the context 5 sentences before and after and add shorter excerpts for newsletter
						context = "".join(context) #Combine back into 1 string
						insert = "".join(insert) #Combine back into 1 string
						self.senateContext.append(context)
						self.senateNewsInsert.append(insert) 
						self.senateLinks.append(pdfLink)


	## Filter unnecessary sentences based on regular expression matches and other heuristics
	@staticmethod
	def filter(sentence):
		# Filters out a sentence mostly mentioning people (over 50% of the sentence)
		nlp = spacy.load("en_core_web_sm")

		doc = nlp(sentence)
		blob = TextBlob(sentence)

		length = len(blob.words)


		count = 0
		for ent in doc.ents:
			if ent.label_ == "PERSON":
				count += 2
		if length != 0 and count/length > 0.50:
			return count 

		# Filter out sentences with all upper case letters
		if sentence.isupper():
			return sentence

		# Filter out sentences with excessive periods
		if len(sentence) != 0 and sentence.count(".")/len(sentence) > 0.2:
			return sentence

		# Filters out interrogative sentences that end in question marks
		if sentence[-1] == "?":
			return sentence


		# Filters by regular expression matches for unnecessary 
		expressions = ("Congressional Record, Volume ",
						"Congress has the power to enact",
						"A bill to",
						"By Mr.",
						"By Ms.",
						"By Mrs.",
						"A letter from the ",
						"A bill to ",
						"The bill",
						"This bill",
						"An act to ",
						"Madam Speaker",
						"The Chair",
						"Is there objection",
						"Pursuant to clause",
						"Under clause",
						"Section \d",
						"\{",
						"``",
						"\[\[",
						"\(",
						"\d",
						"\d:", 
						"\d\d:", 
						"\d\d\d:", 
						"\d\d\d\d:")	

		for e in expressions: 			
			match = re.match(e, sentence)
			if match != None:
				break

		return match


	## If possible keep the context to 5 sentences before and after the given sentence
	## Adds an excerpt to be used for newletter that's 1 sentence before and 1 sentence after
	@staticmethod
	def cutContext(sentence, text):
		i = text.index(sentence)
		length = len(text)

		if (i - 5) >= 0 and (i + 5) < length:
			short = text[i-5:i+5]
			shorter = text[i-1:i+1]

		if (i - 5) < 0 and (i + 5) < length:  #If sentence is close to the beginning
			short = text[:i+5]
			if (i - 1) < 0:
				shorter = text[:1+1]
			else:
				shorter = text[i-1:i+1]

		if (i - 5) >= 0 and (i + 5) >= length: #If sentence is close to the end
			short = text[i-5:]
			if (i + 1) >= length:
				shorter = text[i-1:]
			else:
				shorter = text[i-1:i+1]
		else:                                  #If text is too short                             
			short = text

			if (i - 1) >= 0 and (i + 1) < length: 				
				shorter = text[i-1:i+1]

			if (i - 1) < 0 and (i + 1) < length: #If sentence is the first sentence
				shorter = text[:i+1]				

			if (i - 1) >= 0 and (i + 1) >= length: #If sentence is the last sentence
				shorter = text[i-1:]
				
			else:
				shorter = text #If there's just 1 sentence


		return short, shorter



	## Gets score for the given sentence
	@staticmethod
	def score(sentence):	
		link = "https://idir.uta.edu/claimbuster/API/score/text/"+sentence
		response = requests.get(link)

		if response.status_code == 200:
			object = response.json()
			score = object["results"][0].get("score")		
			return score

	## Scores all the sentences
	def scoreAll(self):
		if self.houseScore != None or self.senateScore != None:
			print("Sentences already scored")
			return

		scores = np.vectorize(Scraper.score) #Applies score function to a vector


		if len(self.house) != 0:
			house = np.asarray(self.house)			
			self.houseScore = scores(house) #Get scores	
				

		if len(self.senate) != 0:
			senate = np.asarray(self.senate)	
			self.senateScore = scores(senate) #Get scores
			

	## Stacks the sentences, scores, contexts, inserts, and links into 1 array
	def stackAll(self):
		if self.houseAll != None or self.senateAll != None:
			print("Array already created")
			return

		self.house = np.asarray(self.house)
		self.senate = np.asarray(self.senate)
		self.houseContext = np.asarray(self.houseContext)
		self.senateContext = np.asarray(self.senateContext)
		self.houseNewsInsert = np.asarray(self.houseNewsInsert)
		self.senateNewsInsert = np.asarray(self.senateNewsInsert)
		self.houseLinks = np.asarray(self.houseLinks)
		self.senateLinks = np.asarray(self.senateLinks)		

		self.houseAll = np.stack((self.house, self.houseScore, self.houseContext, self.houseNewsInsert, self.houseLinks), axis=1)
		self.senateAll = np.stack((self.house, self.houseScore, self.houseContext, self.senateNewsInsert, self.senateLinks), axis=1)
		


	## Create 2 text files with a new sentence per line
	@staticmethod
	def writeFiles():
		yesterday = (date.today() - timedelta(days=1)).strftime("%B %d, %Y")
		f = open(yesterday + "-SENATETEST" + ".txt", "w+")
		f.writelines("%s\n" % item for item in self.senate)
		f.close()

		f = open(yesterday + "-HOUSETEST" + ".txt", "w+")
		f.writelines("%s\n" % item for item in self.house)
		f.close()


	## Sample a batch of sentencees for crowdsourcing
	@staticmethod 
	def sample(size, a, fileName, createFile=False):		
		scores = a[:, 1].astype("float")		

		first = a[scores < 0.25]		
		indices1 = np.random.choice(first.shape[0], size, False)
		first = first[indices1]

		second = a[(scores > 0.25) & (scores < 0.5)]		
		indices2 = np.random.choice(second.shape[0], size, False)
		second = second[indices2]

		third = a[(scores > 0.5) & (scores < 0.75)]		
		indices3 = np.random.choice(third.shape[0], size, False)
		third = third[indices3]

		fourth = a[scores > 0.75]		
		indices4 = np.random.choice(fourth.shape[0], size, False)
		fourth = fourth[indices4]

		samples = np.vstack((first, second, third, fourth))
		formatted_context = Scraper.format(samples)
		samples[:, 2] = formatted_context

		if createFile:		
			with open(fileName+'.csv', 'w', newline='') as f:
				fields = ["claim", "score", "granule", "pdfLink"]				
				writer = csv.writer(f)
				writer.writerow(fields)
				writer.writerows(samples)

		return samples

	#Adds a bold tag to the sentence within the context
	@staticmethod
	def format(samples):
		formatted = []

		for i in range(samples.shape[0]):
			split = str(samples[i, 2]).split(str(samples[i, 0]))
			bolded = "<strong>"+samples[i, 0]+"</strong>"
			split.insert(1, bolded)
			joined = "".join(split)			
			formatted.append(joined)
		

		formatted = np.asarray(formatted)

		return formatted


	

		





