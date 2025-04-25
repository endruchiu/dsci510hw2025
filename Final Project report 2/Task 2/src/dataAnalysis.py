import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import numpy as np
import seaborn as sns

DATA_ANNUAL_WAGE_STATISTICS = 'data/data_annual_wage_statistics.csv'
DATA_SOFTWARE_ENGINEER_SALARY = 'data/data_software_engineer_salary.csv'
DATA_US_SOFTWARE_DEVELOPER_SALARIES = 'data/data_US_software_developer_salaries.csv'

def getLineCharts(df, header, title, ylabel, cols=None):
    ''' Params:
    - `df`: the pandas Dataframe of dataset.
    - `cols`: the list of column's name of the Dataframe to plot line charts. If none, use all the columns
    - `header`: the name of the index column.
    - `title`: the title of the plot.
    - `ylabel`: the label of the y-axis.
    
    Returns None. Plots the columns in `cols` in the Dataframe `df`, with the X-axis as `header` column. '''
    try:
        df2 = df.set_index(header)
        if not cols:
            cols = df2.columns
        plt.figure(figsize=(10, 5))
        for col in cols:
            plt.plot(df2.index, df2[col], marker='o', label=col)
        
        plt.title(title)
        plt.xlabel(header)
        plt.ylabel(ylabel)
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f'Error in plotting {title} header={header} ylabel={ylabel}: {e}')

def getAnnualLineCharts(src = DATA_ANNUAL_WAGE_STATISTICS):
    ''' Params:
    - `src`: the source file path of the dataset.
    
    Returns None. Plots the line charts of the annual wage statistics.'''
    try:
        df = pd.read_csv(src)
        getLineCharts(df, 'Year', 'Annual Wage Statistics', 'Wage')
    except Exception as e:
        print(f'Error in plotting annual wage statistics: {e}')

def getLinearRegression(x, y, title, xlabel, ylabel):
    ''' Params:
    - `x`: the name of the column of the Dataframe to be the X-axis.
    - `y`: the name of the column of the Dataframe to be the Y-axis.
    - `title`: the title of the plot.
    - `xlabel`: the label of the x-axis.
    - `ylabel`: the label of the y-axis.

    Returns None. Prints and plots the linear regression of the columns `x` and `y` in the Dataframe `df`. '''
    try:
        x = x.values.reshape(-1, 1)
        y = y.values.reshape(-1, 1)
        model = LinearRegression()
        model.fit(x, y)
        slope = model.coef_[0][0]
        intercept = model.intercept_[0]
        print(f"Regression fuction: y = {slope:.4f}x + {intercept:.4f}")
        r_squared = model.score(x, y)
        print(f"R² score: {r_squared:.4f}")
        y_pred = model.predict(x)

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='blue', label='Raw data')
        plt.plot(x, y_pred, color='red', label='Regression Line') 
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        
        plt.grid(True)
        equation_text = f'y = {intercept+slope*x[0][0]:.2f} + {slope:.2f}(x-{x[0][0]:.0f}) '
        plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, 
            fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        plt.show()
    except Exception as e:
        print(f'Error in plotting {title} xlabel={xlabel} ylabel={ylabel}: {e}')

def getOLSRegression(x, y):
    ''' Params:
    - `x`: the name of the column of the Dataframe to be the X-axis.
    - `y`: the name of the column of the Dataframe to be the Y-axis.

    Returns None. Prints the analyse results the OLS regression of the columns `x` and `y` in the Dataframe `df`. '''
    try:
        # Z-scoring
        x = (x - x.mean()) / x.std()
        x = sm.add_constant(x)
        model = sm.OLS(y, x)
        results = model.fit()
        print(results.summary())
    except Exception as e:
        print(f'Error in OLS regression: {e}')

def getAnuualWageLinearRegression(src = DATA_ANNUAL_WAGE_STATISTICS):
    ''' Params:
    - `src`: the source file path of the dataset.

    Returns None. Prints and plots the linear regression of the annual wage statistics.'''
    try:
        df = pd.read_csv(src)
        getLinearRegression(df['Year'], df['A_MEAN'], 'Annual Mean Wage Statistics Linear Regression', 'Year', 'Wage')
        getOLSRegression(df['Year'], df['A_MEAN'])
    except Exception as e:
        print(f'Error in plotting annual wage statistics: {e}')

def getBarCharts(df, header, mainColumn, title, ylabel, colors=None):
    ''' Params:
    - `df`: the pandas Dataframe of dataset.
    - `mainColumn`: the name of the column of the Dataframe to be the main column. (sorted by mainColumn ascending)
    - `header`: the name of the index column.
    - `title`: the title of the plot.
    - `ylabel`: the label of the y-axis.
    - `colors`: optional list of colors for bars (defaults to a blue gradient)

    Returns None. Plots the columns in `cols` in the Dataframe `df`, with the X-axis as `header` column. '''
    try:
        df2 = df.set_index(header)
        df2 = df2.sort_values(by=mainColumn, ascending=True) # rows sort
        # columns sort
        col_means = df2.mean().sort_values(ascending=True)
        columns = col_means.index.tolist()
        
        plt.figure(figsize=(12, 8))
        width = 0.8 / len(columns)
        if colors is None:
            colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(columns)))
        for i, (col, color) in enumerate(zip(columns, colors)):
            offset = width * (i - (len(columns)-1)/2)  # Center bars around x-tick
            plt.bar([x + offset for x in range(len(df2))],
                df2[col], width, color=color, label=col)
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(header)
        plt.xticks(range(len(df2)), df2.index, rotation=45, ha='right')
        plt.legend()
        
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f'Error in plotting {title}: {e}')

def getCityBarCharts(src = DATA_SOFTWARE_ENGINEER_SALARY):
    ''' Params:
    - `src`: the source file path of the dataset.

    Returns None. Plots the bar charts of the software engineer salary statistics.'''
    try:
        df = pd.read_csv(src)
        getBarCharts(df, 'city', 'median', 'Software Engineer Mean Salary Statistics in North America', 'Salary')
    except Exception as e:
        print(f'Error in plotting software engineer salary statistics: {e}')

def getVariance2D(df, header, col1, col2, title):
    ''' Params:
    - `df`: the pandas Dataframe of dataset.
    - `header`: the name of the index column.
    - `col1`: the name of the column of the Dataframe to be the X-axis.
    - `col2`: the name of the column of the Dataframe to be the Y-axis.
    - `title`: the title of the plot.
    
    Returns None. Plots the 2D scatter plot of the columns `x` and `y` in the Dataframe `df`. '''
    try:
        print(f'Mean of {col1} : {df[col1].mean():.2f}, Std of {col1} : {df[col1].std():.2f}')
        print(f'Mean of {col2}: {df[col2].mean():.2f},  Std of {col2}: {df[col2].std():.2f}')
        def zscore(series):
            return (series - series.mean()) / series.std()
        df[f'{col1}_z'] = zscore(df[col1])
        df[f'{col2}_z'] = zscore(df[col2])

        x_max = df[f'{col1}_z'].abs().max()
        y_max = df[f'{col2}_z'].abs().max()
        axis_max = max(x_max, y_max) * 1.1
        
        plt.figure(figsize=(10, 8))
        plt.grid(True, linestyle='--', alpha=0.3)
        
        scatter = sns.scatterplot(
            data=df,
            x=f'{col1}_z',
            y=f'{col2}_z',
            hue=header,
            palette='tab20',
            s=150,
            alpha=0.8
        )

        plt.xlim(-axis_max, axis_max)
        plt.ylim(-axis_max, axis_max)
        
        plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
        plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
        
        for i in range(df.shape[0]):
            plt.text(
                x=df[f'{col1}_z'].iloc[i]+0.05,
                y=df[f'{col2}_z'].iloc[i]+0.05,
                s=df[header].iloc[i],
                fontsize=9,
                alpha=0.8
            )
        
        plt.text(0.95, 0.95, f'High {col1}\nHigh {col2}', ha='right', va='top', 
                transform=plt.gca().transAxes, color='darkred')
        plt.text(0.05, 0.95, f'Low {col1}\nHigh {col2}', ha='left', va='top', 
                transform=plt.gca().transAxes, color='darkred')
        plt.text(0.95, 0.05, f'High {col1}\nLow {col2}', ha='right', va='bottom', 
                transform=plt.gca().transAxes, color='darkred')
        plt.text(0.05, 0.05, f'Low {col1}\nLow {col2}', ha='left', va='bottom', 
                transform=plt.gca().transAxes, color='darkred')
        
        plt.title(f'{title}\n(z-score standardized)', pad=20)
        plt.xlabel(f'{col1} deviation (z-score)')
        plt.ylabel(f'{col2} deviation (z-score)')
        
        plt.legend(bbox_to_anchor=(0.05, 0.9), loc='upper left', title=header)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f'Error in plotting {title}: {e}')

def getCityVariance2D(src = DATA_SOFTWARE_ENGINEER_SALARY):
    ''' Params:
    - `src`: the source file path of the dataset.

    Returns None. Plots the 2D scatter plot of the software engineer salary statistics.'''
    try:
        df = pd.read_csv(src)
        df['max-min'] = df['max'] - df['min'] # gap
        getVariance2D(df, 'city', 'median', 'max-min', 'Software Engineer Mean Salary Variance in North America')
    except Exception as e:
        print(f'Error in plotting software engineer salary statistics: {e}')

def getCorrelation(df, colA, colB):
    '''Params:
    - `df`: the pandas Dataframe of combined dataset.
    - `colA`: the column name of the Dataframe to calculate the correlation with `colB`.
    - `colB`: the column name of the Dataframe to calculate the correlation with `colA`.
    
    Returns None. Print the results directly in Pearson Correlation Coefficient, Spearman's rank correlation coefficient, Kendall cofficient of concordance respectively.'''
    try:
        pearson_corr = df[colA].corr(df[colB])
        print(f"Pearson correlation coefficient: {pearson_corr}")

        spearman_corr = df[colA].corr(df[colB], method='spearman')
        print(f"Spearman correlation coefficient: {spearman_corr}")

        kendall_corr = df[colA].corr(df[colB], method='kendall')
        print(f"Kendall correlation coefficient: {kendall_corr}")
    except Exception as e:
        print(f'Error in calculating correlation of {colA} and {colB} of: {e}')

def getCityVarianceCorrelation(src = DATA_SOFTWARE_ENGINEER_SALARY):
    '''Params:
    - `src`: the source file path of the dataset.

    Returns None. Print the results of the correlation of the software engineer salary statistics.'''
    try:
        df = pd.read_csv(src)
        df['max-min'] = df['max'] - df['min'] # gap
        getCorrelation(df, 'median', 'max-min')
    except Exception as e:
        print(f'Error in calculating correlation of software engineer salary statistics: {e}')

def getHeatMap(df, cols, title):
    '''Params:
    - `df`: the pandas Dataframe of combined dataset.
    - `cols`: the list of column names to be plotted.
    - `title`: the title of the plot.

    Returns None. Plots the heatmap of the correlation of the columns.'''
    try:
        corr = df[cols].corr()
        print(corr)
        plt.figure(figsize=(5, 4))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
        plt.title(title)
        plt.show()
    except Exception as e:
        print(f'Error in plotting heatmap of {title}: {e}')

def getUSSalaryHeatMap(src = DATA_US_SOFTWARE_DEVELOPER_SALARIES):
    '''Params:
    - `src`: the source file path of the dataset.

    Returns None. Plots the heatmap of the correlation of the software engineer salary statistics.'''
    try:
        df = pd.read_csv(src)
        getHeatMap(df, ['salary', 'num_jobs', 'purchasing_power'], 'Software Engineer Salary Correlation')
    except Exception as e:
        print(f'Error in plotting heatmap of software engineer salary statistics: {e}')

def getUSSalaryBoxPlot(src = DATA_US_SOFTWARE_DEVELOPER_SALARIES):
    '''Params:
    - `src`: the source file path of the dataset.

    Returns None. Prints and Plots EDA (Exploratory Data Statistics) of the software engineer salary statistics.'''
    try:
        df = pd.read_csv(src)
        print(df.describe())
        
        plt.figure(figsize=(4, 6))
        df_normalized = (df[['salary', 'num_jobs', 'purchasing_power']]  - df[['salary', 'num_jobs', 'purchasing_power']].mean()) / df[['salary', 'num_jobs', 'purchasing_power']].std()
        sns.boxplot(data=df_normalized.melt(), x="variable", y="value", hue="variable", palette="Set2", width=0.5, legend=False)
        plt.xticks(rotation=15)
        plt.xlabel("")
        plt.ylabel("Normalized Values", fontsize=10)
        plt.title("Standardized Distribution Comparison")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f'Error in EDA of software engineer salary statistics: {e}')

def getUSSalaryRelationCharts(src=DATA_US_SOFTWARE_DEVELOPER_SALARIES):
    '''Params:
    - `src`: the source file path of the dataset.

    Returns None. Plots the scatter plot of the software engineer salary statistics.
    
    Abandoned'''
    try:
        df = pd.read_csv(src)
        plt.figure(figsize=(12, 8))
        
        # Create PairGrid with full matrix (corner=False)
        g = sns.PairGrid(df[['salary', 'num_jobs', 'purchasing_power']], 
                         diag_sharey=False, corner=False)
        
        g.map_lower(sns.scatterplot, alpha=0.7, s=60, color='#4B8BBE')
        g.map_diag(sns.histplot, kde=True, color='#306998', bins=15, edgecolor='w')
        # Upper triangle: empty (or use g.map_upper(sns.kdeplot) for density contours)

        for ax in g.axes.flatten():
            if ax.get_xlabel() == 'salary':
                ax.set_xlabel("Salary (USD)", fontsize=10)
            elif ax.get_xlabel() == 'num_jobs':
                ax.set_xlabel("Job Count", fontsize=10)
            elif ax.get_xlabel() == 'purchasing_power':
                ax.set_xlabel("Purchasing Power Index", fontsize=10)
            if ax.get_ylabel() == 'salary':
                ax.set_ylabel("Salary (USD)", fontsize=10)
            elif ax.get_ylabel() == 'num_jobs':
                ax.set_ylabel("Job Count", fontsize=10)
            elif ax.get_ylabel() == 'purchasing_power':
                ax.set_ylabel("Purchasing Power Index", fontsize=10)
        
        plt.suptitle("Relationship Matrix: Salary, Job Count, and Purchasing Power", y=0.92)
        plt.tight_layout(pad=2) 
        plt.show()
        
    except Exception as e:
        print(f'Error in plotting scatter plot of software engineer salary statistics: {e}')

def getUSSalaryKDEPlot(src=DATA_US_SOFTWARE_DEVELOPER_SALARIES):
    '''Params:
    - `src`: the source file path of the dataset.

    Returns None. Plots the scatter plot of the software engineer salary statistics.'''
    df = pd.read_csv(src)

    salary = df['salary']
    num_jobs = df['num_jobs']
    # getCorrelation(df, 'salary', 'num_jobs')
    sns.jointplot(x=salary, y=num_jobs, kind='kde', height=8,fill=True, cmap='Blues')
    plt.suptitle('Joint Density: Salary & Job Numbers', y=1.02)
    plt.tight_layout()
    plt.show()


    # other plotting attempts (not strong conclusion as KDE provide, so abandoned)
    '''
    lowess = sm.nonparametric.lowess(num_jobs, salary, frac=0.5) 
    plt.figure(figsize=(10, 6))
    plt.scatter(salary, num_jobs, alpha=0.6, label='Data Points')
    plt.plot(lowess[:, 0], lowess[:, 1], 'r-', lw=2, label='LOESS Fit')
    plt.title('Salary vs. Job Numbers (LOESS Smoothing)')
    plt.xlabel('Salary ($)')
    plt.ylabel('Number of Jobs')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()'''
    
    ''' ploy fit
    coefficients = np.polyfit(salary, num_jobs, 2)
    poly_func = np.poly1d(coefficients)
    x_fit = np.linspace(salary.min(), salary.max(), 100)
    y_fit = poly_func(x_fit)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=salary, y=num_jobs, alpha=0.6, label='Data Points')
    plt.plot(x_fit, y_fit, 'r-', label=f'Quadratic Fit: y = {coefficients[0]:.2e}x² + {coefficients[1]:.2f}x + {coefficients[2]:.2f}')

    percentiles = [25, 50, 75]
    colors = ['blue', 'green', 'orange']
    for p, color in zip(percentiles, colors):
        x_val = np.percentile(salary, p)
        y_val = np.percentile(num_jobs, p)
        plt.scatter(x_val, y_val, s=100, c=color, zorder=5, 
                    label=f'{p}% Percentile (Salary={x_val:.0f}$, Jobs={y_val:.0f})')

    plt.title('Salary vs. Job Numbers (Quadratic Fit)', pad=20)
    plt.xlabel('Salary ($)')
    plt.ylabel('Number of Jobs')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()
    '''

    ''' linear fit
    plt.figure(figsize=(10, 6))
    sns.regplot(x=df['salary'], y=df['num_jobs'], scatter_kws={'alpha':0.6})
    plt.title('Salary vs. Number of Jobs (r=0.78)', pad=20)
    plt.xlabel('Salary ($)')
    plt.ylabel('Number of Jobs')
    plt.grid(True, alpha=0.3)

    # Annotate key percentiles
    percentiles = [25, 50, 75]
    for p in percentiles:
        x_val = np.percentile(df['salary'], p)
        y_val = np.percentile(df['num_jobs'], p)
        plt.annotate(f'{p}%', (x_val, y_val), 
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center')

    plt.tight_layout()
    plt.show()
    '''

if __name__ == '__main__':
    getAnnualLineCharts()
    getAnuualWageLinearRegression()
    getCityBarCharts()
    getCityVariance2D()
    getCityVarianceCorrelation()
    getUSSalaryBoxPlot()
    getUSSalaryHeatMap()
    # getUSSalaryRelationCharts()
    getUSSalaryKDEPlot()
    