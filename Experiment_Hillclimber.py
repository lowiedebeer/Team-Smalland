#Experiment Hillclimber
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np

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
        self.list_of_stations = []
        self.remake_train = []
        self.connections = self.init_dicts()
        self.coordinates_dict = self.init_station_list()
        self.add_trains(number_of_trains)
        self.setup_plot()
        self.traject_counter = number_of_trains
    
    def add_trains(self, number_of_trains):
            """
            Adding trains from the imported train class
            """
            stations = self.connections.copy()
            odd_connections_dic = {}
            outlying_stations = {}
            counter = 0

            # Making a dictionary for the stations with one connection
            for key, value in stations.items():
                if len(value) == 1:
                    outlying_stations[key] = value

                # Making dictionaries of the odd stations
                if len(value) % 2 == 1 and len(value) != 1:
                    odd_connections_dic[key] = value


            # Using the made dictionaries to assign the stations
            while outlying_stations or odd_connections_dic:
                counter += 1

                # First use the stations with just one connection and make train objects starting here
                if outlying_stations:
                    current_station = random.sample(outlying_stations.keys(), 1)
                    train = Train(str(current_station[0]), self.connections)
                    self.trains_list.append(train)
                    outlying_stations.pop(current_station[0])
                    
                    # If the max trains are reached stop
                    if counter == number_of_trains:
                        return

                # If there are no stations with one connection left use the other dictionary
                elif odd_connections_dic:
                    current_station = random.sample(odd_connections_dic.keys(), 1)
                    train = Train(str(current_station[0]), self.connections)
                    self.trains_list.append(train)
                    odd_connections_dic.pop(current_station[0])

                    # If the max trains are reached stop
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
        train_list = []

        # Loop over all the trains and use there movement definition
        # Add all the trajects that they have ridden on to a list
        for train in self.trains_list:
            train.movement()
            train_list.append(train.list_of_stations)
        
        return train_list
    
    def step_remake(self, remake_train):
        train_list = []

        # Loop over all the trains and use there movement definition
        # Add all the trajects that they have ridden on to a list
        
        for train in remake_train:
            train.movement()
            train_list.append(train.list_of_stations)
    
        return train_list

    def draw(self):
        """
        Plot the stations and trajectories of trains between stations.
        """

        # Making a list of x and y values of the positions of the stations
        # to later be able to plot the stations.
        x_list = list(self.stations['x'])
        y_list = list(self.stations['y'])
        amount_used = 0
        total_list = []

        # Keep track of the stations a train has passed on its route
        for train_list in self.list_of_stations:
            for destination in train_list:
                total_list.append(destination)

        # Loop over the connection between stations and check wether a connection
        # is already in the list of train routes. If yes, color red, if no color blue.
        for i in range(len(self.connect['station1'])):
            x_values = [self.coordinates_dict[self.connect['station1'][i]][0], self.coordinates_dict[self.connect['station2'][i]][0]]
            y_values = [self.coordinates_dict[self.connect['station1'][i]][1], self.coordinates_dict[self.connect['station2'][i]][1]]
            
            if {self.connect['station1'][i], self.connect['station2'][i]} in total_list:
                # self.ax.plot(x_values, y_values, 'ro', linestyle="-")
                amount_used += 1
            # else:
            #     self.ax.plot(x_values, y_values, 'bo', linestyle="--")
        
        # plt.plot(x_list, y_list, 'go')
        # plt.draw()
        # plt.pause(0.01)
        # self.ax.cla()
        
        return amount_used / len(self.connect['station1'])

    def run(self, iterations, remake_train):
        """
        To run the experiment and get its results
        """

        total = 0
        if len(remake_train) > 0:
            for i in range(iterations):
                stations = self.step_remake(remake_train)

        else:
            # Loop over the iterations to set each step and draw each movement
            for i in range(iterations):
                stations = self.step()
        
        self.switch_trajects()
        
        # Add all the stations to a self object
        for station_train in stations:
            self.list_of_stations.append(station_train)

        # Calculate the traject_percentage
        self.traject_percentage = self.draw()

        # Print the stations each train has been to
        for train in self.trains_list:
            total += train.total_min

        
        # Making the total a self object

        # print(self.traject_percentage, self.traject_counter, total, len(self.list_of_stations))
        return 10000 * self.traject_percentage - (self.traject_counter * 100 + total)

    def switch_trajects(self):
        """
        When the experiment is over see if a double traject can be swapped to an unused traject
        """
        all_trajects = [train.list_of_stations for train in self.trains_list]
        for i, current_traject in enumerate(all_trajects):
            other_trajects = all_trajects[:i] + all_trajects[i+1:]
            for station in current_traject:
                if station in [traject for sublist in other_trajects for traject in sublist]:
                    self.trains_list[i].already_taken += 1


    def hill_climber(self, max_iterations, minutes):
        # Initialize the current state of the simulation
        current_state = self.get_state()
        current_score = self.check_objective_function(current_state, minutes)

        for i in range(max_iterations):
            # Make small changes to the current state
            new_state = self.change_route(current_state)

            # Evaluate the objective function for the new state
            new_score = self.check_objective_function(new_state, minutes)

            # If the new state is better than the current state, move to the new state
            if new_score > current_score:
                current_state = new_state
                current_score = new_score
                print("New best state found with score:", current_score)
            if self.traject_percentage == 1:
                self.write_timetable()
                return current_score
            # else:
            #     # Otherwise, with some probability, move to the new state anyway
            #     prob = np.exp((new_score - current_score) / self.temperature)
            #     if np.random.rand() < prob:
            #         current_state = new_state
            #         current_score = new_score
            #         print("New state found with score:", current_score)

        return current_state

    def write_timetable(self):
        train_number = 1
        for train in self.trains_list:
            print(f"Route of train {train_number}:")
            print(train.list_of_stations)
            train_number += 1

    def get_state(self):
        """
        Returns the current state of the simulation, e.g. the positions and velocities of all trains
        """
        return self.train_route_list

    def change_route(self, state):
        """
        Makes small changes to the state of the simulation
        """
        # Choose a random train and delete its stations from the list
        train_count = 0
        removable_train = -1
        for train in range(len(self.trains_list)):
            if self.trains_list[train].already_taken > train_count:
                train_count = self.trains_list[train].already_taken
                removable_train =  train
            self.trains_list[train].already_taken = 0
        
        if removable_train != -1:
            del self.list_of_stations[removable_train]
            # Remove the minutes its used from the total minutes and empty its traject list
            self.trains_list[removable_train].list_of_stations = []
            # Reset its counters
            self.trains_list[removable_train].total_min = 0
            self.trains_list[removable_train].location = 0
            self.trains_list[removable_train].already_taken = 0

            # Change the trains that are being moved to the single train that is removed
            self.remake_train = [self.trains_list[removable_train]]
        else:
            return print("Not Possible")

        

    def check_objective_function(self, state, minutes):
        """
        Returns the value of the objective function for the given state
        """

        return self.run(minutes, self.remake_train)


    def setup_plot(self):
        # Making a subplot for the updating figure
        self.fig, self.ax = plt.subplots(figsize=(4,5))

scores = []
for i in range(1):
    my_experiment = Experiment(20,'ConnectiesNationaal.csv', 'StationsNationaal.csv')
    scores.append(my_experiment.hill_climber(100000, 180))

print(scores)
# plotting labelled histogram
plt.hist(scores)
plt.xlabel('Score')
plt.ylabel('Number of solutions')
plt.show()
