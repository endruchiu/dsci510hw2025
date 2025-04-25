import kagglehub
import requests
import os
import pandas as pd
import glob
import zipfile
import re
import bs4
import json
import shutil

def getUSSoftwareDeveloperSalariesData(out_file="data/data_US_software_developer_salaries.csv", force_download=True):
    ''' Get U.S. Software Developer Salaries datasets (2022) from Kaggle API 
    from https://www.kaggle.com/datasets/thedevastator/u-s-software-developer-salaries

    Param:
    - `out_file`: output file path name
    - `force_download`: whether re-download even if already downloaded (cache)

    returns None
    '''
    try:
        # downloaded into cache directory (path) via API
        path = kagglehub.dataset_download("thedevastator/u-s-software-developer-salaries", force_download=force_download)
        file = 'SofwareDeveloperIncomeExpensesperUSACity.csv'
        src_path = os.path.join(path, file)
        df = pd.read_csv(src_path)
        os.remove(src_path)
        # save the key and stable columns to avoid redundant and outliers
        df = df[['City', 'Mean Software Developer Salary (unadjusted)', 'Number of Software Developer Jobs', 'Local Purchasing Power avg']]
        # rename for convenience
        df.columns = ['city', 'salary', 'num_jobs', 'purchasing_power']
        df.to_csv(out_file, index=False)
        print(f'DATASET1: Wrote {out_file} of data U.S. Software Developer Salaries successfully!')
    except Exception as e:
        print(f'Error in getUSSoftwareDeveloperSalariesData: {e}')
# testing
# getUSSoftwareDeveloperSalariesData()

def getAnnualWageStatisticsData(out_file="data/data_annual_wage_statistics.csv"):
    ''' Get Annual Wage Statistics (2012-2024) from web scrape request
    from alternative URL https://0x0.st/8Onq.zip , since the origin websites 
    https://www.bls.gov/oes/tables.htm is prohibited from scrape robot.

    The alternative URL is created by myself, I download the data from origin websites first and upload it in the alternative URL to make it available by python request scripts.

    Param:
    - `out_file`: output file path name
    - `src_folder`: source folder path name (download from National XLS href and put altogether in the folder)

    returns None
    '''
    
    # STEP1: download from data source
    url = 'https://0x0.st/8Onq.zip' # alternative data source
    src_folder = 'OEWS' # the path of extracted data
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(f'{src_folder}.zip', 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                if chunk:
                    f.write(chunk)
        print(f'Download from {url} successfully!')
    except Exception as e:
        print(f'Error in downloading data: {e}')
        return
    
    # STEP2: unzip
    try:
        with zipfile.ZipFile(f'{src_folder}.zip', 'r') as zip_ref:
            zip_ref.extractall(src_folder)
        print(f'Unzipped {src_folder}.zip successfully!')
    except Exception as e:
        print(f'Error in unzipping {src_folder}.zip: {e}')
        return
    src_folder = os.path.join(src_folder, src_folder) # deal with nesting
    try:
        for file in glob.glob(os.path.join(src_folder, "*.zip")):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall()
    except Exception as e:
        print(f'Error in unzipping files in {src_folder}: {e}')
        return
    print(f'Unzipped all data of annual wage statistics from {src_folder}/ successfully!')

    # STEP3: merge all into one csv
    try:
        rows = []
        # file format (? as any character): oesm??nat/national_M20??_dl.xls(x)
        for file in glob.glob("**/national*"): 
            year = int(re.findall(r'\d+', file)[-1])
            df = pd.read_excel(file)
            # special judge for year 2019
            if year == 2019:
                df.columns = df.columns.str.upper()
            
            mask = df['OCC_TITLE'] == 'Computer Programmers'
            df.loc[mask, 'Year'] = year  # add new field
            columns = ['A_PCT10', 'A_PCT25', 'A_MEAN', 'A_MEDIAN', 'A_PCT75', 'A_PCT90', 'Year']
            rows.append(df.loc[mask, columns].copy())  
        df = pd.concat(rows)
        # sort the columns
        cols = df.columns.tolist()
        cols = [cols[-1]] + cols[:-1]
        df = df[cols] 
        df.to_csv(out_file, index=False)
    except Exception as e:
        print(f'Error in merging files: {e}')
        return
    print(f'Merged all data of annual wage statistics into {out_file} successfully!')

    # STEP4: clean up (unzip files)
    try:
        for file in glob.glob("oesm??nat"): 
            shutil.rmtree(file)
        shutil.rmtree('OEWS')
        os.remove('OEWS.zip')
    except Exception as e:
        print(f'Error in cleaning up: {e}')

    print(f'DATASET2: Wrote {out_file} of data Annual Wage Statistics successfully!')
# testing
# getAnnualWageStatisticsData()

def getSoftwareEngineerSalaryData(out_file="data/data_software_engineer_salary.csv", remove_cache=True):
    ''' Get Software Engineer Salary from web scrape request
    from https://www.levels.fyi/locations?jobFamily=Software+Engineer

    Param:
    - `out_file`: output file path name
    - `remove_cache`: whether remove cache or not

    returns None
    '''

    # STEP1: get city list
    # STEP1.1: scrape the HTML city list via HTTP GET request
    if not os.path.exists('tmp.html'):
        session = requests.Session()
        url_menu = 'https://www.levels.fyi/locations?jobFamily=Software+Engineer'
        try:
            response = session.get(url_menu)
            response.raise_for_status()
            html = response.text
            with open('tmp.html', 'w', encoding='utf-8') as f: # cache
                f.write(html)
        except Exception as e:
            print(f'Error in url: {e}')
            if hasattr(e, 'response'):
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Headers: {e.response.headers}")
                print(f"Response Text: {e.response.text}")
                return
        print(f'Get city list from {url_menu} successfully!')
    else:
        with open('tmp.html', 'r', encoding='utf-8') as f: # cache
            html = f.read()
        print(f'read city lists from cache already!')

    # STEP1.2: parse the HTML city list via BeautifulSoup, json
    try:
        soup = bs4.BeautifulSoup(html, features="html.parser")
        # by looking the HTML source code, find the structure 
        data_script = soup.find('script', id='__NEXT_DATA__')
        json_str = data_script.string
        json_data = json.loads(json_str)
        data = json_data['props']['pageProps']['locations']['North America']
        slugs = [item['slug'] for item in data] 
    except Exception as e:
        print(f'Error in parsing city lists: {e}')
        return

    # STEP2: scrapt salary data of each city via HTTP GET request
    for city in slugs:
        url = f'https://www.levels.fyi/t/software-engineer/locations/{city}'
        if os.path.exists(f'tmp-{city}.html'): # cache
            print(f'cached {city} data already!')
            continue
        try:
            response = session.get(url)
            response.raise_for_status()
            html = response.text
            with open(f'tmp-{city}.html', 'w', encoding='utf-8') as f: # cache
                f.write(html)
                print(f'Get {city} data from {url} successfully!')
        except Exception as e:
            print(f'Error in {city} url: {e}')
            if hasattr(e, 'response'):
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Headers: {e.response.headers}")

    # STEP3: parse the HTML salary data via BeautifulSoup
    rows = []
    try:
        for city in slugs:
            data = {'city': city}
            with open(f'tmp-{city}.html', encoding='utf-8') as f:
                html = f.read()
            soup = bs4.BeautifulSoup(html, features="html.parser")

            h3_tags = soup.find_all('h3', class_=lambda x: x and x.startswith('percentiles_medianAmount'))
            text = [h3.get_text() for h3 in h3_tags][0]
            text = re.findall(r'\d+,\d+', text)[0]
            data['median'] = int(text.replace(',', ''))

            divs = soup.find_all('div', class_=lambda x: x and x.startswith('percentiles_percentileCard'))
            for div in divs: # only 1 div
                p_tags = div.find_all('p', class_='MuiTypography-root')
                for p_tag in p_tags:
                    text = p_tag.get_text()
                    if 'The average' in text:
                        salaries = re.findall(r'\d+,\d+', text)
                        salaries = [int(i.replace(',', '')) for i in salaries]
                        data['min'] = salaries[0]
                        data['max'] = salaries[1]
                        # date = re.findall(r'\d+/\d+/\d+', text)[0]
                        # data['date'] = date
            rows.append(data)
    except Exception as e:
        print(f'Error in parse salary data: {e}')
        return

    # STEP4: save the salary data to CSV file
    try:
        df = pd.DataFrame(rows)
        df.to_csv(out_file, index=False)
    except Exception as e:
        print(f'Error in save data to {out_file}: {e}')
        return

    # STEP5: remove cache
    if remove_cache:
        try:
            for file in glob.glob('tmp*'):
                os.remove(file)
        except Exception as e:
            print(f'Error in remove cache: {e}')
        print('Remove cache successfully!')
    print(f'DATASET3: Wrote {out_file} of data software engineer salary successfully!')
# testing
# getSoftwareEngineerSalaryData(remove_cache=False)

def main():
    print('Start getting data from websites.')
    try:
        os.makedirs('data', exist_ok=True)
        getUSSoftwareDeveloperSalariesData()
        getAnnualWageStatisticsData()
        getSoftwareEngineerSalaryData()
    except Exception as e:
        print(f'Error in main: {e}')
    print('All data preprocessing finished!')
if __name__ == '__main__':
    main()