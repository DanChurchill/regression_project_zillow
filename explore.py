import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def corr_plot(df):
    #explore.plot_variable_pairs(train)
    cols = ['bedroomcnt', 'bathroomcnt',  'yearbuilt', 'fireplacecnt', 'hashottuborspa',
            'sqft', 'lotsizesquarefeet', 'tax_value']
    
    
    # make correlation plot
    df_corr = df[cols].corr()
    plt.figure(figsize=(12,8))
    sns.heatmap(df_corr, cmap='Blues', annot = True, mask= np.triu(df_corr), linewidth=.5)
    plt.show()


def target_dist(df):
    # Plot Distribution of target variable
    plt.figure(figsize=(12,8))
    plt.title('Distribution of Tax Values')
    sns.histplot(data=df, x='tax_value', hue='county', palette=["C1", "blue", "green"])
    plt.axvline(df.tax_value.mean(), color='k', linestyle='dashed', linewidth=1)
    min_ylim, max_ylim = plt.ylim()
    plt.text(df.tax_value.mean()*1.1, max_ylim*0.9, 'Mean: ${:,.2f}'.format(df.tax_value.mean()))
    plt.show()