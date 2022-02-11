"""
lab 1 taks 2
"""
import folium
import pandas
from geopy.geocoders import Nominatim
import geopy.distance


def find_distance_(place1, place2):
    """
    returns distance between two points with coordinates(tuple)
    >>> find_distance_((49.841952, 24.0315921),(50.4501, 30.5234))
    468.7722690754584
    """
    return geopy.distance.geodesic(place1, place2).km

def find_coordinates(place):
    """
    returns latitude and longitude
    >>> find_coordinates('Lviv')
    (49.841952, 24.0315921)
    """
    locator = Nominatim(user_agent="main.py")
    coord = locator.geocode(place)
    return coord.latitude, coord.longitude

def info_about_film(year, name):
    """
    returns list of film name, year, location and coordinates of location
    >>> info_about_film(2004,'locations.csv')
    set()
    """
    name_1 = pandas.read_csv(name, error_bad_lines=False)
    year_1 = name_1['year']
    locations = name_1['location']
    film = name_1['movie']
    info = set()
    for word in range(len(film)):
        try:
            if int(year_1[word]) == year and locations[word] != 'NO DATA':
                info.add((film[word], find_coordinates(locations[word]), locations[word]))
        except AttributeError:
            pass
        except ValueError:
            pass
    return info

if __name__ == '__main__':
    info_1 = []
    yea, lat, lon = (map(float, input('Enter year, latitude and longitude: ').split()))
    path_to_dataset = input('Enter dataset: ')
    coordinates = (lat, lon)
    print('Map is generating, wait a minute...')
    info_ = info_about_film(yea, path_to_dataset)
    for element in info_:
        info_1.append((find_distance_(coordinates, element[1]), element[0], element[1], element[2]))
    info_new = sorted(info_1[:10])
    mapp = folium.Map(location=[lat, lon], zoom_start=11)
    feat = folium.FeatureGroup(name='Point')
    feat.add_child(folium.CircleMarker([lat, lon], popup='my_point', tooltip='me'))
    near = folium.FeatureGroup(name='Filmed nearby')
    for elem in range(len(info_new)):
        tooltip = str(info_1[elem][3])
        near.add_child(folium.CircleMarker([info_new[elem][2][0], info_new[elem][2][1]], popup=info_new[elem][1], tooltip=tooltip))
    mapp.add_child(near)
    mapp.add_child(feat)
    mapp.add_child(folium.LayerControl())
    mapp.save("map.html")
