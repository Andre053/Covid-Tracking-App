# will visualize the data after analysis has been made

import PySimpleGUI as sg
import miner
import analyzer
# import keyboard # add pressing enter functionality

sg.theme('BlueMono')


def sign_in():  # Enter username window
    layout = [
        [sg.Text("Please enter your username")],
        [sg.Text("Username:", key="-ELEMENT-"),
         sg.InputText(key='-ENTER_USER-')],
        [sg.Button('Okay', enable_events=True, key="-FUNCTION-"),
         sg.Button('Clear', key="-CLEAR-"), sg.Button('Quit', key="-QUIT-")]
    ]

    window = sg.Window("Sign In", layout, size=(250, 100))

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-QUIT-'):  # quit gui
            break
        if event == '-CLEAR-':
            window['-ENTER_USER-']("")
        if event in ('-FUNCTION-'):
            window.close()
            return values['-ENTER_USER-']

    window.close()


def query_summary(data):
    # state name and values in list of tuples
    table = analyzer.build_table(data)

    columns = ("death", "recovered", "positive", "negative", "totalTestResults",
               "hospitalizedCumulative", "inIcuCumulative", "onVentilatorCumulative", "positiveCasesViral")

    layout = [
        [sg.Text("State Information")],
        [sg.Multiline(table, size=(30, 5), disabled=True)],
        [sg.Text("x Variable"), sg.Combo(values=columns,
                                         key="-X_SELECTION-", size=(30, 5), readonly=True)],
        [sg.Text("y Variable"), sg.Combo(values=columns,
                                         key="-Y_SELECTION-", size=(30, 5), readonly=True)],
        [sg.Button('Okay', enable_events=True, key="-FUNCTION-"),
         sg.Button('Delete', enable_events=True, key="-DELETE-"),
         sg.Button('Quit', key="-QUIT-")],
        [sg.Text(key='-GRAPH_TITLE-')],
        # [sg.Graph(background_color="white", canvas_size=(400, 400), graph_bottom_left=(
        #     400, 400), graph_top_right=(0, 0), key="-SCATTER-")],
        [sg.Multiline(size=(60, 3), disabled=True, key="-STATS-", visible=False)],
        [sg.Canvas(background_color="white", key="-SCATTER-")]
    ]

    window = sg.Window("Selection Summary", layout,
                       size=(500, 800), finalize=True)

    df_class = analyzer.DataFrame(data)
    graph = analyzer.Graph(window, df_class.build_dataframe())
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-QUIT-'):  # quit gui
            break
        if event == '-FUNCTION-':
            window['-GRAPH_TITLE-'].update("Scatter Plot")
            choices = (values['-X_SELECTION-'], values['-Y_SELECTION-'])
            graph.plot(choices)  # graph should clear axes on each click
            window['-STATS-'].update(df_class.summary_statistics(choices), visible=True)
        # if event == '-DELETE-':
        #     graph.clear_fig()

    window.close()


def gui():
    user = sign_in()

    states = ("Alabama: AL", "Alaska: AK", "Arizona: AZ", "Arkansas: AR",
              "Califormia: CA", "Colorado: CO", "Connetiut: CT", "Deleware: DE",
              "Florida: FL", "Georgia: GA", "Hawaii: HI", "Idaho: ID", "Illinois: IL",
              "Indiana: IN", "Iowa: IA", "Kansas: KS", "Kentucky: KY", "Louisiana: LA",
              "Maine: ME", "Maryland: MD", "Massachusettes: MA", "Michigan: MI",
              "Minnesota: MN", "Mississippi: MS", "Missouri: MO", "Montana: MT",
              "Nebraska: NE", "Nevada: NV", "New Hampshire: NH", "New Jersey: NJ",
              "New Mexico: NM", "New York: NY", "North Carolina: NC", "North Dakota: ND", "Ohio: OH",
              "Oklahoma: OK", "Oregon: OR", "Pennsylvania: PA", "Rhode Island: RI",
              "South Carolina: SC", "South Dakota: SD", "Tennessee: TN", "Texas: TX", "Utah: UT",
              "Vermont: VT", "Virginia: VA", "Washington: WA", "West Virginia: WV",
              "Wisconsin: WI", "Wyoming: WY")

    if user:  # if user is not None
        layout = [
            [sg.Text(f"Hello {user}, welcome to my project!")],
            [sg.Text("This application requests data from the Covid Tracking API ")],
            [sg.Text("Select the states you wish to get data from")],
            [sg.Listbox(values=states, select_mode='extended',
                        key="-STATE_SELECTION-", size=(30, 10))],
            [sg.Button('Okay', enable_events=True, key="-FUNCTION-"),
             sg.Button('Clear', key="-CLEAR-"), sg.Button('Quit', key="-QUIT-")]
        ]

        window = sg.Window(f"{user}'s Session", layout, size=(400, 250))

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, '-QUIT-'):  # quit gui
                break
            if event in ('-FUNCTION-'):
                # state name plus values
                info = miner.data(values['-STATE_SELECTION-'])
                # print(info)
                query_summary(info)
            elif event == "-CLEAR-":
                window['-STATE_SELECTION-'].set_value([])  # set to empty list

        window.close()
