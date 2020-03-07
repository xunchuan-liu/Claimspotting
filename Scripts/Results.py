import csv
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

class Results:

	## CSV file is read and relevant fields are pulled
	def __init__(self, fileName):
		self.raw = pd.read_csv(fileName)

		self.results = self.raw[["WorkTimeInSeconds", "Input.claim", "Input.score", "Input.granule"]] # Input data plus the work time		
		self.responses = np.zeros((self.results.shape[0],7)) # Where we're gonna store the scores by each category

		self.aggregate = None # Where we're gonna store the responses output
		self.pearson = np.zeros((8, 2)) # Where we're gonna store the pearson coeffs and p-values

		self.mean_work_time = self.results["WorkTimeInSeconds"].mean(axis=0)
		self.median_work_time = self.results["WorkTimeInSeconds"].median(axis=0)


	## Updates responses with what workers scored
	def get_responses(self):
		scores = self.raw["Answer.taskAnswers"] #Dictionaries of all the worker responses

		for i in self.results.index:	
			dictionary = json.loads(scores.iloc[i])[0]

			row = [] #Appends the rating for every category for a single user
			for x in dictionary:
				rankings = dictionary[x] # Key for the category
				for y in rankings:
					if rankings[y] == True: #Key for the rating from 1-5 user gave
						row.append(y)
						break

			self.responses[i] = row

		#Updates self.responses into DataFrame
		self.responses = pd.DataFrame(self.responses, columns=["conflict",
																"economic_relevance",
																"magnitude",
																"personal_relevance",
																"political_relevance",
																"public_relevance",
																"surprise"]) 

	## Combines the data into a single results spreadsheet
	def combine(self, toCSV=False):			
		row_mean = self.responses.mean(axis=1) # Gets the mean for every row - by user

		combined = pd.concat([self.results, self.responses, row_mean], axis=1) # Combines our input data, task answers, and means
		combined = combined.rename(columns={"Input.claim": "Claim", "Input.score": "Score", "Input.granule": "Context", 0: "Mean of Ratings"})
		self.aggregate = combined.groupby(["Claim", "Context"], as_index=False).mean() #Aggregates by claim by averaging all user responses

		column_mean = self.aggregate.mean(axis=0, numeric_only=True) # Gets the mean for every column - by category
		self.aggregate = self.aggregate.append(column_mean, ignore_index=True)
		self.aggregate = self.aggregate.rename(index={(len(self.aggregate.index)-1): "Mean by Category"}) # Rename column mean

		if toCSV:
			self.aggregate.to_csv("Responses.csv", index=False)


	## Gets the pearson coeff and p-value for each category
	def get_pearson(self, toCSV=False):		
		i = 0
		for category in ["conflict",
						"economic_relevance",
						"magnitude",
						"personal_relevance",
						"political_relevance",
						"public_relevance",
						"surprise",
						"Mean of Ratings"]:

			p = scipy.stats.pearsonr(self.aggregate["Score"], self.aggregate[category]) #Calculates pearson coeff and p-value for each category
			self.pearson[i] = p 
			i += 1

		self.pearson = pd.DataFrame(self.pearson, index=["conflict",
												    "economic_relevance",
													"magnitude",
													"personal_relevance",
													"political_relevance",
													"public_relevance",
													"surprise",
													"Mean of Ratings"],
										columns=["Pearson Coefficient", "p-value"])

		if toCSV:
			self.pearson.to_csv("Correlation.csv")



	## Produce data visualizations from the results
	def Visualize(self):	
		sns.scatterplot(x="Score", y="Mean of Ratings", hue="Claim", legend=False, data=self.aggregate)
		sns.regplot(x="Score", y="Mean of Ratings", data=self.aggregate)
		#x = np.linspace(0, 1)
		#y = np.linspace(1, 5)
		#sns.lineplot(x, y)
		#sns.distplot(aggregate["Score"])
		plt.savefig("Scores vs Ratings.png")








