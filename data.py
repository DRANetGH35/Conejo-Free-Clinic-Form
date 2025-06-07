import csv

def cities_in_california():
    cities = []
    with open('us_cities_states_counties.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            if row[2] == "California":
                cities.append(row[4])
                cities = list(set(cities))
    return cities

def languages():
    languages_list = []
    with open('flat-ui__data-Fri Jun 06 2025.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            languages_list.append(row[1])
            languages_list = list(set(languages_list))
    return languages_list