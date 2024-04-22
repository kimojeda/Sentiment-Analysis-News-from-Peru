#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to obtain datasets of news from Peru, using 'El Comercio' website.

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
def web_scrapping(name,num_pages): # Function that allows to choose any topic (Name) and the number of news pages that the script should collect.
    # Create empty lists to save data from loops
    headlines = []  
    descriptions = []  
    dates = []  
    links = []  

    # Define topic and URL of El Comercio website (digital version of newspaper from Peru)
    topic = name.lower().replace(" ","+")
    for i in range(1,num_pages+1):
        url = f'https://elcomercio.pe/buscar/{topic}/todas/descendiente/{i}/'
        page = requests.get(url)

    # Obtain the HTML code from website & 
    # Use BeautifulSoup library function to obtain data of news:
        data = BeautifulSoup(page.text,'html.parser')
        news = data.find_all('div',class_='story-item__information-box w-full')
        dates_html = data.find_all('p',class_='story-item__date')
    
    # Separate the news into headlines, description, dates & links:
        for headline in news:  
            headlines.append(headline.h2.a.text)
        
        for description in news:  
            descriptions.append(description.p.text)
        
        for date in dates_html:  
            dates.append(date.get_text())
        
        for link in news:  
            links.append('https://elcomercio.pe'+link.h2.a["href"])
            
        # Obtain number of news pages for selected topic
        if i==1:
            pagesnum = data.find_all('a',class_='pagination__page capitalize secondary-font h-full text-md text-gray-300')
            lastpage=pagesnum[-1].text
        
    return headlines, descriptions, dates, links, lastpage

# Define function to translate Spanish text to English:
def news_translate(headlines,descriptions):
    
    # Create empty lists to save translations
    headline_en = []
    description_en = []

    # Translate Spanish text from news headlines to English:    
    for i in range(len(headlines)):
        translations = GoogleTranslator(source='es',target='en').translate(headlines[i]) # Spanish (es) to English (en)
        headline_en.append(translations)
    
    # Translate Spanish text from news descriptions to English:          
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

# Define function to create a wordcloud from news' headlines
def cloud(data,name):
    tokens = word_tokenize(' '.join(data["Headline"]))
    avoid_name = name.split()
    avoid_words = ["will","S","s","``","'s","``","$",",","%","''",".","(",")","...","year","Peru"] + avoid_name #Added for custom words we want to filter out
    tokens = [x for x in tokens if x not in avoid_words] 
    tagged_words = pos_tag(tokens)
    # Filter out words some words such as: Prepositions, Conjunctions, Verb Conjugation & Punctuation Marks:
    filtered_words = [word for word, tag in tagged_words if tag not in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']]
    text = ' '.join(filtered_words)
    
    # Generate word cloud from headlines:
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f"Wordcloud_{name}.png") #Save word cloud for each topic
    
# Define functions to combine all previous functions
def search_news(name, num_pages=2):
    data= web_scrapping(name, num_pages)
    translation = news_translate(data[0], data[1])
    dataset = pd.DataFrame(database(translation[0],translation[1],data[2],data[3]))
    dataset.to_pickle(f"{name}.pkl") # Save dataset of news for each topic into pickle file
    cloud(dataset,name) 

    print("You're looking for news of:",name) # Print name of selected topic
    print("There are",data[-1],"pages of news for this topic on the website") # Print number of news pages that are available for the selected topic
    
    return dataset #This function will return a Pandas DataFrame for each selected topic.
    
    
