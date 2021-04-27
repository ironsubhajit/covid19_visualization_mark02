import os

import pandas as pd
import folium
import webbrowser


global india


def clean_covid19_data(covid19):
    """cleaning covid19 data for easy to use"""
    print('Cleaning covid19 Data...')
    covid19 = covid19.iloc[:-2, :-4]
    covid19.columns = ['State', 'Total cases', 'Deaths', 'Recoveries', 'Active cases']
    return covid19


def clean_coordinates_data(coordinates):
    """cleaning coordinates data (removing degree etc.)"""
    print('Cleaning coordinates Data...')
    coordinates['Latitude'] = coordinates['Latitude'].apply(lambda cord: cord[0:5]).astype('float')
    coordinates['Longitude'] = coordinates['Longitude'].apply(lambda cord: cord[0:5]).astype('float')
    return coordinates


def merged_data(coordinates, covid19):
    """merging two DataFrames"""
    print("Merging coordinates and covid19 data...")
    final_data = pd.merge(coordinates, covid19, how='inner', on='State')
    return final_data


def zip_final_data(final_data):
    """zip the merged data"""
    final_zip_data = zip(list(final_data['State']), list(final_data['Latitude']),
                         list(final_data['Longitude']), list(final_data['Total cases']),
                         list(final_data['Deaths']), list(final_data['Recoveries']),
                         list(final_data['Active cases']))
    return final_zip_data


def mark_on_map(final_zip_data, india):
    """make mark form the zipped data on india"""

    for state, lat, long, total_cases, Death, Recov, Active in final_zip_data:
        # for creating circle marker
        folium.CircleMarker(location=[lat, long], radius=5, color='red',
                            fill=True, fill_color="red").add_to(india)
        # for creating marker
        folium.Marker(location=[lat, long],
                      # adding information that need to be displayed on popup
                      popup=folium.Popup(('<strong><b>State  : ' + state + '</strong> <br>' +
                                          '<strong><b>Total Cases : ' + total_cases + '</striong><br>' +
                                          '<strong><font color= red>Deaths : </font>' + Death + '</striong><br>' +
                                          '<strong><font color=green>Recoveries : </font>' + Recov + '</striong><br>' +
                                          '<strong><b>Active Cases : ' + Active + '</striong>'),
                                         max_width=200)).add_to(india)
    # return map object
    return india


def save_file(file_name):
    """save the file in the projects directory & return file path"""
    project_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_dir_path, f'{file_name}.html')
    map = india
    map.save(file_path)

    #print(f"File Saved to {file_path}")
    return file_path


def auto_open(file_path):
    """open map.html file automatically"""
    webbrowser.open_new_tab(file_path)



# get coordinates of states
print("scraping coordinates data... ")
info = pd.read_html(
    'http://www.quickgs.com/latitudinal-and-longitudinal-extents-of-india-indian-states-and-cities/')

# creates a df from that table data
coordinates = pd.DataFrame(info[0])

# get corona statistics for the States
print("scraping covid19 data... ")
corona_stats = pd.read_html('https://en.wikipedia.org/wiki/COVID-19_pandemic_in_India#covid19-container',
                           match='State/Union Territory')
# creates df from corona statistics data
covid19 = pd.DataFrame(corona_stats[0])

# new & cleaned coordinates data
coordinates = clean_coordinates_data(coordinates)

# new & cleaned covid19 data
covid19 = clean_covid19_data(covid19)

# joining two Dataframes
final_data = merged_data(coordinates, covid19)

# get zipped data from final data
final_zip_data = zip_final_data(final_data)

# create map of india and zoomed to it

india = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# get the new marked map
india = mark_on_map(final_zip_data, india)

# saving the map
#file_name = input("Enter file name in which you want to save the map: ")
#file_path = save_file(file_name)

# visualizing the final output
#auto_open(file_path)
