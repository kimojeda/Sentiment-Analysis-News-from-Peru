# Sentiment-Analysis-News-from-Peru
Using NLP for sentiment analysis of news obtained through web scraping technique.

This is a project that is composed in three main sections:

## I. Datasets
Using a web scraping technique, we obtain a Pandas DataFrame that contains information of news for a certain topic. The news will be obtained from the digital version of [El Comercio](https://elcomercio.pe/) (Peruvian Newspaper).

The details of the web scraping procedure are in the file "Web_Scraping.py", which contains a function that allows to select a topic to generate a Pandas DataFrame.

## II. Sentiment Analysis
We use the VADER Module to analyze each headline obtained during the previous section. 

The details of this procedure are in the file "Sentiment_Scores.py".

## III. Data Visualization
We generate graphs for each selected topic, including:
* Evolution of sentiment scores by topic.
* Comparison of mean sentiment scores for a list of topics.
* Comparison of the sentiment score distribution for a list of topics.

For demostration purposes, please refer to the demo files:
1. Python Script: "Sentiment Analysis_Demo.py"

2. Dataframes (Pickle Files) that contain news data of the following topics:
    * Dina Boluarte
    * United States
    * Peruvian National Soccer Team
    * Shakira
