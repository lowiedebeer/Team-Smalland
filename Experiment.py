import pandas as pd
import matplotlib.pyplot as plt
import random

from train import Train
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
        self.stations_list = []
        self.ridden_history = []
        self.minutes_left = 120
        self.train_route_list = []
        self.total = 0
        self.connections = self.init_dicts()
        self.coordinates_dict = self.init_station_list()
        self.add_stations()
        self.add_trains(number_of_trains)
        self.setup_plot()
        self.traject_percentage, self.traject_counter = self.draw()


    def add_stations(self):
        """
        Adding stations
        """

        # Looping over the length of the given dict of the stations
        for i in range(len(self.coordinates_dict.keys())):
            stations = Station(list(self.coordinates_dict.keys())[i])
            self.stations_list.append(stations)

    def add_trains(self, number_of_trains):
        """
        Adding trains from the imported train class
        """

        # Making trains for the given amount of total trains
        for i in range(number_of_trains):
            current_station = random.sample(self.coordinates_dict.keys(), 1)
            train = Train(str(current_station[0]), self.connections)
            self.trains_list.append(train)


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

        # Making a list of x and y values of the positions of the stations
        # to later be able to plot the stations.
        x_list = list(self.stations['x'])
        y_list = list(self.stations['y'])

        # Keep track of the stations a train has passed on its route
        for train in self.trains_list:
            self.train_route_list.append({train.current_station, train.destination[0]})

        fraction_used = 0

        # Loop over the connection between stations and check wether a connection
        # is already in the list of train routes. If yes, color red, if no color blue.
        for i in range(len(self.connect['station1'])):
            x_values = [self.coordinates_dict[self.connect['station1'][i]][0], self.coordinates_dict[self.connect['station2'][i]][0]]
            y_values = [self.coordinates_dict[self.connect['station1'][i]][1], self.coordinates_dict[self.connect['station2'][i]][1]]

            # If yes, color red, if no color blue.
            if {self.connect['station1'][i], self.connect['station2'][i]} in self.train_route_list:
                self.ax.plot(x_values, y_values, 'ro', linestyle="-")
                fraction_used += 1
            else:
                self.ax.plot(x_values, y_values, 'bo', linestyle="--")

        plt.plot(x_list, y_list, 'go')
        plt.draw()
        plt.pause(0.01)
        self.ax.cla()
        return len(self.connect['station1']) / fraction_used, len(self.train_route_list)

    def run(self, iterations):
        """
        To run the experiment and get its results
        """
        station = set()
        # Loop over the iterations to set each step and draw each movement
        count = 0
        for i in range(iterations):
            self.step()
            self.traject_percentage, self.traject_counter = self.draw()
            count += 1
            # print(count)

        # Print the stations each train has been to
        for train in self.trains_list:
            station.update(set(train.list_of_stations))
            self.total += train.total_min

        return 10000 * self.traject_percentage - (self.traject_counter * 100 + self.total)


    def setup_plot(self):
        # Making a subplot for the updating figure
        self.fig, self.ax = plt.subplots(figsize=(4,5))

scores = []
for i in  range(3):
    my_experiment = Experiment(22,'ConnectiesNationaal.csv', 'StationsNationaal.csv')
    scores.append(my_experiment.run(180))
print(scores)
