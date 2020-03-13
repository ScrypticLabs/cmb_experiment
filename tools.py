import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

class Data:
    def __init__(self, filename=None):
        self.df = None
        self.angle = None
        self.power_units = None
        self.comments = None
        self.duration = None
        self.filename = "N/A"
        if filename:
            self.filename = filename.split("/")[-1]
            self.parse_data(filename)

    
    def parse_data(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            # the first 8 lines are metadata
            metadata, data = lines[:8], lines[8:]
            duration = float(metadata[1].split(" ")[-1])
            angle = metadata[3].split(" ")[-1].strip()
            try:
                angle = float(angle)
            except:
                angle = "N/A"
            power_units = metadata[6].split(" ")[-1]
            comments = metadata[7].split(":")[-1].strip()
            json = {
                "time" : [],
                "power" : [],
                "temperature" : []
            }
            for line in data:
                if len(line.split(" ")) < 3: 
                    print('skip')
                    continue
                time, power, temp = line.split(" ")
                json["time"].append(float(time))
                json["power"].append(float(power) * (10.0 if "ambient" in self.filename else 1.0))
                json["temperature"].append(float(temp))
        for datatype in json.keys():
            json[datatype] = np.array(json[datatype])
        self.df = pd.DataFrame.from_dict(json)
        self.angle = angle
        self.power_units = power_units
        self.comments = comments
        self.duration = duration
    
    def split_data(self, data, n=2):
        timesteps = data.count().time
        split = timesteps//n
        datasets = []
        for i in range(n):
            data = Data()
            data.df = data[i*split : (i+1)*split]
            data.angle = self.angle
            data.power_units = self.power_units
            data.comments = self.comments
            data.duration = self.duration
            datasets.append(data)
        return datasets

    def __str__(self):
        return self.filename
    
    def __repr__(self):
        return self.filename

def compute_regression_params(X, Y):
    x = np.array(X).reshape((len(X),1))
    y = np.array(Y).reshape((len(Y),1))
    model = LinearRegression()
    model.fit(x, y)
    r_sq = model.score(x, y)
    return model.coef_[0, 0], model.intercept_[0], r_sq

def plot_calibration(paired_datasets):
    temperatures = []
    powers = []
    colors = {
        0 : 'r', 
        1 : 'g', 
        2 : 'b',
        3 : 'c',
        4 : 'm',
        5 : 'y'
    }
    for pair in paired_datasets:
        ambient_Data, cold_Data = pair
        df_ambient, df_cold = ambient_Data.df, cold_Data.df
        avg_ambient_tmp, avg_ambient_power = df_ambient.temperature.mean(), df_ambient.power.mean()
        avg_cold_tmp, avg_cold_power = df_cold.temperature.mean(), df_cold.power.mean()
        temperatures.append([avg_ambient_tmp, avg_cold_tmp])        
        powers.append([avg_ambient_power, avg_cold_power])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(temperatures)):
        ax.plot(temperatures[i], powers[i], c=colors[i], label=str(i))
    plt.legend(loc='upper left');
    plt.show()

def plot_single_calibration(pair):
    temperatures = []
    powers = []
    colors = {
        0 : 'r', 
        1 : 'g', 
        2 : 'b',
        3 : 'c',
        4 : 'm',
        5 : 'y'
    }
    
    ambient_Data, cold_Data = pair
    df_ambient, df_cold = ambient_Data.df, cold_Data.df
    avg_ambient_tmp, avg_ambient_power = df_ambient.temperature.mean(), df_ambient.power.mean()
    avg_cold_tmp, avg_cold_power = df_cold.temperature.mean(), df_cold.power.mean()
    temperatures = [avg_ambient_tmp, avg_cold_tmp]       
    powers = [avg_ambient_power, avg_cold_power]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(temperatures, powers, c=colors[0], label=str(0))
    plt.legend(loc='upper left');
    plt.show()

    m, b, r_sq = compute_regression_params(temperatures, powers)
    x1 = min(temperatures)
    y1 = m*x1 + b
    x2 = max(temperatures)
    y2 = m*x2 + b

    ax = fig.add_subplot(111)
    ax.plot([x1, x2], [y1, y2], '--')

    plt.legend(loc='upper left');
    plt.show()

    return m, b, r_sq


def plot_data(x, y, x_axis, y_axis, title):
    n = len(x)
    xi = sum(x)
    yi = sum(y)
    xi_2 = sum([i**2 for i in x])
    yi_2 = sum([i**2 for i in y])
    xiyi = sum([x[i]*y[i] for i in range(n)])

    m = (n*xiyi - xi*yi) / (n*xi_2 - xi**2)
    b = (xi_2*yi - xi*xiyi) / (n*xi_2 - xi**2)

    # S = ((sum([(y[i] - m*x[i] - b)**2 for i in range(n)]))/(n-2))**0.5

    dm = (n/(n*xi_2 - xi**2))**0.5
    db = (xi_2/(n*xi_2 - xi**2))**0.5

    # ideal_x = 0.5232125957097838
    # factor = (1/n + n*(ideal_x - xi/n)**2/(n*xi_2-xi**2))**0.5

    print(m, " +- ", dm)
    print(b, " +- ", db)
    # print(1.28*S*factor, 1.65*S*factor, 1.97*S*factor)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(title+" m: %.5f +- %.5f, b: %.5f +- %.5f" % (m, dm, b, db))
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)

    ax.scatter(x, y, c='b')
    
    # m, b, r_sq = compute_regression_params(x, y)
    x1 = min(x)
    y1 = m*x1 + b
    x2 = max(x)
    y2 = m*x2 + b

    ax = fig.add_subplot(111)
    ax.plot([x1, x2], [y1, y2], '--')
    plt.legend(loc='upper left')
    plt.show()

    return m, dm, b, db


def plot_angle(datasets, transform=False):
    angles = []
    powers = []
    for data in datasets:
        angle, df = data.angle, data.df
        if type(angle) is not float: continue
        avg_power = df.power.mean()
        if avg_power < 0.51: continue
        angles.append(angle if not transform else 1.0/np.sin(angle*np.pi/180))
        powers.append(avg_power)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(angles, powers, c='b')

    m, b, r_sq = compute_regression_params(angles, powers)
    x1 = min(angles)
    y1 = m*x1 + b
    x2 = max(angles)
    y2 = m*x2 + b

    ax = fig.add_subplot(111)
    ax.plot([x1, x2], [y1, y2], '--')
    plt.legend(loc='upper left');
    plt.show()

    return m, b, r_sq