import pandas as pd
import matplotlib.pyplot as plt

station_map = pd.read_csv('StationsHollandPositie.csv')
traject_map = pd.read_csv('ConnectiesHolland.csv')

x_list = list(station_map['x'])
y_list = list(station_map['y'])
coordinates_dict = {}

for i in range(len(station_map['x'])):
    coordinates_dict[station_map['station'][i]] = [station_map['x'][i], station_map['y'][i]]

print(coordinates_dict)

for i in range(len(traject_map['station1'])):
    x_values = [coordinates_dict[traject_map['station1'][i]][0], coordinates_dict[traject_map['station2'][i]][0]]
    y_values = [coordinates_dict[traject_map['station1'][i]][1], coordinates_dict[traject_map['station2'][i]][1]]
    plt.plot(x_values, y_values, 'yo', linestyle="--")

plt.plot(x_list, y_list, 'go')
plt.show()
