#Experiment_Hillcimber_2.0
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
        self.total = 0
        self.connections = self.init_dicts()
        self.coordinates_dict = self.init_station_list()
        self.add_trains(number_of_trains)
        self.setup_plot()
        self.traject_counter = number_of_trains
        self.temperature = 100

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
                self.ax.plot(x_values, y_values, 'ro', linestyle="-")
                amount_used += 1
            else:
                self.ax.plot(x_values, y_values, 'bo', linestyle="--")

        plt.plot(x_list, y_list, 'go')
        plt.draw()
        plt.pause(0.01)
        self.ax.cla()
        return amount_used / len(self.connect['station1'])

    def run(self, iterations):
        """
        To run the experiment and get its results
        """

        total = 0

        # Loop over the iterations to set each step and draw each movement
        for i in range(iterations):
            stations = self.step()

        # Add all the stations to a self object
        for station_train in stations:
            self.list_of_stations.append(station_train)

        # Calculate the traject_percentage
        self.traject_percentage = self.draw()

        # Print the stations each train has been to
        for train in self.trains_list:
            total += train.total_min

        # Making the total a self object
        self.total += total

        return 10000 * self.traject_percentage - (self.traject_counter * 100 + self.total)


    def hill_climber(self, max_iterations):
        # Initialize the current state of the simulation
        current_state = self.get_state()
        current_score = self.check_objective_function(current_state)

        current_states = []
        current_scores = []

        for i in range(max_iterations):
            # Make small changes to the current state
            new_state = self.change_route(current_state)
            current_states.append(new_state)

            # Evaluate the objective function for the new state
            new_score = self.check_objective_function(new_state)
            current_scores.append(new_score)

            # If the new state is better than the current state, move to the new state
            if new_score > current_score:
                current_state = new_state
                current_score = new_score
                print("New best state found with score:", current_score)
            # else:
            #     # Otherwise, with some probability, move to the new state anyway
            #     prob = np.exp((new_score - current_score) / self.temperature)
            #     if np.random.rand() < prob:
            #         current_state = new_state
            #         current_score = new_score
            #         print("New state found with score:", current_score)

        return current_state

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
        train = random.randrange(len(self.trains_list))
        del self.list_of_stations[train]

        # for station in train:
        #     del station[-1]
        #     del station[-2]
        #     del station[-3]
        #     del station[-4]

        # Remove the minutes its used from the total minutes and empty its traject list
        self.total -= self.trains_list[train].total_min
        self.trains_list[train].list_of_stations = []

        # Reset its counters
        self.trains_list[train].total_min = 0
        self.trains_list[train].location = 0

        # Change the trains that are being moved to the single train that is removed
        self.trains_list = [self.trains_list[train]]



    def check_objective_function(self, state):
        """
        Returns the value of the objective function for the given state
        """

        return self.run(120)


    def setup_plot(self):
        # Making a subplot for the updating figure
        self.fig, self.ax = plt.subplots(figsize=(4,5))

        # Plotting the change in scores
        plt.plot(current_states, current_scores, 'bl')
        plt.draw()
        plt.show()

scores = []
for i in range(1):
    my_experiment = Experiment(7,'ConnectiesHolland.csv', 'StationsHollandPositie.csv')
    scores.append(my_experiment.hill_climber(120))
    print(sum(scores) / len(scores))
    print(max(scores))
print(scores)

# plotting labelled histogram
plt.hist(scores)
plt.xlabel('Score')
plt.ylabel('Number of solutions')
plt.show()
