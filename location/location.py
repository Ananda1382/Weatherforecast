import requests

LOCATION_API_URL = 'https://ipinfo.io/json'

def get_location():
    try:
        response = requests.get(LOCATION_API_URL)
        response.raise_for_status()
        data = response.json()
        location = data.get('loc').split(",")
        return location[0], location[1]
    except requests.exceptions.RequestException as e:
        print(f"Error in fetching the location: {e}")
        return None, None

# if __name__ == '__main__':
#     print(get_location())