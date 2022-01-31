import re
import pandas as pd

def extract_fund(name):
    first_word = name.split()[0]
    first_word = re.findall('\w+',first_word)[0]
    return first_word
    
def selection_process(df): 
    #Filtering by Morningstar Sustainability Rating of 5
    df_sel = df[df['Morningstar Sustainability Rating']==5]
    
    #Filtering by claim as Sustainable Investment - ESG Fund
    df_sel = df_sel[df_sel['Sustainable Investment - ESG Fund']=="Yes"]
    
    #Filtering by Average Credit Quality of A, AA or AAA
    df_sel = df_sel[df_sel['Average Credit Quality'].isin(['A','AA','AAA'])]
    
    #Filtering by no animal testing
    df_sel = df_sel[df_sel['Animal Testing']==0]
    
    #Filtering by highest returning Equity StyleBox funds
    df_sel = df_sel[df_sel['Equity StyleBox'].isin(['Large Core','Large Value','Mid Core'])]
    
    #Filtering by highest returning Morningstar Catergories
    df_sel = df_sel[~df_sel['Morningstar Category'].isin(['Cautious Allocation','Global Emerging Markets Equity','Moderate Allocation'])]

    return df_sel