# will analyze the mined data using statistics
import pandas as pd
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def build_table(data):  # for gui
    return "\n".join([x[0] for x in data])

class DataFrame:
    def __init__(self, data, df=None):
        self.data = data
        self.df = df
    def build_dataframe(self):
        data_list = [x[1] for x in self.data]
        self.df = pd.DataFrame(data_list, columns=[
            "death", "recovered", "positive",
            "negative", "totalTestResults", "hospitalizedCumulative",
            "inIcuCumulative", "onVentilatorCumulative", "positiveCasesViral"])
        return self.df

    def summary_statistics(self, chosen):
        # x_values = self.df[choices[0]].values # choice 1 from gui
        # y_values = self.df[choices[1]].values # choice 2 from gui
        # chosen_data = [x_values, y_values]
        # print(chosen_data)
        states = [x[0] for x in self.data]
        self.df['states'] = states
        df_states = self.df.set_index('states')
        # print(self.df)
        data_choices = df_states[[chosen[0], chosen[1]]].to_string(col_space=(30,30), justify="center")
        #print(data_choices)
        return data_choices


class Graph:
    def __init__(self, window, df, axes=None, fig=None, fig_canvas=None):
        self.window = window # the widget the graph will be printed on
        self.df = df # data frame
        self.axes = axes # the plot for each instantiation
        self.fig = fig # the figure container
        self.fig_canvas = fig_canvas

    def clear_fig(self):
        self.fig_canvas.get_tk_widget().destroy()

        # self.axes.cla()
        # self.fig.clf()

    def draw_figure(self):  # figure out this logic
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self.window['-SCATTER-'].TKCanvas)
        self.fig_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def plot(self, choices):  # data in tuples (country, death, totalResults)

        if self.axes is not None:
            self.clear_fig()
        
        self.fig = Figure()
        x_values = self.df[choices[0]].values # choice 1 from gui
        y_values = self.df[choices[1]].values # choice 2 from gui

        #states = df['States'].values
        # sets up figure axes with x and y choices as labels
        self.set_up_figure(self.fig, choices[0], choices[1]) 

        # figure out this function
        self.draw_figure()

        # plugging in scatter data, will reference returned tuple from variables()
        self.axes.scatter(x=x_values, y=y_values)

    def set_up_figure(self, fig, x, y):  # string names for x and y
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel(x)
        self.axes.set_ylabel(y)
        self.axes.grid()

    

    
