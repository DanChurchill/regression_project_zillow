import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# def plot_variable_pairs(df):
#     cols = ['bedroomcnt', 'bathroomcnt',  'yearbuilt',  'county', 'fireplacecnt', 'hashottuborspa',
#             'sqft', 'lotsizesquarefeet', 'tax_value']
    
    
#     # make correlation plot
#     df_corr = df[cols].corr()
#     plt.figure(figsize=(12,8))
#     sns.heatmap(df_corr, cmap='Blues', annot = True, mask= np.triu(df_corr), linewidth=.5)
#     plt.show()

#     # make pairplot
#     sns.pairplot(df[cols], corner=True, kind='reg',plot_kws={'line_kws':{'color':'red'}})
#     plt.show()

# def initial_charts(df):
#     cat_vars = ['bathroomcnt', 'bedroomcnt', 'county', 'fireplacecnt', 'garagecarcnt', 'poolcnt', 'yearbuilt']
#     num_vars = ['sqft', 'lotsizesquarefeet']

   

#     # make box plots
#     for cat in cat_vars:
#         plt.figure(figsize=(12,8))
#         plt.title(f'Tax value and {cat}')
#         sns.boxplot(data=df, y='tax_value', x=cat)
#         plt.show()
        
#     for num in num_vars:
#         sns.lmplot(data=df, y='tax_value', x=num, height=8, aspect=12/8, row='poolcnt', col='bedroomcnt', hue='county')
#         plt.show()