#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:26:08 2024

@author: Kimberley Ojeda Rojas
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Define function for web scrapping in news website of Peru:
def web_scrapping(name,num_pages):
    # Create empty lists to save data
    headlines = []  
    descriptions = []  
    dates = []  
    links = []  

    # Define URL of website
    topic = name.lower().replace(" ","+")
    for i in range(1,num_pages+1):
        url = f'https://elcomercio.pe/buscar/{topic}/todas/descendiente/{i}/'
        page = requests.get(url)

    # Obtain the HTML code from website & 
    # Use BeautifulSoup library function to obtain data of news:
        data = BeautifulSoup(page.text,'html.parser')
        news = data.find_all('div',class_='story-item__information-box w-full')
        dates_html = data.find_all('p',class_='story-item__date')
    
    # Separate the news into headlines, description & link:
        for headline in news:  
            headlines.append(headline.h2.a.text)
        
        for description in news:  
            descriptions.append(description.p.text)
        
        for date in dates_html:  
            dates.append(date.get_text())
        
        for link in news:  
            links.append('https://elcomercio.pe'+link.h2.a["href"])
            
        # Obtain number of pages
        if i==1:
            pagesnum = data.find_all('a',class_='pagination__page capitalize secondary-font h-full text-md text-gray-300')
            lastpage=pagesnum[-1].text
        
    return headlines, descriptions, dates, links, lastpage

# Define function for translate spanish text to English:
def news_translate(headlines,descriptions):
    
    # Create empty lists to save translations
    headline_en = []
    description_en = []

    # Translate Spanish text into English    
    for i in range(len(headlines)):
        translations = GoogleTranslator(source='es',target='en').translate(headlines[i])
        headline_en.append(translations)
            
    for i in range(len(descriptions)):
        try:
            translations = GoogleTranslator(source='es',target='en').translate(descriptions[i])
            description_en.append(translations)
        except:      #Added because some descriptions are empty.
            description_en.append("")

    return headline_en, description_en

# Define function to add every list into a dataframe
def database(headline_en,description_en,dates, links):
    news_db = pd.DataFrame(
        {'Headline':headline_en,
         'Description':description_en,
         'Date':dates,
        'Link':links})
    
    # Convert date columnn to date type variable
    news_db.Date = pd.to_datetime(news_db['Date'].str[:11], dayfirst=True)

    return news_db

# Define function to create a wordcloud from news
def cloud(data,name):
    tokens = word_tokenize(' '.join(data["Headline"]))
    avoid_name = name.split()
    avoid_words = ["will","S","s","``","'s","``","$",",","%","''",".","(",")","...","year","Peru"] + avoid_name #Added for custom words we want to filter out
    tokens = [x for x in tokens if x not in avoid_words] 
    tagged_words = pos_tag(tokens)
    filtered_words = [word for word, tag in tagged_words if tag not in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']]
    text = ' '.join(filtered_words)
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f"Wordcloud_{name}.png")
    
# Define functions to combine all previous funcions
def search_news(name, num_pages=2):
    data= web_scrapping(name, num_pages)
    translation = news_translate(data[0], data[1])
    dataset = pd.DataFrame(database(translation[0],translation[1],data[2],data[3]))
    dataset.to_pickle(f"{name}.pkl")
    cloud(dataset,name)

    print("You're looking for news of:",name)
    print("There are",data[-1],"pages of news for this topic on the website")
    
    return dataset
    
    
