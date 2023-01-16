import pandas as pd
import matplotlib.pyplot as plt
import random

from train import Train
from class_station import Station


class Experiment():

    #initialize trains and stations
    def __init__(self, number_of_trains):
        self.ridden_history = []
        self.minutes_left = 120

        self.connections = self.init_dicts()
        self.x_list, self.y_list, self.coordinates_dict = self.init_station_list()
        self.add_trains(number_of_trains)
        self.add_stations(len(self.coordinates_dict.keys()))
        self.draw()

    #adds trains objects
    def add_trains(self, number_of_trains):
        trains_list = []
        stations = []

        for i in range(number_of_trains):
            current_station = random.sample(self.coordinates_dict.keys(), 1)
            while current_station in stations:
                current_station = random.sample(self.coordinates_dict.keys(), 1)

            train = Train(str(current_station[0]), self.connections)
            trains_list.append(train)
        self.trains_list = trains_list

    #adds station objects
    def add_stations(self):
        stations_list = []
        for i in range(len(coordinates_dict.keys())):
            stations = Station(next_stations, coordinates_dict.keys()[i])
            stations_list.append(stations)
        self.stations_list = stations_list


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
        station_map = pd.read_csv('StationsHollandPositie.csv')

        x_list = list(station_map['x'])
        y_list = list(station_map['y'])
        coordinates_dict = {}

        for i in range(len(station_map['x'])):
            coordinates_dict[station_map['station'][i]] = [station_map['x'][i], station_map['y'][i]]
        return x_list, y_list, coordinates_dict

    def step(self):
        for train in self.trains_list:
            if train.traject_length < smallest_traject:
                smallest_traject = train.traject_length
        for train in self.trains_list:
            train.traject_length -= smallest_distance
            if train.traject_length == 0:
                train.movement()
        self.minutes_left -= smallest_traject

    def draw(self):
        station_map = pd.read_csv('StationsHollandPositie.csv')

        x_list = list(station_map['x'])
        y_list = list(station_map['y'])
        coordinates_dict = {}

        for i in range(len(station_map['x'])):
            coordinates_dict[station_map['station'][i]] = [station_map['x'][i], station_map['y'][i]]

        for i in range(len(traject_map['station1'])):
            x_values = [coordinates_dict[traject_map['station1'][i]][0], coordinates_dict[traject_map['station2'][i]][0]]
            y_values = [coordinates_dict[traject_map['station1'][i]][1], coordinates_dict[traject_map['station2'][i]][1]]
            plt.plot(x_values, y_values, 'yo', linestyle="--")

        plt.plot(x_list, y_list, 'go')
        plt.show()

Experiment(7)
