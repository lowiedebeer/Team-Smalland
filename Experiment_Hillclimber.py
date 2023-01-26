#Experiment Hillclimber
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
        self.add_trains(number_of_trains)
        self.setup_plot()
        self.traject_percentage = self.draw()
        self.traject_counter = number_of_trains

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

        # Making a list of x and y values of the positions of the stations
        # to later be able to plot the stations.
        x_list = list(self.stations['x'])
        y_list = list(self.stations['y'])

        # Keep track of the stations a train has passed on its route
        for train in self.trains_list:
            self.train_route_list.append({train.current_station, train.destination[0]})

        amount_used = 0

        # Loop over the connection between stations and check wether a connection
        # is already in the list of train routes. If yes, color red, if no color blue.
        for i in range(len(self.connect['station1'])):
            x_values = [self.coordinates_dict[self.connect['station1'][i]][0], self.coordinates_dict[self.connect['station2'][i]][0]]
            y_values = [self.coordinates_dict[self.connect['station1'][i]][1], self.coordinates_dict[self.connect['station2'][i]][1]]

            # If yes, color red, if no color blue.
            if {self.connect['station1'][i], self.connect['station2'][i]} in self.train_route_list:
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
            self.step()
            self.traject_percentage = self.draw()

        # Print the stations each train has been to
        for train in self.trains_list:
            total += train.total_min

        return 10000 * self.traject_percentage - (self.traject_counter * 100 + total)

    def hill_climber(self, max_iterations):
        # Initialize the current state of the simulation
        current_state = self.get_state()
        current_score = self.evaluate_objective_function(current_state)

        for i in range(max_iterations):
            # Make small changes to the current state
            new_state = self.perturb_state(current_state)

            # Evaluate the objective function for the new state
            new_score = self.evaluate_objective_function(new_state)

            # If the new state is better than the current state, move to the new state
            if new_score > current_score:
                current_state = new_state
                current_score = new_score
                print("New best state found with score:", current_score)
            else:
                # Otherwise, with some probability, move to the new state anyway
                prob = np.exp((new_score - current_score) / self.temperature)
                if np.random.rand() < prob:
                    current_state = new_state
                    current_score = new_score
                    print("New state found with score:", current_score)

        return current_state

    def get_state(self):
        """
        Returns the current state of the simulation, e.g. the positions and velocities of all trains
        """
        return self.train_route_list

    def perturb_state(self, state):
        """
        Makes small changes to the state of the simulation
        """

        

    def check_objective_function(self, state):
        """
        Returns the value of the objective function for the given state
        """

        return self.run()


    def setup_plot(self):
        # Making a subplot for the updating figure
        self.fig, self.ax = plt.subplots(figsize=(4,5))

scores = []
for i in range(3):
    my_experiment = Experiment(7,'ConnectiesHolland.csv', 'StationsHollandPositie.csv')
    scores.append(my_experiment.run(120))
    print(sum(scores) / len(scores))
    print(max(scores))
print(scores)

# plotting labelled histogram
plt.hist(scores)
plt.xlabel('Score')
plt.ylabel('Number of solutions')
plt.show()
