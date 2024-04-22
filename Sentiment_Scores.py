#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentiment Analysis (Function)
Author: Kimberley Ojeda Rojas

"""
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns

plt.rcParams['figure.dpi'] = 300

# Function to convert input from list of topics to dataframe file names:
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

# Function for sentiment analysis using a list of topics as input:
def sentiment_analysis(lst):
    dict = dict_list(lst)
    dataset_topics = pd.DataFrame()
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
        dict[1][item].plot.bar(y='compound', figsize = (10, 5),ax=ax,legend=False, color=colors, width=1)
        plt.style.use("fivethirtyeight")
        ax.set_xlabel(f'Number of news: {len(dict[1][item].index)}')
        ax.set_ylim(-1, 1)
        plt.suptitle(f"Evolution of Sentiment Scores from News of {item}")
        ax.set_xticks([0, len(dict[1][item].index) - 1])
        last_day = dict[1][item]["Date"].iloc[-1].strftime('%m/%d/%Y') + "\n(Latest)"
        ax.set_xticklabels([dict[1][item]["Date"].iloc[0].strftime('%m/%d/%Y'), last_day],rotation=0, fontsize = 9)      
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, labeltop=False, pad=20)
        ax.tick_params(axis='y', labelsize=9)
        
        # Read each dataframe in list of topics & add "Topic" column
        topic = dict[1][item]
        topic["Topic"] = item
        dataset_topics = pd.concat([dataset_topics, topic], ignore_index=True)
        # Create a list for the mean sentiment scores for each topic
        mean_scores.append([item,round((dict[1][item])["compound"].mean(),2)])
        
    # Plot to compare mean scores
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
    g = sns.FacetGrid(dataset_topics, row='Topic', hue='Topic', aspect=12, height=0.5,palette='Set1')
    g.map(sns.kdeplot, 'compound', bw_adjust=1, clip_on=False, fill=True, alpha=1) # Density plots
    g.map(plt.axvline, x=0, color='black', linestyle='--', lw=0.8) # Add a vertical line at x=0

    # Add name of each item (Topic) on the list to the graph:
    for i, ax in enumerate(g.axes.flat):
        ax.text(-1.6, 0.5, lst[i],
                 fontsize=9)
        
    # Add a negative value for the space between plot to simulate a combined background (combined vertical axis lines)
    g.fig.subplots_adjust(hspace=-0.03)

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
    
    return dataset_topics, mean_scores