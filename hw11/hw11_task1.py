#task 1
!pip install requests beautifulsoup4 #for parsing on html
import requests
from bs4 import BeautifulSoup
import json

def sky_scraper(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    if not table:
        raise ValueError("Could not find the launch table on the page")
    
    launches = [] #Empty dictionary
    
    rows = table.find_all('tr')[1:] 
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 7:
            continue  
        
        current_launch = {
            "datetime": cells[0].text.strip(),
            "rocket": cells[1].text.strip(),
            "country": cells[2].text.strip(),
            "flight_number": cells[3].text.strip(),
            "launch_site": cells[4].text.strip(),
            "lsp": cells[5].text.strip(),
            "payload": []
        }
        payload_cell = cells[6]
        payload_items = payload_cell.find_all('li') or [payload_cell]
        
        for item in payload_items:
            text = item.text.strip()
            satellite = {
                "name": text.split('(')[0].strip() if '(' in text else text,
                "country": current_launch["country"], 
                "operator": "Unknown",  
                "orbit": "Unknown",    
                "function": "Unknown", 
                "decay": "In orbit",   
                "outcome": "Operational" 
            }
            current_launch["payload"].append(satellite)
        
        launches.append(current_launch)
    
    filename = "space_launches.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(launches, f, indent=4, ensure_ascii=False) #json file
    
    return filename

if __name__ == "__main__": #testing winki
    url = "https://en.wikipedia.org/wiki/List_of_spaceflight_launches_in_January%E2%80%93June_2022"
    result = sky_scraper(url)
    print(f"Data saved to {result}")
