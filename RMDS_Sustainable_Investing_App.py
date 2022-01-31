#!/usr/bin/env python
# coding: utf-8

# # 1. Import libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')
import dash
from dash import Dash, dcc, html, Input, Output  
import supporting_functions as sf


# # 2. Load dataset

# In[2]:

path = r"C:\Users\sdas\RDMS_Data_Challenge\competition_data\funds.csv"
df = pd.read_csv(path)


# In[3]:


df = df.rename(columns={"Portfolio Sustainability Score":"Portfolio Financial Score"})


# #  3. Fund selection process
# 
# Key factors and weights (1, 2, and 3): 
# - *Morningstar Sustainability Rating*: 3
# - *Environmental, Social and Governance Scores*
# -- **difficult to gauge what a good score cutoff should be**
# - *Claimed as 'Sustainable Investment'* (focusing on 'ESG Investment' criteria): 3
# - *Animal testing*: 2
# - *Alcohol, Thermal Coal, Fossil Fuels, Small Arms, Tobacco*
# -- **difficult to gauge what a good score cutoff should be**
# - *1-year return*: 2
# - *Average Credit Quality*: 2
# - *Return vs Equity StyleBox*: 2 
# -- **Large Core and Large Value appear to have the best 1-year returns**
# - *Return vs Morningstar Category*: 2

# # 4. Dashboard

df_pipeline = df.copy()

##########################################################################################################
############################################### Row 1 ####################################################
##########################################################################################################

fig1 = make_subplots(
    rows=1, cols=4,
    specs=[[{"type": "domain"},{"type": "domain"},{"type": "domain"},{"type": "domain"}]],
    subplot_titles=("Sustainability Rating - 5 selected",
                    "Sustainable ESG Fund - Yes selected", 
                    "Credit Quality - A/AA/AAA selected",  
                    "Animal Testing - 0 selected")
)

#Plotting Morningstar sustainability ratings
df_sus_ratings = df_pipeline['Morningstar Sustainability Rating'].value_counts()
df_sus_ratings = df_sus_ratings.sort_index()

fig1.add_trace(go.Pie(
                    labels=list(df_sus_ratings.index), 
                     values=list(df_sus_ratings.values), 
                     hole=.45,
                     pull=[0, 0, 0, 0, 0.2]
                     )
                     ,row=1,col=1)

fig1.update_traces(textinfo='value+percent+label')

#Filtering by Morningstar Sustainability Rating of 5
df_pipeline = df_pipeline[df_pipeline['Morningstar Sustainability Rating']==5]

#Plotting distribution of funds claimed as Sustainable Investment - ESG Fund 
df_sus_inv_dist = df_pipeline['Sustainable Investment - ESG Fund'].value_counts()
df_sus_inv_dist = df_sus_inv_dist.sort_index()

fig1.add_trace(go.Pie(
                    labels=list(df_sus_inv_dist.index), 
                     values=list(df_sus_inv_dist.values), 
                     hole=.45,
                     #pull=[0.2, 0]
                     )
                     ,row=1,col=2)

fig1.update_traces(textinfo='percent+label')

#Filtering by Sustainable Investment - ESG Fund claims
df_pipeline = df_pipeline[df_pipeline['Sustainable Investment - ESG Fund']=="Yes"]

#Plotting distribution of funds claimed as Sustainable Investment - ESG Fund 
df_cred_rating = df_pipeline['Average Credit Quality'].value_counts()
df_cred_rating = df_cred_rating.sort_index()

fig1.add_trace(go.Pie(
                    labels=list(df_cred_rating.index), 
                     values=list(df_cred_rating.values), 
                     hole=.45,
                     #pull=[0.2,0.2,0.2,0,0,0]
                     )
                     ,row=1,col=3)

fig1.update_traces(textinfo='percent+label')

#Filtering by Average Credit Quality of A, AA or AAA
df_pipeline = df_pipeline[df_pipeline['Average Credit Quality'].isin(['A','AA','AAA'])]

#Plotting distribution of funds claimed as Sustainable Investment - ESG Fund 
df_animal_testing = df_pipeline['Animal Testing'].value_counts()
df_animal_testing = df_animal_testing.sort_index()

fig1.add_trace(go.Pie(
                    labels=list(df_animal_testing.index), 
                     values=list(df_animal_testing.values), 
                     hole=.45,
                     )
                     ,row=1,col=4)

fig1.update_traces(textinfo='percent+label')

#Filtering by no animal testing
df_pipeline = df_pipeline[df_pipeline['Animal Testing']==0]

fig1.update_layout(
    title="ESG Fund Selection Pipeline and Analysis",
    legend_title="",
    title_font_size=30
)

##########################################################################################################
############################################### Row 2 ####################################################
##########################################################################################################

fig2 = make_subplots(
    rows=1, cols=3,
    specs=[[{"type": "box"},{"type": "box"},{"type": "xy"}]],
    subplot_titles=("Equity 1-Year Return", 
                    "Morningstar Category 1-Year Return (excluding 'Large Growth')",
                    "Equity Metrics (excluding equities <30% return)")
)

#Plotting boxplots across Equity StyleBox
fig2.add_trace(go.Box(
    x=df_pipeline['Equity StyleBox'],
    y=df_pipeline['1 Year Annualized (%)'],
    #marker_color='coral',
    name = '1-Year Return',
    ),row=1,col=1)

#Filtering by highest returning Equity StyleBox funds
df_pipeline = df_pipeline[df_pipeline['Equity StyleBox'].isin(['Large Core','Large Value','Mid Core'])]

#Plotting boxplots across Morningstar Category
fig2.add_trace(go.Box(
    x=df_pipeline['Morningstar Category'],
    y=df_pipeline['1 Year Annualized (%)'],
    #marker_color='peachpuff',
    name = '1-Year Return',
    ),row=1,col=2)

#Filtering by highest returning Morningstar Categories
df_pipeline = df_pipeline[~df_pipeline['Morningstar Category'].isin(['Cautious Allocation','Global Emerging Markets Equity',
                                                      'Moderate Allocation'])]

fig2.update_layout(
    title="Filtering Funds Based On 1-Year Returns And Environmental Factors",
    title_font_size=30
)

#Plotting percentage of alchohol, fossil fuels, small arms, thermal coal and tobacco association across Equity StyleBox
avg_per_cat = df_pipeline[['Morningstar Category','% Alcohol','% Fossil Fuels','% Small Arms',
                '% Thermal Coal', '% Tobacco']].groupby('Morningstar Category').mean()

fig2.add_trace(go.Bar(
    x = avg_per_cat.index,
    y = avg_per_cat['% Alcohol'],
    name = '% Alcohol',
    marker_color = 'indianred',
),row=1,col=3)

fig2.add_trace(go.Bar(
    x = avg_per_cat.index,
    y = avg_per_cat['% Fossil Fuels'],
    name = '% Fossil Fuels',
    marker_color = 'lightsalmon',
),row=1,col=3)

fig2.add_trace(go.Bar(
    x = avg_per_cat.index,
    y = avg_per_cat['% Small Arms'],
    name = '% Small Arms',
    marker_color = 'darkkhaki',
),row=1,col=3)

fig2.add_trace(go.Bar(
    x = avg_per_cat.index,
    y = avg_per_cat['% Thermal Coal'],
    name = '% Thermal Coal',
    marker_color = 'olive',
),row=1,col=3)

fig2.add_trace(go.Bar(
    x = avg_per_cat.index,
    y = avg_per_cat['% Tobacco'],
    name = '% Tobacco',
    marker_color = 'mediumorchid',
),row=1,col=3)

'''
#Plotting average scores across *Equity StyleBox*

avg_scores = df[['Equity StyleBox','Portfolio Social Score','Portfolio Governance Score',
                'Portfolio Environmental Score']].groupby('Equity StyleBox').mean()

fig2.add_trace(go.Bar(
    x = avg_scores.index,
    y = avg_scores['Portfolio Social Score'],
    name = 'Portfolio Social Score',
    marker_color = 'lightsalmon',
),row=1,col=4)

fig2.add_trace(go.Bar(
    x = avg_scores.index,
    y = avg_scores['Portfolio Environmental Score'],
    name = 'Portfolio Environmental Score',
    marker_color = 'darkkhaki',
),row=1,col=4)

fig2.add_trace(go.Bar(
    x = avg_scores.index,
    y = avg_scores['Portfolio Governance Score'],
    name = 'Portfolio Governance Score',
    marker_color = 'olive',
),row=1,col=4)

'''
# Update xaxis properties
fig2.update_xaxes(title_text="Equity StyleBox", row=1, col=1)
fig2.update_xaxes(title_text="Morningstar Category", row=1, col=2)
fig2.update_xaxes(title_text="Morningstar Category", row=1, col=3)

# Update yaxis properties
fig2.update_yaxes(title_text="Return (%)", row=1, col=1)
fig2.update_yaxes(title_text="Return (%)", row=1, col=2)
fig2.update_yaxes(title_text="Avg Percent (%)", row=1, col=3)

##########################################################################################################
############################################### Row 3 ####################################################
##########################################################################################################

fig3 = make_subplots(
    rows=1, cols=4,
    specs=[[{"type": "xy"},{"type": "xy"},{"type": "box"},{"type": "box"}]],
    subplot_titles=("Distribution of Institutions from Selected Funds",
                    "Average ESG Score", 
                    "Avg ESG Score vs Sustainability Rating",
                    "Return Per Sustainability Rating")
)

#Plotting average ESG scores for all funds 
df_scores = df[['Portfolio Social Score','Portfolio Environmental Score','Portfolio Governance Score']].mean()

#Plotting average ESG scores for selected funds
df_pipeline = df_pipeline[df_pipeline['Morningstar Category']!='Target Date']
df_select_scores = df_pipeline[['Portfolio Social Score','Portfolio Environmental Score','Portfolio Governance Score']].mean()

'''
df_cat_freq = df_pipeline['Morningstar Category'].value_counts().sort_index()

fig3.add_trace(go.Bar(
    x=list(df_cat_freq.index),
    y=list(df_cat_freq.values),
    name = 'Fund Category Counts ',
    #marker_color = 'mediumorchid',
    ),row=1,col=1)
'''

sus_funds = df_pipeline['Name'].map(sf.extract_fund).value_counts().sort_index()

fig3.add_trace(go.Bar(
    x=list(sus_funds.index),
    y=list(sus_funds.values),
    name = 'Count of selected funds',
    #marker_color = 'mediumorchid',
    ),row=1,col=1)

fig3.add_trace(go.Bar(
    x=list(df_scores.index),
    y=list(df_scores.values),
    name = 'Avg ESG Scores - All Funds',
    #marker_color = 'mediumorchid',
    ),row=1,col=2)

fig3.add_trace(go.Bar(
    x=list(df_select_scores.index),
    y=list(df_select_scores.values),
    name = 'Avg ESG Scores - Selected Funds ',
    #marker_color = 'mediumorchid',
    ),row=1,col=2)

#Plotting 1, 3, and 5 year returns for all funds
fig3.add_trace(go.Box(
    x=df['Morningstar Sustainability Rating'],
    y=df['1 Year Annualized (%)'],
    name = '1-Year Return - All Funds',
    ),row=1,col=4)
'''
fig3.add_trace(go.Box(
    x=df['Morningstar Sustainability Rating'],
    y=df['3 Years Annualized (%)'],
    name = '3-Years Return',
    ),row=1,col=4)

fig3.add_trace(go.Box(
    x=df['Morningstar Sustainability Rating'],
    y=df['5 Years Annualized (%)'],
    name = '5-Years Return',
    ),row=1,col=4)
'''

#Plotting 1, 3, and 5 year returns for selected funds

fig3.add_trace(go.Box(
    x=df_pipeline['Morningstar Sustainability Rating'],
    y=df_pipeline['1 Year Annualized (%)'],
    name = '1-Year Return - Selected Funds',
    ),row=1,col=4)
'''
fig3.add_trace(go.Box(
    x=df_select['Morningstar Sustainability Rating'],
    y=df_select['3 Years Annualized (%)'],
    name = '3-Years Return - Selected Funds',
    ),row=1,col=4)

fig3.add_trace(go.Box(
    x=df_select['Morningstar Sustainability Rating'],
    y=df_select['5 Years Annualized (%)'],
    name = '5-Years Return - Selected Funds',
    ),row=1,col=4)
'''
fig3.add_trace(go.Box(
    x=df['Morningstar Sustainability Rating'],
    y=df['Portfolio Environmental Score'],
    name='Environmental Score'
    ),row=1,col=3)

fig3.add_trace(go.Box(
    x=df['Morningstar Sustainability Rating'],
    y=df['Portfolio Social Score'],
    name='Social Score'
    ),row=1,col=3)

fig3.add_trace(go.Box(
    x=df['Morningstar Sustainability Rating'],
    y=df['Portfolio Governance Score'],
    name='Governance Score'
    ),row=1,col=3)
        
fig3.update_layout(
    title="Analyzing ESG Metrics And Returns For Selected Funds",
    xaxis_title="ESG Metric",
    yaxis_title="Avg Score",
    title_font_size=30,
    boxmode='group' # group together boxes of the different traces for each value of x
)

# Update xaxis properties
fig3.update_xaxes(title_text="Institution", row=1, col=1)
fig3.update_xaxes(title_text="ESG Feature", row=1, col=2)
fig3.update_xaxes(title_text="Sustainability Rating", row=1, col=3)
fig3.update_xaxes(title_text="Sustainability Rating", row=1, col=4)

# Update yaxis properties
fig3.update_yaxes(title_text="Count", row=1, col=1)
fig3.update_yaxes(title_text="Avg Score", row=1, col=2)
fig3.update_yaxes(title_text="Avg Score", row=1, col=3)
fig3.update_yaxes(title_text="Return (%)", range=[-25,120], row=1, col=4)

##########################################################################################################
############################################## Output File ###############################################
##########################################################################################################

df_pipeline.to_csv('Sustainable_Funds.csv')

##########################################################################################################
############################################## Dash App ##################################################
##########################################################################################################
    
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3)
])

app.run_server(debug=True, use_reloader=False)


# In[ ]:




