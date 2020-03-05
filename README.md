# Claimspotting
Knight Lab Studio Class Project Winter 2020: Claimspotting
Medill School of Journalism, Northwestern University 

## Built With
* [Claimbuster](https://idir.uta.edu/claimbuster/) - The automated claim scoring platform used
* [MJML](https://mjml.io/) - The email framework used
* [Amazon Mechanical Turk](https://www.mturk.com/) - The crowdsourcing tool used

## MTurk Test
This contains our HTML file that was uploaded to Amazon Mechanical Turk (MTurk) for crowdsourcing purposes. 

## QuickScripts
This folder contains quick scripts that we used for testing various components of the project along the way such as Spacy and Claimbuster. 

### Test1, Test2
These folders contain CSV files associated with our first and second uses of Amazon MTurk. They include the samples that we inputted (Samples.csv), results (Results.csv), analysis (Statistics.csv), and visualizations (Score vs Rating.png) 

### Database.py
This script uses the sqlite package to perform basic database functions on the data gained from Scraper.py. 

### Results.py
This script performs data analysis using the Pearson Coefficient and p-value provided by the results gained from Amazon MTurk and exports the results to a csv file. 

### Scraper.py
This script scrapes the Congressional Record for claims that will later be scored by Claimbuster and Amazon MTurk. Performs filtering on irrelevant statements, reading of bills, etc. Also gains the context around a sentence and scores the sentence using Claimbuster. Uploads the final results to a csv file.

### WriteHouse.py, WriteSenate.py
These are scripts that use the Claimbuster API to score claims scraped from the Congressional Record for the House of Representatives and the Senate, respectively. These claims are then sent to a Google Sheets database for storage. Modified version included in Scraper.py. 

### create_tasks.py 
This is a script that creates HITs on Amazon MTurk for crowdsourcing purposes. 

## Scripts
This folder contains the bulk of our scripts that control the data pipeline within our project. Includes data collection, cleaning, storage, analysis, and visualization. 

## Contributors 
* **Andrew Huh** - *Student, Northwestern University Class of 2022*
* **Xunchuan Liu** - *Student, Northwestern University Class of 2021*
* **Lauren Tran** - *Student, Northwestern University Class of 2021*
* **Nick Diakopoulos** - *Professor, Northwestern University* 

## Acknowledgements 
Thank you to Knight Lab faculty and staff for making this project possible!
