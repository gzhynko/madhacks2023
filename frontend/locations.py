import googlemaps
import json

def parse_building_list():
    input_string = """1220 Capitol Court (Primate Annex)	0782
    1410 Engineering Dr.	0486
    1433 Monroe St.	1095
    1610 University Ave.	0129
    1800 University Ave.	0113
    1910 Linden Dr.	0103
    206 Bernard Ct.	1082
    209 N. Brooks St.	0788
    215-217 N. Brooks St.	1060
    21 N. Park St.	1078
    30 N. Mills St.	0124
    333 East Campus Mall	0467
    432 East Campus Mall	0515A
    445 Henry Mall	0102
    45 N. Charter St.	0504
    502 Herrick Dr.	0111
    702 W. Johnson St.	1072
    711 State St.	8122
    901 University Bay Dr.	0547
    Adams Residence Hall	0564
    Agricultural Bulletin Building	0078
    Agricultural Dean's Residence	0072
    Agricultural Engineering Building	0080
    Agricultural Engineering Laboratory	0099
    Agricultural Hall	0070
    Alumni Hall, 1100 Delaplaine Ct.	1000001
    American Family Children's Hospital	1426
    Animal Science Building	0118
    Apartment Facilities Office	
    Armory and Gymnasium (Red Gym)	0020
    Art Lofts	0220
    Athletics Operations Building	0584
    Atmospheric, Oceanic and Space Sciences Building	0156
    Babcock Hall	0106
    Bakke Recreation & Wellbeing Center	0081
    Bardeen Medical Laboratories	0451B
    Barnard Residence Hall	0560
    Bascom Hall	0050
    Below Alumni Center	0489
    Bernie’s Place Childcare	1239
    Biotron Laboratory	0045
    Birge Hall	0054
    Bock Laboratories	0033
    Bradley Memorial Building	0452
    Bradley Residence Hall	0506
    Brogden Psychology Building	0470
    Camp Randall Sports Center	0025
    Camp Randall Stadium	0022
    Carillon Tower	0487
    Carl Schuman Shelter	0116
    Carson Gulley Center	0565
    CDIS Building (opening fall 2025)	
    Cereal Crops Research Unit	0121
    Chadbourne Residence Hall	0557
    Chamberlin Hall	0055
    Chamberlin House (Kronshage)	0571
    Charter Street Heating and Cooling Plant	0529
    Chazen Museum of Art	0524
    Chemistry Building	0047
    Cole Residence Hall	0555
    Computer Sciences	0155
    Conover House (Kronshage)	0574C
    Conrad A. Elvehjem Building	0544
    Dairy Barn	0105
    Dairy Cattle Center	0092
    Davis Residence Hall	0578
    D.C. Smith Greenhouse	0206
    Dejope Residence Hall	0567
    DeLuca Biochemical Sciences Building	0204
    DeLuca Biochemistry Building	0084
    DeLuca Biochemistry Laboratories	0205
    Discovery Building	0212
    Eagle Heights	
    Eagle Heights Buildings 101-108	
    Eagle Heights Buildings 201-209	
    Eagle Heights Buildings 301-309	
    Eagle Heights Buildings 401-408	
    Eagle Heights Buildings 501-509	
    Eagle Heights Buildings 601-610	
    Eagle Heights Buildings 701-819	
    Eagle Heights Buildings 901-946	
    Eagle Heights Community Center	1299
    Education Building	0400
    Engineering Centers Building	0481
    Engineering Hall	0408
    Engineering Research Building	0762
    Environmental Health and Safety Building	0549
    Enzyme Institute	0479
    Extension Building	0500
    Field House	0029
    Fleet and Service Garage	1077
    Fluno Center For Executive Education	0139
    Forest Products Laboratory	0036
    Genetics-Biotechnology Center Building	0082
    Gilman House (Kronshage)	0569
    Goodman Softball Complex	0175
    Goodnight Hall	0508
    Gordon Dining and Event Center	1249
    Grainger Hall	0140
    Hamel Music Center	0585
    Hanson Biomedical Sciences Building	0094
    Harlow Primate Lab	0527
    Harvey Street Apartments	
    Hasler Laboratory of Limnology	0483
    Health Sciences Learning Center	1480
    Helen C. White Hall	0018
    Hiram Smith Annex	0077
    Hiram Smith Hall	0076
    Holt Center (Kronshage)	0574H
    Horse Barn	0095
    Horticulture	0087B
    Humphrey Hall	0136
    Ingraham Hall	0056
    Integrative Biology Research Building	0401
    Jones House (Kronshage)	0572
    Jorns Hall	0137
    Kellner Hall	0460
    King Hall	0074A
    Kronshage Residence Hall	
    LaBahn Arena	0227
    Lathrop Hall	0032
    Law Building	0430
    Leopold Residence Hall	0576
    Livestock Laboratory	0115
    Lowell Center	0502
    Mack House (Kronshage)	0570
    Materials Science and Engineering Building	0520
    McArdle Building	0468
    McClain Athletic Facility	0021
    Meat Microbiology Lab	0249
    Meat Science and Muscle Biology Lab	0123
    Meat Science & Animal Biologics Discovery	0149
    Mechanical Engineering Building	0407
    Medical Sciences	0451C
    Medical Sciences Center	0450
    Meiklejohn House	0035
    Memorial Library	0015
    Memorial Union	0008
    Merit Residence Hall	0575
    Microbial Sciences	0060
    Middleton Building	0455
    Moore Hall - Agronomy	0087A
    Mosse Humanities Building	0469
    Music Hall	0485
    Nancy Nicholas Hall	0085
    Nicholas-Johnson Pavilion and Plaza	0226
    Nicholas Recreation Center	0026
    Nielsen Tennis Stadium	0038
    Noland Hall	0402
    North Hall	0052
    Nutritional Sciences	0449
    Observatory Hill Office Building	0512
    Ogg Residence Hall	1243
    Phillips Residence Hall	0507
    Plant Sciences	0087C
    Police and Security Facility	0550
    Porter Boathouse	0172
    Poultry Research Laboratory	0110
    Pyle Center	0006
    Radio Hall	0405
    Rennebohm Hall	0034
    Russell Laboratories	0114
    Rust-Schreiner Hall	0158
    School of Social Work Building	0453
    Science Hall	0053
    Sellery Residence Hall	1245
    Service Memorial Institute	0451A
    Sewell Social Sciences	0046
    Showerman House (Kronshage)	0574S
    Signe Skott Cooper Hall	0044
    Slichter Residence Hall	0558
    Smith Residence Hall	1079
    Soils Building	0074B
    Southeast Residence Halls	
    South Hall	0051
    Steenbock Library	0079
    Sterling Hall	0057
    Stock Pavilion	0090
    Stovall Building (Wisconsin State Laboratory of Hygiene)	0476
    Sullivan Residence Hall	0556
    Swenson House (Kronshage)	0573
    Taylor Hall	0464
    Teacher Education	0153
    The Kohl Center	0225
    Tripp Residence Hall	0563
    Turner House (Kronshage)	0568
    Union South	0088
    University Club	0515B
    University Hospital	1400
    University Houses	1201
    U.S. Dairy Forage Research Center	0096
    UW Foundation	0493
    UW Medical Foundation Centennial Building	1435
    Van Hise Hall	0482
    Van Vleck Hall	0048
    Veterans Administration Hospital	1055
    Veterinary Medicine	0093
    Vet Med Expansion (Under Construction, 2023)	0793
    Vilas Hall	0545
    Waisman Center	0459
    Walnut Street Greenhouse	0122
    Walnut Street Heating and Cooling Plant	0049
    WARF Office Building	0039
    Washburn Observatory	0510
    Water Science and Engineering Laboratory	0403
    Waters Residence Hall	0559
    Weeks Hall for Geological Sciences	0521
    Wendt Commons	0404
    West Campus Cogeneration Facility	0120
    Wisconsin Energy Institute	0752
    Wisconsin Historical Society	0016
    Wisconsin Institutes for Medical Research	1485
    Wisconsin Primate Center	0526
    Wisconsin Veterinary Diagnostic Laboratory	0126
    Witte Residence Hall	1246
    Zoe Bayliss Co-Op	0577"""

    # Split the string into lines
    lines = input_string.splitlines()

    # Initialize an empty list to store the parsed data
    parsed_data = []

    # Loop through each line and split it into components
    for line in lines:
        components = line.split('\t')  # Assuming the tab character is used as the delimiter
        components[0] = components[0].strip()
        print(components[0])
        parsed_data.append(components)

    return parsed_data


def get_coordinates(api_key, building_name):
    gmaps = googlemaps.Client(key=api_key)
    # query = f"{building_name}, University of Wisconsin-Madison"
    query = f"{building_name}"
    geocode_result = gmaps.geocode(query)

    geocode_result = gmaps.find_place(query, 'textquery', ['geometry/location'], 'circle:16000@43.076242,-89.404499')
    # print('geocode_result')
    # print(geocode_result)
    # geocode_result = gmaps.geocode(building_name)

    if geocode_result and geocode_result['candidates'] and geocode_result['candidates'][0]:
        # location = geocode_result[0]['geometry']['location']
        location = geocode_result['candidates'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return {'name': building_name, 'latitude': latitude, 'longitude': longitude}
    else:
        return None
    
def main():
    api_key = 'AIzaSyDmUmZAlA0755_h2ndv5RRmZYeMofPO03c'
    
    # Array of building names and codes
    # building_data = [
    #     ['Vilas Hall', '0545'],
    #     ['Waisman Center', '0459'],
    #     # Add more buildings as needed
    # ]

    building_data = parse_building_list();

    # Dictionary to store building data
    # buildings = {}

    # # Iterate through the array and get coordinates
    # for building in building_data:
    #     building_name = building[0]
    #     coordinates = get_coordinates(api_key, building_name)

    #     if coordinates:
    #         buildings[building_name] = {'latitude': coordinates['latitude'], 'longitude': coordinates['longitude']}
    #     else:
    #         print(f"Location not found for {building_name}")

    # # Save the data to a JSON file
    # with open('uw_madison_buildings.json', 'w') as json_file:
    #     json.dump(buildings, json_file, indent=2)

    # # List to store building data
    buildings = []

    # Iterate through the array and get coordinates
    for building in building_data:
        building_name = building[0]
        coordinates = get_coordinates(api_key, building_name)

        if coordinates:
            print(f"Found {building_name}")
            buildings.append(coordinates)
        else:
            print(f"Location not found for {building_name}")

    # Save the data to a GeoJSON file
    geojson_data = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [building['longitude'], building['latitude']]
                },
                'properties': {'name': building['name']}
            }
            for building in buildings
        ]
    }

    with open('uw_madison_buildings.js', 'w') as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2)

if __name__ == "__main__":
    main()

# # Replace 'YOUR_API_KEY' with your actual Google Maps API key
# gmaps = googlemaps.Client(key='AIzaSyDmUmZAlA0755_h2ndv5RRmZYeMofPO03c')

# # Example: Get latitude and longitude for a building
# building_name = "Engineering Hall, University of Wisconsin-Madison"
# geocode_result = gmaps.geocode(building_name)

# # Extract latitude and longitude
# if geocode_result:
#     location = geocode_result[0]['geometry']['location']
#     latitude = location['lat']
#     longitude = location['lng']

#     print(f"{building_name}: Longitude {longitude}, Latitude {latitude}")
# else:
#     print(f"Location not found for {building_name}")

# # Display the parsed data
# for data in parsed_data:
#     print(data + ",")