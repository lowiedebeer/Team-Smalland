import pandas as pd
import matplotlib.pyplot as plt
import random

from train import Train
from class_station import Station

class Experiment():

    #initialize trains and stations
    def __init__(self, number_of_trains):
        self.trains_list = []
        self.stations_list = []
        self.ridden_history = []
        self.minutes_left = 120
        self.train_route_list = []
        self.connections = self.init_dicts()
        self.x_list, self.y_list, self.coordinates_dict = self.init_station_list()
        self.add_stations()
        self.add_trains(number_of_trains)
        self.setup_plot()
        self.draw()


    def add_stations(self, ):
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
        connections = pd.read_csv('ConnectiesHolland.csv')
        dict_of_connections = {}

        # Loop over the dataframe to append all stations as dictionaries to list
        for i in range(len(connections['station1'])):
            if connections["station1"][i] in dict_of_connections.keys():
                dict_of_connections[connections["station1"][i]][connections["station2"][i]] = connections["distance"][i]
            else:
                dict_of_connections[connections["station1"][i]] = {connections["station2"][i] : connections["distance"][i]}
            if connections["station2"][i] in dict_of_connections.keys():
                dict_of_connections[connections["station2"][i]][connections["station1"][i]] = connections["distance"][i]
            else:
                dict_of_connections[connections["station2"][i]] = {connections["station1"][i] : connections["distance"][i]}

        return dict_of_connections

    def init_station_list(self):
        """
        Create a dictionary of the stations with their coordinates as values
        """

        # Read the csv-file with the geographical locations of the stations
        self.station_map = pd.read_csv('StationsHollandPositie.csv')

        self.coordinates_dict = {}

        # Loop over the coordinates and append to dictionary
        for i in range(len(self.station_map['x'])):
            coordinates_dict[self.station_map['station'][i]] = [self.station_map['x'][i], self.station_map['y'][i]]
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

        # Read the csv-file of the connections between stations into
        # a dataframe for each csv-file.
        train_route_map = pd.read_csv('ConnectiesHolland.csv')

        # Making a list of x and y values of the positions of the stations
        # to later be able to plot the stations.
        x_list = list(self.station_map['x'])
        y_list = list(self.station_map['y'])

        # Keep track of the stations a train has passed on its route
        for train in self.trains_list:
            self.train_route_list.append({train.current_station, train.destination[0]})


        for i in range(len(traject_map['station1'])):
            x_values = [self.coordinates_dict[train_route_map['station1'][i]][0], self.coordinates_dict[train_route_map['station2'][i]][0]]
            y_values = [self.coordinates_dict[train_route_map['station1'][i]][1], self.coordinates_dict[train_route_map['station2'][i]][1]]

            if {train_route_map['station1'][i], train_route_map['station2'][i]} in self.train_route_list:
                self.ax.plot(x_values, y_values, 'ro', linestyle="-")
            else:
                self.ax.plot(x_values, y_values, 'bo', linestyle="--")

        plt.plot(x_list, y_list, 'go')
        plt.draw()
        plt.pause(0.01)
        self.ax.cla()

    def run(self, iterations):
        """
        To run the experiment and get its results
        """
        # Loop over the iterations to set each step and draw each movement
        for i in range(iterations):
            self.step()
            self.draw()

        # Print the stations each train has been to
        for train in self.trains_list:
            print(train.list_of_stations)

    def setup_plot(self):
        # Making a subplot for the updating figure
        self.fig, self.ax = plt.subplots(figsize=(4,5))


my_experiment = Experiment(7)
my_experiment.run(120)
