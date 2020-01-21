import pygsheets
import datetime
import pandas as pd
import requests
import time

df = pd.DataFrame()
d = datetime.datetime.today().strftime("%B %d, %Y") #Example: January 20, 2020
link = "https://idir.uta.edu/factchecker/score_text/{" #Starting point of the request API link

title = d + ".txt" #Name of the file will be in the format January XX, 2020.txt
claims = [] #Creating arrays to be used later
scores = []

f = open(title, "r") #Opens file

for x in f:
    x = x.rstrip() #Gets rid of \n
    claims.append(x) #Adds to claims list
    claimScore = link + x + "}" #Finishes the link
    #print(claimScore)
    response = requests.get(claimScore) #Sends the request to API
    #print(response)
    obj = response.json()
    final = obj['results'][0]['score'] #Retrieves the score
    scores.append(final) #Adds to score array
    time.sleep(2) #Make sure we're not treating the API too harshly

df['Claims'] = claims #Sets in dataframe
df['Scores'] = scores

gc = pygsheets.authorize(service_file='/Users/andre/PycharmProjects/SpacyTest/ClaimSpotting-76d810d48572.json') #Authorizes the use of Sheets API

api_key='AIzaSyDFYwDLiwJklXOf-w2hTLtNFwZufKWCrhk'

headers = {'Authorization': 'Bearer %s' % api_key}

sh = gc.open('Claim') #Opens the sheet we are using, called 'Claim'
current = sh.add_worksheet(title=d) #Adds a new worksheet for that day
current.set_dataframe(df, (1, 1)) #Adds dataframe info

