from bs4 import BeautifulSoup

def xml_reader():

    points = []
    
    with open('fp.xml', 'r') as f:
        data = f.read()
    
    soup = BeautifulSoup(data, "xml")
    
    wp = soup.find_all('wp')

    for match in wp:

        wp_altitude = match.find_all('altitude-ft')
        altitude_val = int(wp_altitude[0].contents[0])

        wp_lon = match.find_all('lon')
        lon_val = float(wp_lon[0].contents[0])

        wp_lat = match.find_all('lat')
        lat_val = float(wp_lat[0].contents[0])

        wp_id = match.find_all('ident')
        id_name = wp_id[0].contents[0]

        points.append(lon_val)
        points.append(lat_val)

    return points