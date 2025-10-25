import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np


def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')
    
    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], alpha=0.6, s=20)
    
    # Create first line of best fit using all data
    slope, intercept, r_value, p_value, std_err = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    
    # Generate x values from first year to 2050
    years_extended = np.arange(df['Year'].min(), 2051)
    sea_level_pred = slope * years_extended + intercept
    
    # Plot first line of best fit
    plt.plot(years_extended, sea_level_pred, 'r', label='Best fit line (1880-)')
    
    # Create second line of best fit using data from year 2000 onwards
    df_recent = df[df['Year'] >= 2000]
    slope_recent, intercept_recent, r_value_recent, p_value_recent, std_err_recent = linregress(
        df_recent['Year'], df_recent['CSIRO Adjusted Sea Level']
    )
    
    # Generate x values from 2000 to 2050
    years_recent = np.arange(2000, 2051)
    sea_level_pred_recent = slope_recent * years_recent + intercept_recent
    
    # Plot second line of best fit
    plt.plot(years_recent, sea_level_pred_recent, 'g', label='Best fit line (2000-)')
    
    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    plt.legend()
    
    # Save plot and return data for testing
    plt.savefig('sea_level_plot.png')
    return plt.gca()
