import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True)

df = df.set_index('date')

lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)

df = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df.index = pd.to_datetime(df.index)
    # Add year and month columns
    df['year'] = df.index.year
    df['month'] = df.index.month
    
    # Group by year and month
    df_bar = df.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Create bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar.plot(kind='bar', ax=ax)
    
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily Page Views by Month')
    
    # Add month labels to legend
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    ax.legend(labels=months, title='Months')
    
    plt.tight_layout()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')  # Short month names (Jan, Feb, etc.)
    
    # Create month number for proper ordering
    df_box['month_num'] = df_box['date'].dt.month
    
    # Sort by month number to ensure Jan-Dec order
    df_box = df_box.sort_values('month_num')
    
    # Create figure with 2 subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    
    # ===== FIRST BOX PLOT: Year-wise (Trend) =====
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    
    # ===== SECOND BOX PLOT: Month-wise (Seasonality) =====
    # Define month order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, order=month_order)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    
    plt.tight_layout()
    fig.savefig('box_plot.png')
    return fig

draw_line_plot()
draw_bar_plot()
draw_box_plot()
plt.show()
