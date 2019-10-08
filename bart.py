import os
import requests
from time import sleep

def get_etd(origin):
    """Submit API query for Estimated Departure Time (EDT)"""

    # define the parameters for the query
    params = {
        "key": os.getenv("bart_key"),
        "cmd": "etd",
        "orig": origin,
        "dir": "n",
        "json": "y"
    }

    # define the base url for the API
    base_url = "http://api.bart.gov/api/"

    # submit the query
    r = requests.get(base_url + "/etd.aspx", params=params)

    if r.status_code != 200:
        print("There was an issue. Error code {}".format(r.status_code))
    else:
        return r.json()


def parse_etd(data, destination):
    """Parse the API query response for the Estimated Departure Time (EDT) query"""

    # parse the response and return the time for the given train
    for dest in data['root']['station'][0]['etd']:
        if dest['abbreviation'] == destination:
            status = "The next train is in {} minutes".format(dest['estimate'][0]['minutes'])
            break
        else:
            status = "This train is not going to {}".format(destination)

    return status

if __name__ == '__main__':
    while True:
        data = get_etd("civc")
        edt = parse_etd(data, "DUBL")
        print(edt)
        sleep(60)
