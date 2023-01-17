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
        self.traject_list = []
        self.connections = self.init_dicts()
        self.x_list, self.y_list, self.coordinates_dict = self.init_station_list()
        self.add_stations(self.connections)
        self.add_trains(number_of_trains)
        self.draw(self.trains_list)
        # while self.minutes_left > 0:
        #     self.step()
        #     self.draw(self.trains_list)

    #adds station objects
    def add_stations(self, connections):
        stations_list = []
        for i in range(len(self.coordinates_dict.keys())):
            stations = Station(list(self.coordinates_dict.keys())[i])
            stations_list.append(stations)
        self.stations_list = stations_list

    #adds trains objects
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


    def init_dicts(self):
        connections = pd.read_csv('ConnectiesHolland.csv')
        self.connections = connections
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
        self.station_map = station_map

        x_list = list(station_map['x'])
        y_list = list(station_map['y'])
        coordinates_dict = {}

        for i in range(len(station_map['x'])):
            coordinates_dict[station_map['station'][i]] = [station_map['x'][i], station_map['y'][i]]
        return x_list, y_list, coordinates_dict

    def traject_list(self, trains_list):
        
        for train in trains_list:
            self.traject_list.append([train.current_station, train.destination])
        return self.traject_list

    def step(self):
        smallest_traject = 50
        for train in self.trains_list:
            train.movement()

        #     print(train.traject_length)
        #     print(train.current_station)
        #     print(train.destination[0])
        #     if train.traject_length < smallest_traject:
        #         smallest_traject = train.traject_length
        # for train in self.trains_list:
        #     train.traject_length -= smallest_traject
        #     if train.traject_length == 0:
        #         train.movement()
        # self.minutes_left -= smallest_traject

    def draw(self, trains_list):
        self.trains_list = trains_list
        traject_map = pd.read_csv('ConnectiesHolland.csv')
        station_map = pd.read_csv('StationsHollandPositie.csv')

        x_list = list(station_map['x'])
        y_list = list(station_map['y'])

        traject_list = self.trains_list
        print(self.trains_list)
        coordinates_dict = {}

        for i in range(len(self.station_map['x'])):
            coordinates_dict[station_map['station'][i]] = [station_map['x'][i], station_map['y'][i]]

        for i in range(len(traject_map['station1'])):
            x_values = [coordinates_dict[traject_map['station1'][i]][0], coordinates_dict[traject_map['station2'][i]][0]]
            y_values = [coordinates_dict[traject_map['station1'][i]][1], coordinates_dict[traject_map['station2'][i]][1]]
            if [traject_map['station1'][i], traject_map['station2'][i]] in traject_list:
                plt.plot(x_values, y_values, 'ro', linestyle="-")
            elif [traject_map['station2'][i], traject_map['station1'][i]] in traject_list:
                plt.plot(x_values, y_values, 'ro', linestyle="-")
            else:
                plt.plot(x_values, y_values, 'bo', linestyle="--")

        plt.plot(x_list, y_list, 'go')
        plt.show()

    def run(self, iterations):
        for i in range(iterations):
            self.step()

        for train in self.trains_list:
            print(train.list_of_stations)



my_experiment = Experiment(7)
my_experiment.run(120)