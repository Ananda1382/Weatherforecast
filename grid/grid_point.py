import requests
from location import location

GRID_POINTS_URL = 'https://api.weather.gov/points/{latitude},{longitude}'

def get_gridData():
    try:
        lat, lon = location.get_location()
        response = requests.get(GRID_POINTS_URL.format(latitude=lat, longitude=lon))
        response.raise_for_status()
        grid_id = response.json().get('properties')['gridId']
        grid_x = response.json().get('properties')['gridX']
        grid_y = response.json().get('properties')['gridY']
        return grid_id, grid_x, grid_y
    except Exception as e:
        print(f"Error fetching grid points: {e}")
        return None

# if __name__ == '__main__':
#     print(get_gridData())