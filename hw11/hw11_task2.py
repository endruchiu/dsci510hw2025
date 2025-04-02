#task 2
!pip install requests
import requests
import xml.etree.ElementTree as ET

def land_scraper(cities_file: str) -> str:
    API_KEY = "310eb161d567417ab9a6b538d985f397"  #opencage API
    
    with open(cities_file, 'r') as f:
        cities = [line.strip() for line in f if line.strip()]
    
    city_data = []
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    
    for city in cities:
        url = f"{base_url}?key={API_KEY}&q={requests.utils.quote(city)}&language=en&pretty=1"
        response = requests.get(url)
        data = response.json()
        
        if data['results']:
            result = data['results'][0] 
            city_info = {
                "city": city,
                "latitude": result['geometry']['lat'],
                "longitude": result['geometry']['lng']
            }
            city_data.append(city_info)
        else:
            print(f"Warning: No results found for {city}")
    
    root = ET.Element("cities")
    for city in city_data:
        city_elem = ET.SubElement(root, "city")
        ET.SubElement(city_elem, "name").text = city["city"]
        ET.SubElement(city_elem, "latitude").text = str(city["latitude"])
        ET.SubElement(city_elem, "longitude").text = str(city["longitude"])
    
    filename = "cities.xml"
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    
    return filename

if __name__ == "__main__":
    with open("cities.txt", "w") as f:
        f.write("Los Angeles\nChicago\nNew York\n") #example output
    
    result = land_scraper("cities.txt")
    print(f"Data saved to {result}")
