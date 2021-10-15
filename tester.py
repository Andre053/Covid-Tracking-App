# Learning matplotLib


from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg


class Graph():
    def __init__(self, window, axes=None, fig=None, fig_canvas=None):
        self.window = window  # the widget the graph will be printed on
        self.axes = axes  # the plot for each instantiation
        self.fig = fig  # the figure container
        self.fig_canvas = fig_canvas

    def clear_fig(self):
        self.fig_canvas.get_tk_widget().destroy()
        # try:
        #     self.fig_canvas.get_tk_widget.destroy()
        #     print("cleared!")
        # except:
        #     pass

        # self.axes.cla()
        # self.fig.clf()


    # def draw_figure(self, fig, canvas):  # figure out this logic
    #     self.fig_canvas = FigureCanvasTkAgg(fig, canvas)
    #     self.fig_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def plot(self):  # data in tuples (country, death, totalResults)

        # self.window['-SCATTER-'].TKCanvas.delete("all")
        # self.window.read()
        x_values = [1, 2, 3, 4]
        y_values = [1, 2, 3, 4]
        
        if self.axes is not None:
            self.clear_fig()

        self.fig = Figure()

        #states = df['States'].values
        # sets up figure axes with x and y choices as labels
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlabel("x axis")
        self.axes.set_ylabel("y axis")
        self.axes.grid()

        graph_elem = self.window['-SCATTER-']  # gui canvas for the graph
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=graph_elem.TKCanvas)
        self.fig_canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


        # plugging in scatter data, will reference returned tuple from variables()
        self.axes.scatter(x=x_values, y=y_values)
        #self.fig_canvas.draw()


def main():  # Enter username window
    layout = [
        [sg.Text("Tester")],
        [sg.Text("Scatter")],

        [sg.Button('Okay', enable_events=True, key="-FUNCTION-"),
         sg.Button('Clear', key="-CLEAR-"), sg.Button('Quit', key="-QUIT-")],
        [sg.Canvas(key="-SCATTER-", background_color="red")]
    ]

    window = sg.Window("Testing", layout, size=(800, 800))

    graph = Graph(window)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-QUIT-'):  # quit gui
            break
        if event == '-CLEAR-':
            # canvas = window['-SCATTER-'].TKCanvas
            # canvas.delete("all")
            window.read()
            window.refresh()
        if event in ('-FUNCTION-'):
            graph.plot()

    window.close()


main()
