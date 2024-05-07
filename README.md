# Sentiment-Analysis-News-from-Peru
Sentiment analysis is a part of the Natural Language Processing field that focuses on analyzing people’s opinions, sentiments, evaluations, appraisals, attitudes, or emotions derived from written text. The analysis of this project is based on headlines from digital news in Peru, where the main objective is finding out the polarity or emotion's stregth of any topic by using a web scraping technique and an open-source NLP module.

This is a project that is composed in three main sections:

## I. Datasets
Using a web scraping technique with the [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) library, we obtain a Pandas DataFrame that contains information of news for any topic. The news are obtained from the digital version of [El Comercio](https://elcomercio.pe/) (Peruvian Newspaper). 

The details of the web scraping procedure are in the file "Web_Scraping.py", which contains a function that allows to select any topic, in order to generate a Pandas DataFrame with information of headlines, short description, link, and dates. Then, each dataset is saved as a Pickle file, which will be used later to perform the a sentiment analysis.

For demo purposes, we chose the following topics to perform an example of this analysis: 
* Dina Boluarte
* United States
* Peruvian National Soccer Team
* Shakira

Each of these topics has a dataframe with their latest 600 news (As of April 14, 2024) obtained from El Comercio, saved into a pickle file.

## II. Sentiment Analysis
For this section, the objective is obtaining a metric score for the headlines' derived emotion: Positive, Negative, or Neutral.

To do so, we use the VADER Module to analyze each headline obtained during the previous section. After this, we obtain a continuous numeric metric for each headline, that ranges from -1 to 1.

If the mean score is close to -1, then the headline can be perceived as Negative; if the score is close to 1, the text can be perceived as Positive. Lastly, if the score is 0, then the emotion derived from the headline is Neutral.

The details of this procedure are in the file "Sentiment_Scores.py". For demo purposes, we used the dataframes from the previous section.

## III. Data Visualization
Using the results from the previous section, we generate graphs for each selected topic, including:
* Evolution of sentiment scores by topic.
* Comparison of mean sentiment scores for a list of topics.
* Comparison of the sentiment score distribution for a list of topics.

The code for building these charts are inside the function for sentiment analysis, in the file "Sentiment_Scores.py".

Moreover, the code to show the charts for the selected topics is in the file "Sentiment Analysis_Demo.py".

From the demo files, we conclude that:

* Focusing only in the average mean score could lead to a biased conclusion on a topic's perception. In the case of "Dina Boluarte" and "United States", their mean scores are close to zero, but these results are not enough to conclude that the headlines perception is neutral, as they could also mean that the positive and negative scores are cancelling each other out.

* A more complete approach is taking into acount the distribution of scores across our analysis. For the example of "Dina Boluarte" and "United States", we can conclude that the headlines perception is more polarized, given that their headlines have both positive and negative perceptions.

* The results of the sentiment analysis can change over time, as this analysis is based on a dataset of news that will be updated by the newspaper.