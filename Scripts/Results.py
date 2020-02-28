import csv
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import scipy


raw1 = pd.read_csv("./Test2/Raw.csv")
raw2 = pd.read_csv("./Test1/Results.csv")
overall = pd.concat((raw1, raw2), axis=0, ignore_index=True)
results = overall[["WorkTimeInSeconds", "Input.claim", "Input.score", "Input.granule"]]
scores = overall["Answer.taskAnswers"]

mean_work_time = results["WorkTimeInSeconds"].mean(axis=0)
median_work_time = results["WorkTimeInSeconds"].median(axis=0)


responses = np.zeros((360,7))
for i in results.index:	
	dict = json.loads(scores.iloc[i])[0]

	row = []
	for x in dict:
		rankings = dict[x]
		for y in rankings:
			if rankings[y] == True:
				row.append(y)
				break

	responses[i] = row


responses = pd.DataFrame(responses, columns=["conflict",
											"economic_relevance",
											"magnitude",
											"personal_relevance",
											"political_relevance",
											"public_relevance",
											"surprise"])

column_total = responses.sum(axis=0)
column_mean = responses.mean(axis=0)
row_total = responses.sum(axis=1)
row_mean = responses.mean(axis=1)


combined = pd.concat([results, responses, row_total, row_mean], axis=1)
totals = combined.sum(axis=0, numeric_only=True)
totals = combined.append(totals, ignore_index=True)

combined = combined.rename(columns={"Input.claim": "Claim", "Input.score": "Score", "Input.granule": "Context", 0: "Total", 1: "Mean of Ratings"})
aggregate = combined.groupby(["Claim", "Context"], as_index=False).mean()
aggregate.to_csv("Analysis.csv", index=False)

pearson = np.zeros((8, 2))
i = 0
for category in ["conflict",
				"economic_relevance",
				"magnitude",
				"personal_relevance",
				"political_relevance",
				"public_relevance",
				"surprise",
				"Mean of Ratings"]:

	p = scipy.stats.pearsonr(aggregate["Score"], aggregate[category])
	pearson[i] = p 
	i += 1

pearson = pd.DataFrame(pearson, index=["conflict",
									   "economic_relevance",
										"magnitude",
										"personal_relevance",
										"political_relevance",
										"public_relevance",
										"surprise",
										"Mean of Ratings"],
								columns=["Pearson Coefficient", "p-value"])

pearson.to_csv("Statistics.csv")












## Graphing

#sns.scatterplot(x="Score", y="Mean of Ratings", hue="Claim", legend=False, data=aggregate)
#sns.regplot(x="Score", y="Mean of Ratings", data=aggregate)
#x = np.linspace(0, 1)
#y = np.linspace(1, 5)
#sns.lineplot(x, y)
sns.distplot(aggregate["Score"])
plt.savefig("Score distribution.png")








