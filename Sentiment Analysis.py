#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentiment Analysis (Demo)
Author: Kimberley Ojeda Rojas

"""
from Final_Project import search_news
from Sentiment_Scores import sentiment_analysis

##Demo
#search_news("Dina Boluarte",20)

topics = ["Dina Boluarte","Seleccion Peruana","Shakira","Estados Unidos"]

per_topic, aggregate = sentiment_analysis(topics)

