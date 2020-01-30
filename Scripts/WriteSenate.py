import pygsheets
import pandas as pd
import requests
from datetime import date, timedelta

df = pd.DataFrame()
yesterday = (date.today() - timedelta(days=1)).strftime("%B %d, %Y") #Example: January 20, 2020
link = "https://idir.uta.edu/factchecker/score_text/{" #Starting point of the request API link

title = yesterday + "-SENATE" + ".txt" #Name of the file will be in the format January XX, 2020.txt
claims = [] #Creating arrays to be used later
scores = []

f = open(title, "r") #Opens file

for x in f:
    x = x.rstrip() #Gets rid of \n
    claims.append(x) #Adds to claims list
    claimScore = link + x + "}" #Finishes the link
    response = requests.get(claimScore) #Sends the request to API

    if response.status_code == 200:
        obj = response.json()
        final = obj['results'][0]['score']  # Retrieves the score
        scores.append(final)  # Adds to score array
    else:
        scores.append('N/A')

df['Claims'] = claims #Sets in dataframe
df['Scores'] = scores

gc = pygsheets.authorize(service_file='/Users/andre/PycharmProjects/SpacyTest/ClaimSpotting-76d810d48572.json') #Authorizes the use of Sheets API

api_key='AIzaSyDFYwDLiwJklXOf-w2hTLtNFwZufKWCrhk'

headers = {'Authorization': 'Bearer %s' % api_key}

sh = gc.open('Claim') #Opens the sheet we are using, called 'Claim'
current = sh.add_worksheet(title=yesterday) #Adds a new worksheet for that day
current.set_dataframe(df, (1, 1)) #Adds dataframe info
