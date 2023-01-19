import pandas as pd

# Loading the dataframe of connections between stations
connections = pd.read_csv("ConnectiesHolland.csv")

# Class instance for the stations
class Station():
    def __init__(self, connections):
        self.connections = connections

    def next_station(self):
        '''
        This function takes a csv-file of the distance between stations as input,
        loops over this to output a list of dictionaries with next station and distance
        as a value in the form of a tuple.
        '''

        # Empty list for all next_station values
        list_of_connections = []

        # Loop over the dataframe to append all stations as dictionaries to list
        for i in range(len(self.connections['station1'])):
                    next_station1 = {}
                    next_station1[self.connections["station1"][i]] = (self.connections["station2"][i], self.connections["distance"][i])

                    next_station2 = {}
                    next_station2[self.connections["station2"][i]] = (self.connections["station1"][i], self.connections["distance"][i])

                    list_of_connections.append(next_station1)
                    list_of_connections.append(next_station2)

        return list_of_connections
