from src.config import * # read config.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def getSalaryChange(file_path=DATA_COMBINED, chart_type='line'):
    ''' get salary change from 2022 to 2025 by city.

    Param:
    - ` file_path`: the path of the combined data file.
    - `chart_type`: the type of the chart, 'bar' or 'line'.

    Returns None. Plot the chart directly to compare.
    '''   
    try:
        df = pd.read_csv(file_path)
        required_cols = ['city', 'median', 'min', 'max', 'salary']
        df['change_pct'] = ((df['median'] - df['salary']) / df['salary'] * 100).round(1)
        
        colors_2022 = '#8c564b' 
        colors_2025 = ['#1f77b4', '#ff7f0e', '#2ca02c'] 
        
        plt.figure(figsize=(12, 6))
        x = np.arange(len(df['city']))
        
        if chart_type == 'bar':
            width = 0.2
            
            bars_2022 = plt.bar(x - width, df['salary'], width, 
                            label='2022 Avg Salary', color=colors_2022, alpha=0.8)
            bars_median = plt.bar(x, df['median'], width, 
                                label='2025 Median', color=colors_2025[0])
            bars_min = plt.bar(x + width, df['min'], width, 
                            label='2025 Low Avg', color=colors_2025[1], alpha=0.7)
            bars_max = plt.bar(x + 2*width, df['max'], width, 
                            label='2025 High Avg', color=colors_2025[2], alpha=0.7)
            

            for i, (city, pct) in enumerate(zip(df['city'], df['change_pct'])):
                plt.text(i, max(df.loc[i, ['salary', 'median', 'min', 'max']]) + 5000, 
                        f'+{pct}%', ha='center', fontsize=9)
            
            plt.title('Salary Change from 2022 to 2025 by City (Bar Chart)')
            
        elif chart_type == 'line':
            plt.plot(x, df['salary'], 'o--', label='2022 Avg', color=colors_2022, markersize=8)
            plt.plot(x, df['median'], 'o-', label='2025 Median', color=colors_2025[0], markersize=8)
            
            plt.errorbar(x, df['median'], 
                        yerr=[df['median'] - df['min'], df['max'] - df['median']],
                        fmt='none', ecolor='red', capsize=5, alpha=0.5, label='2025 Range')
            
            for i, (city, pct) in enumerate(zip(df['city'], df['change_pct'])):
                plt.annotate(f'+{pct}%', (x[i], df['median'][i]), 
                            textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
            
            plt.title('Salary Trend with Range (2022 vs 2025)')
        
        plt.xlabel('City')
        plt.ylabel('Salary ($)')
        plt.xticks(x, df['city'], rotation=45)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f'Error in getSalaryChange: {e}')

def completeYearWithLinearFit(df, target_year=2025):
    ''' Use linear regression to complete the missing data for the target year.
    
    Param:
    - `df`: the DataFrame containing the data.
    - `target_year`: the year to complete, default is 2025.

    Returns: the DataFrame with the completed data. 
    ''' 
    df_completed = df.copy()
    
    numeric_cols = df.select_dtypes(include=['number']).columns.drop('Year')
    
    predictions = {}
    for col in numeric_cols:
        valid_data = df[['Year', col]].dropna()
        if len(valid_data) < 2:
            predictions[col] = None
            continue
        
        slope, intercept, _, _, _ = linregress(valid_data['Year'], valid_data[col])
        
        predictions[col] = slope * target_year + intercept
    
    new_row = {'Year': target_year}
    new_row.update(predictions)
    
    df_completed = pd.concat([df_completed, pd.DataFrame([new_row])], ignore_index=True)
    
    return df_completed

def getEnhancedAnnualLineCharts(original_src=DATA_ANNUAL_WAGE_STATISTICS, new_data_path=DATA_COMBINED):
    ''' 
    Enhanced version that plots the original annual wage statistics plus additional data points.
    
    Params:
    - `original_src`: the source file path of the original annual wage dataset.
    - `new_data_path`: the file path containing additional city data for 2025 (mean, min, max) and 2022 average salary.
    
    Returns None. Plots the enhanced line charts with additional data points.
    '''
    try:
        df = pd.read_csv(original_src)
        df = completeYearWithLinearFit(df)
    
        plt.figure(figsize=(12, 6))
        
        df2 = df.set_index('Year')
        cols = df2.columns
        for col in cols:
            plt.plot(df2.index, df2[col], marker='o', label=col)
        
        if new_data_path:
            try:
                new_data = pd.read_csv(new_data_path)
                
                year_2025 = 2025
                plt.scatter([year_2025]*len(new_data), new_data['median'], color='red', marker='s', label='2025 City Median', zorder=5)
                # plt.scatter([year_2025]*len(new_data), new_data['min'], color='blue', marker='_', s=100, label='2025 City Min', zorder=5)
                # plt.scatter([year_2025]*len(new_data), new_data['max'], color='green', marker='_', s=100, label='2025 City Max', zorder=5)
                
                year_2022 = 2022
                plt.scatter([year_2022]*len(new_data), new_data['salary'], 
                           color='purple', marker='x', s=100, label='2022 City Avg Salary', zorder=5)
                
                for i, row in new_data.iterrows():
                    plt.text(year_2025, row['median'], row['city'], 
                            fontsize=8, ha='left', va='bottom')
                    
            except Exception as e:
                print(f'Error processing additional data: {e}')
        
        plt.title('Enhanced Annual Wage Statistics with City Data')
        plt.xlabel('Year')
        plt.ylabel('Wage')
        
        # Combine legends and adjust layout
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles, labels, bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()
        
    except Exception as e:
        print(f'Error in plotting enhanced annual wage statistics: {e}')

if __name__ == '__main__':
    getSalaryChange()
    getEnhancedAnnualLineCharts()