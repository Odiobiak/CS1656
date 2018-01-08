# -*- coding: utf-8 -*-
import sys
import requests as req
import json
import os

API_KEY = "44gXRTFLTAakikZ6kSR2Hn4ye"
FORMAT = 'json'

# Download all of the available bus routes in the RealTime API
def get_routes():
    # Send the GET request
    parameters = {'format': FORMAT, 'key': API_KEY}
    data_request = req.get("http://realtime.portauthority.org/bustime/api/v3/getroutes", params = parameters) # Returns a JSON
    if data_request.status_code == 200:
        data = data_request.json() # Grab the JSON
    else: # Error with the API
        print("Error in request to API! Returning...")
        return

    routes = []
    # Parse the JSON accordingly
    if data["bustime-response"]:
        for route in data["bustime-response"].get("routes"): # Parse each route information
            rt = route.get("rt") # Alphanumeric designator of aroute (ex. “20” or “X20”)
            rtnm = route.get("rtnm") # Common name of the route(ex. “Madison” for the 20 route).
            print(rt + ", " + rtnm)
            this_route = {'rt': rt, 'rtnm': rtnm} # Wrap the data of this specific route in a dictionary
            routes.append(this_route)
    else:
        print("Error in request to API! Returning...")
        return

    with open("allroutes.json", "w") as bus_file: # Save json to file
        json.dump(routes, bus_file)

# For all of the routes in allroutes.json, download all the directions for each route for busses that start with '6'
def get_directions():
    routes = []

    if not os.path.exists("allroutes.json"):
        print("ERROR: file allroutes.json does not exist")
        return

    with open("allroutes.json", "r") as bus_file:
        routes = json.load(bus_file)

    busses = [bus for bus in routes if bus["rt"][0] == "6"] # Find all busses in the routes list with an ID that starts with 6

    directions = []
    for bus in busses:
        bus_id = bus["rt"] # e.g. '61D', '61C', '69'
        bus_name = bus["rtnm"] # e.g. 'Madison' for the 20 route, 'Fifth Ave' for 61D
        parameters = {'format': FORMAT, 'key': API_KEY, 'rt': bus_id, 'rtpidatafeed': 'Port Authority Bus'} # The parameters passed into the API call
        data_request = req.get("http://realtime.portauthority.org/bustime/api/v3/getdirections", params = parameters) # Returns a JSON
        if data_request.status_code == 200:
            data = data_request.json()
        else: # Status code is not 200, there was an error in the API
            print("Error in request to API! Returning...")
            return
        bus_directions = data["bustime-response"].get("directions") # Parse the JSON

        for direction in bus_directions: # Print out the directions for each bus route to the user
            direction_name = direction.get("name") # INBOUND or OUTBOUND
            print(bus_id + ", " + bus_name + ", " + direction_name)
            new_route_info = {'rt': bus_id, 'rtnm': bus_name, 'dir': direction_name} # Aggregate the data for this route
            directions.append(new_route_info)

    with open("6routes.json", "w") as routes_file: # Save the json to a file
        json.dump(directions, routes_file)

# For a specified route ID and direction, get all of the bus stops
def get_stops(route_id, direction):
    directions = []

    if not os.path.exists("6routes.json"): # Make sure 6routes.json exists, because we'll need it later
        print("ERROR: file 6routes.json does not exist")
        return

    with open("6routes.json", "r") as bus_file: # Load directions data from file
        directions = json.load(bus_file)

    bus_directions = [route for route in directions if route.get("rt") == route_id and route.get("dir") == direction] # Find all the routes that fit the criteria (function arguments) that the user specified (route id and direction)
    if not len(bus_directions) == 1: # There was either 0 busses or more than 1 bus returned from the list comprehension; this is invalid
        print("ERROR: invalid route/direction combination: " + route_id + "/" + direction)
        return
    bus = bus_directions[0] # Easily grab the only bus we need

    parameters = {'format': FORMAT, 'key': API_KEY, 'rt': route_id, 'dir': direction, 'rtpidatafeed': 'Port Authority Bus'}
    data_request = req.get("http://realtime.portauthority.org/bustime/api/v3/getstops", params = parameters) # Returns a JSON
    if data_request.status_code == 200:
        data = data_request.json()
    else: # Status code from request was not 200, there was some kind of error in the API
        print("Error in request to API! Returning...")

    route_stops_combined = {} # Route id, Route direction, and all Route stops with their necessary information
    bus_stops_list = [] # Store the stop id and stop name for each bus stop on the above route
    stops = data["bustime-response"].get("stops")
    for stop in stops: # Parse the information for each stop
        stop_id = stop.get('stpid')
        stop_name = stop.get("stpnm")
        curr_stop = {'stpid': stop_id, 'stpnm': stop_name} # Current stop we're looking at on this route
        bus_stops_list.append(curr_stop)
        print(stop_id + ", " + stop_name) # Print the stop information out for the user

    # Aggregate more information just for the mystops.json file we're writing to
    route_stops_combined["rt"] = route_id
    route_stops_combined["dir"] = direction
    route_stops_combined["stops"] = bus_stops_list

    with open("mystops.json", "w") as stops_file: # Save the json to a file
        json.dump(route_stops_combined, stops_file)

# For a specified bus stop, find all the busses in 6routes.json that are arriving and when
def get_arrivals(stop_id):
    if not os.path.exists("6routes.json"):
        print("ERROR: file 6routes.json does not exist")
        return

    with open("6routes.json", "r") as bus_file:
        routes = json.load(bus_file)

    tmres = 'm' # Set time resolution for the timestamp to minutes ('s' for seconds, 'd' for days)
    parameters = {'format': FORMAT, 'key': API_KEY, 'stpid': stop_id, 'tmres': tmres, 'rtpidatafeed': 'Port Authority Bus'}
    data_request = req.get("http://realtime.portauthority.org/bustime/api/v3/getpredictions", params = parameters) # Returns a JSON
    if data_request.status_code == 200:
        data = data_request.json()
    else: # Status code from request was not 200, there was an error in the API
        print("Error in request to API! Returning...")

    stops = data["bustime-response"].get("prd") # Parse the JSON that was returned
    stop_arrivals = []

    if stops is None:
        print("No data was returned; Returning...")
        return

    for stop in stops:
        # Gather each and every piece of important information from this current bus stop
        stop_id = stop.get("stpid")
        stop_name = stop.get("stpnm")
        stop_timestamp = stop.get("tmstmp")
        route_id = stop.get("rt")
        route_direction = stop.get("rtdir")
        find_route = [route for route in routes if route.get("rt") == route_id and route.get("dir") == route_direction] # Find the route name (similar to destination) in the routes list with the current bus's ID and direction
        route_destination = find_route[0].get("rtnm") if len(find_route) == 1 else "TBD" # If we only found one bus in that routes list, use its route name; otherwise, the route name is TBD

        print(route_id + ", " + route_destination + ", " + route_direction + ", " + stop_id + ", " + stop_name + ", " + stop_timestamp)
        stop_information_agg = {'rt': route_id, 'rtnm': route_destination, 'rtdir': route_direction, 'stpid': stop_id, 'stopnm': stop_name, 'tmstmp': stop_timestamp}
        stop_arrivals.append(stop_information_agg)

    with open("myarrivals.json", "w") as arrivals_file:
        json.dump(stop_arrivals, arrivals_file)

# NOTE: Each command-line argument below is capitalized with .upper() just to keep string comparisons consistent later on
if len(sys.argv) == 2: # getroutes and getdirections take no command-line arguments
    if sys.argv[1] == "getroutes": # Download all of the available bus routes in the RealTime API
        get_routes()
    elif sys.argv[1] == "getdirections": # For all of the routes in allroutes.json, download all the directions for each route for busses that start with '6'
        get_directions()
    else:
        print("Invalid command-line argument, try again!")
elif len(sys.argv) == 3: # getarrivals takes one command-line argument
    if sys.argv[1] == "getarrivals": # For a specified bus stop, find all the busses in 6routes.json that are arriving and when
        get_arrivals(sys.argv[2].upper())
    else:
        print("Invalid command-line arguments, try again!")
elif len(sys.argv) == 4: # getstops takes two command-line arguments
    if sys.argv[1] == "getstops": # For a specified route ID and direction, get all of the bus stops
        get_stops(sys.argv[2].upper(), sys.argv[3].upper())
    else:
        print("Invalid command-line arguments, try again!")
else:
    print("Invalid number of arguments!")
