from src.config import * # read config.py
import pandas as pd

# common words to filter out from the city name
FILTER_WORDS = {'greater', 'metro', 'area', 'region', 'bay', 'city', 'town', 'valley'}

def preprocess_city_name(city_str, filter_words=FILTER_WORDS):
    ''' helper function, preprocess name of city in data source 2 (`U.S. Software Developer Salaries`) to remove the descriptive words and standardize the format

    Param:
    - `city_str` : city name string
    - `filter_words` : words to filter out from the city name
    Returns:
    - `city_str` : preprocessed city name string
    '''
    parts = city_str.lower().replace('-', ' ').split()
    filtered = [p for p in parts if p not in filter_words]
    return ' '.join(filtered).title()

def findCommonCity(src2 = DATA_US_SOFTWARE_DEVELOPER_SALARIES, src3 = DATA_SOFTWARE_ENGINEER_SALARY, filter_words = FILTER_WORDS):
    ''' source 2 (`U.S. Software Developer Salaries`) and source 3 (`Software Engineer Salary`) share same column `city` with different string format, find the mapping between them.

    Param:
    - `src2` : path of source 2
    - `src3` : path of source 3
    - `filter_words` : words to filter out from the city name

    Returns:
    - pd.DataFrame with 3 columns:
        * raw_city3: Original city names from src3
        * processed_city3: Normalized names after preprocessing
        * matched_city2: Corresponding entries from src2 (or NA if no match)
    '''
    try:
        city3 = pd.read_csv(src3)['city']
        city2 = pd.read_csv(src2)['city']

        city2_mapping = {}
        for entry in city2:
            # e.g. : "San Francisco, CA" -> "San Francisco"
            city_part = entry.split(',')[0].strip()
            city2_mapping[preprocess_city_name(city_part)] = entry
        
        results = []
        for raw_name in city3:
            processed_name = preprocess_city_name(raw_name, filter_words)
            matched = city2_mapping.get(processed_name, pd.NA)
            results.append({
                "raw_city3": raw_name,
                "processed_city3": processed_name,
                "matched_city2": matched
            })
        
        df = pd.DataFrame(results)
    except Exception as e:
        print('Error in findCommonCity: ', e)
        df = None
    return df

def mergeCityData(src2=DATA_US_SOFTWARE_DEVELOPER_SALARIES,
                src3=DATA_SOFTWARE_ENGINEER_SALARY,
                dest=DATA_COMBINED):
    ''' Merges two datasets using city name mapping and saves the combined result.

    Param:
    - `src2` : path to U.S. Software Developer Salaries dataset
    - `src3` : path to Software Engineer Salary dataset
    - `dest` : output path for merged dataset

    Returns:
    - pd.DataFrame : merged dataset containing matched records from both sources
    '''
    try:
        df2 = pd.read_csv(src2)
        df3 = pd.read_csv(src3)
        commoncity = findCommonCity(src2, src3)

        valid_matches = commoncity.dropna(subset=['matched_city2'])
        
        merged_df = pd.merge(
            df3, 
            valid_matches, 
            left_on='city', 
            right_on='raw_city3'
        ).merge(
            df2, 
            left_on='matched_city2', 
            right_on='city',
            suffixes=('_src3', '_src2')
        )

        merged_df.drop(columns=['city_src2', 'city_src3', 'raw_city3', 'matched_city2'], inplace=True)
        merged_df = merged_df.rename(columns={'processed_city3':'city'})
        cols = ['city'] + [col for col in merged_df.columns if col != 'city'] # reorder columns
        merged_df = merged_df[cols]
        
        merged_df.to_csv(dest, index=False)
    except Exception as e:
        print('Error in mergeCityData: ', e)
        merged_df = None
    return merged_df

if __name__ == '__main__':
    # findCommonCity()
    mergeCityData()