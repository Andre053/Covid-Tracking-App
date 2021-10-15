# will scrape the data and clean it for analysis

# API: https://api.covidtracking.com
### JSON: /v1/status.json ###
# Historial values: /v1/states/{state}/daily.json
### CSV: /v1/status.csv ###
# Historical values: /v1/states/{state}/daily.csv

import requests as req

### get request methods ###
# request by itself returns http code
# .content returns byte representation
# .text returns string representation of data payload
# .json returns json representation of data payload


def state_data(state):
    query = f"https://api.covidtracking.com/v1/states/{state}/daily.json"
    request = req.get(query)
    if request.status_code == 200:  # good request
        return good_req(request)
    else:  # if there is a bad request
        return request.status_code


def good_req(request):
    json = request.json()
    return gather_data(json)


def data(state_list):
    to_analyze = []
    for state in state_list:
        # requests state data from api and returns as dictionary
        values = state_data(state[-2:].lower())

        to_analyze.append((state[:-4], values)) # state name plus all values
    return to_analyze


def gather_data(data):

    ### Define important data points to specify ###

    # death: Confirmed and probable fatalities due to Covid
    # recovered: Number of individuals identified as revocered from Covid
    # positive: Cases confirmed plus probable (if state is reporting probable cases)
    # negative: Negative PCR tests (unique people)
    # positiveCasesViral: Confirmed unique cases using PCR or other approved NAAT test
    # totalTestResults: At best an estimate of US viral (PCR) testing, variation of test reporting methods has large effects
    # hospitalizedCumulative: Number of individuals ever hospitalized with Covid
    # inIcuCumulative: Number of individuals ever hospitalized in the ICU with Covid
    # onVentilatorCumulative: Number of individuals ever hospitalized under advanced ventilation

    ### Types of statistical analysis ###
    # Allow choice of x and y values in window and create graph for each

    # deaths vs. total test results
    # deaths vs. total hospitalized
    # deaths vs. ICU
    # deaths vs. positive
    # deaths vs. ventilator
    # ICU vs. total hospitalized
    # positive vs. total test results

    important = {"death", "recovered", "positive", "negative", "totalTestResults",
                 "hospitalizedCumulative", "inIcuCumulative", "onVentilatorCumulative", "positiveCasesViral"}

    keys = {}  # append unique keys to dictionary
    for item in data:
        for key in item.keys():
            if key in important:  # important categories
                if key in keys:  # if in dictionary already
                    if item[key] == None:
                        pass
                    else:
                        keys[key] += item[key]
                else:
                    if item[key] == None:
                        keys[key] = 0
                    else:
                        keys[key] = item[key]
    return keys


def summary_stats(dict):

    print(
        f'Total positive viral cases is {dict["positiveCasesViral"]}\nTotal recovered cases is {dict["recovered"]}\nTotal deaths are {dict["death"]}\nTotal test results are {dict["totalTestResults"]}\n')

    pos_cases = dict["positiveCasesViral"] / dict["totalTestResults"]
    reg_cases = dict["recovered"] / dict["positiveCasesViral"]
    death_v_cases = dict["death"] / dict["positiveCasesViral"]

    return print(f"Percentage of positive cases is {pos_cases*100}\nPercentage of recovered cases are {reg_cases*100}\nPercentage of deaths are {death_v_cases*100}\n")
