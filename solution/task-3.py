from flask import Flask
from json import loads
from helper_functions import import_file, flatten_census_hierarchy, merge_class_census, calculate_bounds, filter_by_state, sum_data

app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return "Welcome to the Census Data page for North Carolina!"

@app.route('/previous_state/<id>/')
@app.route('/previous_state/<id>/<year>/')
def route_to_state(id, year=None):
    return filter_prev_state_id(id, year)

@app.route('/previous_division/<id>/')
@app.route('/previous_division/<id>/<year>/')
def route_to_division(id, year=None):
    return filter_prev_division_id(id, year)


def filter_prev_state_id(id, year=None):
    """Function which returns a json object which meets the criteria of the url parameters for previous state and year"""
    # Access data frame
    df = data_prep()

    # Filter by id
    output_df = df.loc[df["previous_state_id"] == id][["previous_state", "year", "estimate", "estimate_lb", "estimate_ub"]]

    # Filter by year
    if year is not None:
        output_df = output_df.loc[df["year"] == int(year)]

    # Convert to JSON 
    json =  output_df.to_json(orient="records")
    parsed = loads(json)
    return parsed

def filter_prev_division_id(id, year=None):
    """Function which returns a json object which meets the criteria of the url parameters for previous division and year"""
    # Access data frame
    df = data_prep()

    # Filter by id
    output_df = df.loc[df["previous_division_id"] == id][["previous_division", "year", "estimate", "estimate_lb", "estimate_ub"]]

    # Filter by year
    if year is not None:
        output_df = output_df.loc[df["year"] == int(year)]

    # Sum data by division and year
    grouped_output_df = sum_data(output_df, ["previous_division", "year"])

    # Convert to JSON 
    json =  grouped_output_df.to_json(orient="records")
    parsed = loads(json)
    return parsed


def data_prep():
    # Import required files
    class_df = import_file("../problem/census_classification.csv")
    if class_df.empty:
        return

    census_df = import_file("../problem/census_migration_data.csv")
    if census_df.empty:
        return
    
    # Reshape and merge census data with census classification data and population data to prep for analysis 
    reshaped_df = flatten_census_hierarchy(class_df)
    merged_df = merge_class_census(reshaped_df, census_df)
    bounded_df = calculate_bounds(merged_df)
    nc_df = filter_by_state(bounded_df, "NC")

    return nc_df
