#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentiment Analysis (Demo)
Author: Kimberley Ojeda Rojas

"""
from Web_Scrapping import search_news
from Sentiment_Scores import sentiment_analysis

# Demo using web scrapping to obtain dataframes of selected topics:
#search_news("Dina Boluarte",20)

# Demo using a list to apply sentiment analysis of selected topics:
topics = ["Dina Boluarte","Seleccion Peruana","Shakira", "Estados Unidos"] # Each dataframe (pickle files) is already generated for demo purposes
dataset, mean = sentiment_analysis(topics) # Aggregated dataset for selected topics.
