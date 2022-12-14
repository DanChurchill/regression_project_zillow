import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats


def bath_plot(train):
    ''' 
    Creates a Boxplot for the number of bathrooms and tax value
    Accepts a dataframe and creates/displays a plot
    '''
    plt.figure(figsize=(24,12))
    plt.title('Tax value and Number of Bathrooms')
    plt.grid(False)
    s = sns.boxplot(data=train, x='bathrooms', y='tax_value', palette="Blues", showfliers=False)
    s.set_xlabel("Number of Bathrooms")
    s.set_ylabel("Tax Value")
    plt.yticks([200000,400000,600000,800000,1_000_000],['$200k', '$400k', '$600k', '$800k', '$1M'])
    plt.axvline(5.5, color='red', linestyle='dashed', linewidth=1)
    plt.show()


def corr_plot(df):
    '''
    Creates a correlation plot for home features
    Accepts a dataframe and creates/displays a plot
    
    '''
    #explore.plot_variable_pairs(train)
    cols = ['bedrooms', 'bathrooms',  'age', 'fireplacecnt', 
            'sqft', 'lotsize', 'tax_value', 'poolcnt']
    
    # make correlation plot
    df_corr = df[cols].corr()
    plt.figure(figsize=(12,8))
    sns.heatmap(df_corr, cmap='Blues', annot = True, mask= np.triu(df_corr), linewidth=.5)
    plt.show()


def target_dist(df):
    '''
    Creates a hist plot to show the distribution of tax_value for properties by county
    Accepts a dataframe and creates/displays a plot
    '''
    # Plot Distribution of target variable
    plt.figure(figsize=(24,12))
    sns.set(font_scale=2)
    plt.title('Distribution of Tax Values')
    sns.histplot(data=df, x='tax_value', hue='county', bins= 75)
    #plt.legend(labels=["Los Angeles","Orange","Ventura"])

    plt.grid(False)
    plt.axvline(df.tax_value.mean(), color='k', linestyle='dashed', linewidth=3)
    min_ylim, max_ylim = plt.ylim()
    plt.text(df.tax_value.mean()*1.1, max_ylim*0.9, 'Mean: ${:,.2f}'.format(df.tax_value.mean()))
    plt.show()

def county_plot(df):
    '''
    Function to display a factor plot with the average property value of properties in each county
    Accpets a dataframe, creates a plot, and prints mean values by county
    '''
    # create subsets of df for each county
    orange = df[df.county == 'Orange']
    ventura = df[df.county == 'Ventura']
    la = df[df.county == 'Los Angeles']

    # get baseline churn rate for the horizontal line
    baseline = df.tax_value.mean()

    # display factorplot
    p = sns.factorplot( x="county", y="tax_value",  data=df, size=5, 
                   aspect=2, kind="bar", palette="muted", ci=None,
                   edgecolor=".2")
    plt.grid(False)
    plt.axhline(baseline, label = 'overall average property value', ls='--')
    p.set_ylabels("Property Value")
    p.set_xlabels("County")
    plt.title('Does County affect property value?')
    plt.show()
    # output values in each county
    print('Average property value of those in Los Angeles County is ', "${:,}".format(int(la.tax_value.mean())))
    print('Average property value of those in Ventura County is', "${:,}".format(int(ventura.tax_value.mean())))
    print('Average property value of those in Orange County is', "${:,}".format(int(orange.tax_value.mean())))
    print("")
    print("")

def county_ANOVA(df):
    '''
    Performs Analysis of Variance test for mean property values in 3 counties
    Accepts a dataframe and prints whether the null hypothesis can be rejected or confirmed
    
    '''
    orange = df[df.county == 'Orange']
    ventura = df[df.county == 'Ventura']
    la = df[df.county == 'Los Angeles']


    alpha = .05
    f, p = stats.f_oneway(orange.tax_value, ventura.tax_value, la.tax_value) 
    if p < alpha:
        print("We reject the Null Hypothesis")
    else:
        print("We confirm the Null Hypothesis")

def manybath_plot(df):
    '''
    Function to display a factor plot with the values of properties with more or less than 
    3 bathrooms.
    Accepts a dataframe and displays a plot, along with mean property values
    '''
    # create subsets of df for those with/without 3 plus bathrooms
    yes = df[df['4plusBath'] == 1].tax_value.mean()
    no = df[df['4plusBath'] == 0].tax_value.mean()
    
    # get baseline property value for the horizontal line
    baseline = df.tax_value.mean()

    # display factorplot
    p = sns.factorplot( x="4plusBath", y="tax_value",  data=df, size=8, 
                   aspect=2, kind="bar", palette="muted", ci=None,
                   edgecolor=".2")


    plt.yticks([200000,400000,600000],['$200k', '$400k', '$600k'])
    plt.xticks([0,1],['No', 'Yes'])
    plt.axhline(baseline, label = 'overall average property value', ls='--')
    p.set_ylabels("Property Value")
    p.set_xlabels("Has more than Three Bathrooms")
    plt.title('Do Lots of Bathrooms affect Tax Value?')
    plt.show()
    # output values for each subset
    print('Average property value of properties with more than three bathrooms', "${:,}".format(round(yes)))
    print('Average property value of properties with less than three bathrooms', "${:,}".format(round(no)))
    print("")



 

# Perform Independent T-Test: 2 samples, normal distribution, test variance

def manybath_test(df):
    '''
    function to perform an indepentdent 2 sample T-test to determine the difference in value of properties
    having more or less than 3 bathrooms is statistically significant
    Accepts a dataframe, displays whether the null hypothesis can be rejected or confirme
    '''

    # create subsets
    yes = df[df['4plusBath'] == 1]
    no = df[df['4plusBath'] == 0]

    # test variance
    variance = yes.tax_value.var() == no.tax_value.var()
    ?? = .05

    # calculate t and p values and output results
    t, p = stats.ttest_ind(yes.tax_value, no.tax_value, equal_var=variance)
    if p < ??:
        print('We reject the null hypothesis.')
    else:
        print('The null hypothesis is confirmed')
