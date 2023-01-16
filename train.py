class Train():

    # Defining train_location, traject_length and destination
    def __init__(self, current_station, traject_length):
        self.train = current_station
        self.traject_length = traject_length # In minuten
        self.list_of_stations = [current_station]
        self.location=0

    def movement(self):
        """
        The movement of a single train is defined by its speed if the destination
        is reached the station will be added to a list of stations on its traject.
        """
        self.location += 1
       
       # If the distance between the train and the station is 0 add it to the list of stations
        if self.traject_length[1] - self.location == 0:
            self.train = self.traject_length[0]
            self.list_of_stations.append(self.train)
       
        return self.list_of_stations


