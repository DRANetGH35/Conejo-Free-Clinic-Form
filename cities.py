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
