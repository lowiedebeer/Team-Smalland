import pandas as pd
import matplotlib.pyplot as plt
import random

from class_train import Train
from class_station import Station

class Experiment():

    #initialize trains and stations
    def __init__(self, number_of_trains, connections, stations):
        # Read the csv-file of the connections between stations into
        # a dataframe for each csv-file.
        self.connect = pd.read_csv(connections)

        # Read the csv-file with the geographical locations of the stations
        self.stations = pd.read_csv(stations)
        self.trains_list = []
        self.train_route_list = []
        self.connections = self.init_dicts()
        self.coordinates_dict = self.init_station_list()
        self.traject_counter = number_of_trains
        self.add_trains(number_of_trains)
        self.traject_percentage = self.draw()

    def add_trains(self, number_of_trains):
            """
            Adding trains from the imported train class
            """
            stations = self.connections.copy()
            odd_connections_dic = {}
            outlying_stations = {}
            counter = 0

            #             
            for key, value in stations.items():
                if len(value) == 1:
                    outlying_stations[key] = value

                if len(value) % 2 == 1 and len(value) != 1:
                    odd_connections_dic[key] = value


            # Making trains for the given amount of total trains
            while outlying_stations or odd_connections_dic:
                counter += 1
                
                if outlying_stations:
                    current_station = random.sample(outlying_stations.keys(), 1)
                    train = Train(str(current_station[0]), self.connections)
                    self.trains_list.append(train)
                    outlying_stations.pop(current_station[0])
                
                elif odd_connections_dic:
                    current_station = random.sample(odd_connections_dic.keys(), 1)
                    train = Train(str(current_station[0]), self.connections)
                    self.trains_list.append(train)
                    odd_connections_dic.pop(current_station[0])
                    
                    if counter == number_of_trains:
                        return


    def init_dicts(self):
        dict_of_connections = {}

        # Loop over the dataframe to append all stations as dictionaries to list
        for i in range(len(self.connect['station1'])):
            if self.connect["station1"][i] in dict_of_connections.keys():
                dict_of_connections[self.connect["station1"][i]][self.connect["station2"][i]] = self.connect["distance"][i]
            else:
                dict_of_connections[self.connect["station1"][i]] = {self.connect["station2"][i] : self.connect["distance"][i]}
            if self.connect["station2"][i] in dict_of_connections.keys():
                dict_of_connections[self.connect["station2"][i]][self.connect["station1"][i]] = self.connect["distance"][i]
            else:
                dict_of_connections[self.connect["station2"][i]] = {self.connect["station1"][i] : self.connect["distance"][i]}

        return dict_of_connections

    def init_station_list(self):
        """
        Create a dictionary of the stations with their coordinates as values
        """

        self.coordinates_dict = {}

        # Loop over the coordinates and append to dictionary
        for i in range(len(self.stations['x'])):
            self.coordinates_dict[self.stations['station'][i]] = [self.stations['x'][i], self.stations['y'][i]]

        return self.coordinates_dict


    def step(self):
        """
        Calling for every train in the list of trains for its movement
        """
        for train in self.trains_list:
            train.movement()


    def draw(self):
        """
        Plot the stations and trajectories of trains between stations.
        """

        # Keep track of the stations a train has passed on its route
        for train in self.trains_list:
            self.train_route_list.append({train.current_station, train.destination[0]})

        amount_used = 0

        # Loop over the connection between stations and check wether a connection
        # is already in the list of train routes. If yes, color red, if no color blue.
        for i in range(len(self.connect['station1'])):

            # If yes, color red, if no color blue.
            if {self.connect['station1'][i], self.connect['station2'][i]} in self.train_route_list:
                amount_used += 1

        return amount_used / len(self.connect['station1'])

    def run(self, iterations):
        """
        To run the experiment and get its results
        """

        total = 0

        # Loop over the iterations to set each step and draw each movement
        for i in range(iterations):
            self.step()
            self.traject_percentage = self.draw()

        # Print the stations each train has been to
        for train in self.trains_list:
            total += train.total_min

        return 10000 * self.traject_percentage - (self.traject_counter * 100 + total)



scores = []
for i in range(100):
    my_experiment = Experiment(7,'ConnectiesHolland.csv', 'StationsHollandPositie.csv')
    scores.append(my_experiment.run(120))

# Plotting labelled histogram
plt.hist(scores)
plt.xlabel('Score')
plt.ylabel('Number of solutions')
plt.show()

