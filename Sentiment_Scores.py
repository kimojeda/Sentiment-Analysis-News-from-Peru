#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentiment Analysis (Function)
Author: Kimberley Ojeda Rojas

"""
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def dict_list(lst):
    if len(lst) == 0:
        raise ValueError("List is empty: You must choose a topic")
    
    else:
        files_dict = {}
        dfnames_dict = {}

        for item in lst:
            key = item
            value1 = item + '.pkl'
            files_dict[key] = value1
            value2 = item.lower().replace(' ', '_')
            dfnames_dict[key] = value2
            
        return files_dict, dfnames_dict

def sentiment_analysis(lst):
    dict = dict_list(lst)
    datasets = []
    mean_scores=[]
    for item in lst:
        dict[1][item] = pd.read_pickle(dict[0][item])
        
        vader = SentimentIntensityAnalyzer()
        new_words={"corruption":-1,"Rolex":-1,"investigation":-1,"watches":-1}
        vader.lexicon.update(new_words)
        
        scores = [vader.polarity_scores(head) for head in dict[1][item].Headline]
        
        dict[1][item] = dict[1][item].sort_values(by='Date')
        dict[1][item]= (dict[1][item].join(pd.DataFrame(scores))).reset_index()
        dict[1][item]= dict[1][item].drop(columns='index')
        
       # Plot for single topic
        fig,ax = plt.subplots()
        colors = ['lightcoral' if value < 0 else 'lightseagreen' for value in (dict[1][item])["compound"]]
        dict[1][item].plot.bar(y='compound', figsize = (10, 5),ax=ax,legend=False, color=colors)
        plt.style.use("fivethirtyeight")
        ax.set_xlabel(f'Number of news: {len(dict[1][item].index)}')
        ax.set_ylim(-1, 1)
        plt.suptitle(f"Evolution of Sentiment Scores from News of {item}")
        ax.set_xticks([0, len(dict[1][item].index) - 1])
        last_day = dict[1][item]["Date"].iloc[-1].strftime('%m/%d/%Y') + "\n(Latest)"
        ax.set_xticklabels([dict[1][item]["Date"].iloc[0].strftime('%m/%d/%Y'), last_day],rotation=0, fontsize = 9)      
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, labeltop=False, pad=20)
        ax.tick_params(axis='y', labelsize=9)
        datasets.append(dict[1][item])
        mean_scores.append([item,round((dict[1][item])["compound"].mean(),2)])
        
    # Plot to compare mean scores
    mean_scores = pd.DataFrame(mean_scores, columns=['Topic', 'Mean Score'])
    fig,ax = plt.subplots()
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

    return datasets, mean_scores