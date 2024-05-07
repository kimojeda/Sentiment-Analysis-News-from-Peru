#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to obtain Sentiment Analysis Scores from news headlines, using SentimentIntensityAnalyzer (VADER Module)
Author: Kimberley Ojeda Rojas

"""
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer #Module for Sentiment Analysis (https://www.nltk.org/api/nltk.sentiment.vader.html)
import seaborn as sns

# Parameter for all graphs:
plt.rcParams['figure.dpi'] = 300

# Function to convert names from list of topics to dataframe file names:
def dict_list(lst):
    if len(lst) == 0:
        raise ValueError("List is empty: You must choose a topic")
    
    else:
        files_dict = {}
        dfnames_dict = {}

        for item in lst:
            key = item
            value1 = item + '.pkl' # Format of the pickle file name for each dataframe
            files_dict[key] = value1
            value2 = item.lower().replace(' ', '_')
            dfnames_dict[key] = value2
            
        return files_dict, dfnames_dict

# Function for sentiment analysis using a list of topics as input:
def sentiment_analysis(lst):
    dict = dict_list(lst)
    dataset_topics = pd.DataFrame()
    mean_scores=[]
    
    for item in lst:
        dict[1][item] = pd.read_pickle(dict[0][item]) 
        
        vader = SentimentIntensityAnalyzer() # Start sentiment analysis tool
        new_words={"corruption":-1,"Rolex":-1,"investigation":-1,"watches":-1} #Added words for context of news in Peru (Example: 'Rolex' is associated with a corruption case)
        vader.lexicon.update(new_words) # Update sentiment analysis tool with new words.
        
        scores = [vader.polarity_scores(head) for head in dict[1][item].Headline] # Calculate scores for each headline
        
        dict[1][item] = dict[1][item].sort_values(by='Date') # Sort dataframe by date
        dict[1][item]= (dict[1][item].join(pd.DataFrame(scores))).reset_index()
        dict[1][item]= dict[1][item].drop(columns='index')
        
       # Plot for single topic: Evolution of sentiment scores for each topic
        fig,ax = plt.subplots()
        colors = ['lightcoral' if value < 0 else 'lightseagreen' for value in (dict[1][item])["compound"]]
        dict[1][item].plot.bar(y='compound', figsize = (10, 5),ax=ax,legend=False, color=colors, width=1)
        plt.style.use("fivethirtyeight")
        ax.set_xlabel(f'Number of news: {len(dict[1][item].index)}')
        ax.set_ylim(-1, 1)
        plt.suptitle(f"Evolution of Sentiment Scores from News of {item}")
        ax.set_xticks([0, len(dict[1][item].index) - 1])
        last_day = dict[1][item]["Date"].iloc[-1].strftime('%m/%d/%Y') + "\n(Latest)" # Show the range of dates available for each topic
        ax.set_xticklabels([dict[1][item]["Date"].iloc[0].strftime('%m/%d/%Y'), last_day],rotation=0, fontsize = 9) # Update date format (Since in Peru they use DD/MM/YYYY) 
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, labeltop=False, pad=20)
        ax.tick_params(axis='y', labelsize=9)
        
        # Read each dataframe in list of topics & add "Topic" column
        topic = dict[1][item]
        topic["Topic"] = item
        dataset_topics = pd.concat([dataset_topics, topic], ignore_index=True)
        # Create a list for the mean sentiment scores for each topic
        mean_scores.append([item,round((dict[1][item])["compound"].mean(),2)])
        
    # Plot to compare mean scores for all topics within a list
    mean_scores = pd.DataFrame(mean_scores, columns=['Topic', 'Mean Score'])
    fig,ax = plt.subplots()
    colors = ['lightcoral' if value < 0 else 'lightseagreen' for value in mean_scores["Mean Score"]] # Change color depending on mean value
    mean_scores.plot(kind="bar",x="Topic",y='Mean Score',figsize = (10, 5),ax=ax,legend=False,color=colors)
    plt.suptitle("Sentiment Mean Score from News in Peru")
    ax.set_xlabel('')
    ax.axhline(y=0, color='black', linewidth=1.5)
    plt.xticks(rotation=0, ha="center")
    plt.gca().set_yticklabels([])
    plt.grid(False)
    
    for bar in ax.patches: # Show values of mean scores in the graph
        bar_height = bar.get_height()  
        ax.annotate(f'{bar_height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, bar_height/2-0.004),
                    ha='center')
        
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, labeltop=False, pad=10)
    
    # Plot to compare distribution of sentiment scores
    g = sns.FacetGrid(dataset_topics, row='Topic', hue='Topic', aspect=10, height=0.9,palette='Set1')
    g.map(sns.histplot, 'compound', clip_on=False, fill=True, alpha=1,kde = True, line_kws={'linewidth': 0.8, 'linestyle':'--','color': 'black'}) # Histograms
    g.map(plt.axvline, x=0, color='black', linestyle='--', lw=0.8) # Add a vertical line at x=0
    g.set(xlim=(-1, 1)) #Change range in X 
    
    # Add name of each item (Topic) on the list to the graph:
    for i, ax in enumerate(g.axes.flat):
        ax.text(-1.4, 0.5, lst[i],
                 fontsize=9)
        
    # Add a negative value for the space between plot to simulate a combined background (combined vertical axis lines)
    g.fig.subplots_adjust(hspace=0)

    # Remove axes titles & yticks, since we already added the names of the topic using a loop
    g.set_titles("")
    g.set(yticks=[])
    g.set_axis_labels("", "")
    
    # Customize x axis and add a title
    plt.setp(ax.get_xticklabels(), fontsize=9)
    plt.xlabel('Sentiment Score', fontsize=10)
    g.fig.suptitle('Comparison of sentiment scores distribution',
                   ha='center', 
                   fontsize=12,y=1.05);
    
    return dataset_topics, mean_scores # The funcion will return an aggregated dataframe for all topics inside list