import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('cardio_train.csv', sep=';')

#calculate BMI
df['overweight'] = (df['weight'] / ((df['height']/100)**2) > 25) * 1

#Normalize cholesterol and gluc
df['cholesterol'] = np.where(df['cholesterol'] > 1, 1, 0)
df['gluc'] = np.where(df['gluc'] > 1, 1, 0)

def draw_cat_plot():
    df_cat = pd.melt(df,
                     id_vars=['cardio'],
                     value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
                     )

    df_cat = df_cat.groupby(['cardio', 'variable', 'value'],as_index=False).size()
    df_cat = df_cat.rename(columns={'size':'total'})
    fig = sns.catplot(data=df_cat,x='variable',y='total',hue='value',col='cardio',kind='bar',height=5,aspect=1.2)
    
    fig.set_axis_labels("variable", "total")

    fig.savefig('catplot.png')

    

    return fig


def draw_heat_map():
    df = pd.read_csv('cardio_train.csv', sep=';')
    #calculate overweight
    df['overweight'] = (df['weight'] / ((df['height']/100)**2) > 25).astype(int)
    # Normalize cholesterol and gluc
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &  # diastolic <= systolic
        (df['height'] >= df['height'].quantile(0.025)) &  # height >= 2.5th percentile
        (df['height'] <= df['height'].quantile(0.975)) &  # height <= 97.5th percentile
        (df['weight'] >= df['weight'].quantile(0.025)) &  # weight >= 2.5th percentile
        (df['weight'] <= df['weight'].quantile(0.975))    # weight <= 97.5th percentile
    ]
        

    # Calculate correlation matrix
    corr = df_heat.corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # Draw the heatmap
    sns.heatmap(corr,
                mask=mask,          # hide upper triangle
                annot=True,          # show correlation values
                fmt='.1f',           # format to 1 decimal place
                center=0,            # center colormap at 0
                square=True,         # make cells square
                linewidths=0.5,      # add gridlines
                cbar_kws={'shrink': 0.5},  # shrink colorbar
                ax=ax)
    
    # Return the figure
    return fig





print(draw_heat_map())
plt.show()
