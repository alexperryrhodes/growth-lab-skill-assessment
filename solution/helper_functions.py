import pandas as pd
from functools import reduce

################  Import and Export Functions ################
def import_file(filename):
    """Function which imports a CSV file as data frame"""
    
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print("Error:", filename, "file not found\n")
    except:
        print("Error:", filename, "CSV import failed\n")
    

def export_file(df, filename):
    """Function which writes out a df to a csv file"""
    
    df.to_csv(filename, index=False)




################  Data Prep & Manipulation Functions ################
def flatten_census_hierarchy(df):
    """Function which takes in a df with a hierarchy structure and returns a new df with a flatten structure for easier data processing"""

    # Create three separate data frames for each hierarchy level 
    # Rename and drop columns to better describe data
    state_df = df.loc[df["level"] == "state"][["id", "name", "abbrv", "parent_id"]].rename(columns={'id': 'state_id', 'name' :'state', 'parent_id': 'division_id'})
    division_df = df.loc[df["level"] == "division"][["id", "name", "parent_id"]].rename(columns={'name' :'division',  'parent_id': 'region_id'})
    region_df = df.loc[df["level"] == "region"][["id", "name"]].rename(columns={'name' :'region'})

    # Merge state and division data frames
    state_div_df = state_df.merge(division_df, 
                                how="left", 
                                left_on="division_id", 
                                right_on="id")

    # Merge new state/division data frame with region data frame
    reshaped_df = state_div_df.merge(region_df,
                                    how="left", 
                                    left_on="region_id", 
                                    right_on="id")
    
    # Drop extra columns no longer needed after merge
    reshaped_df.drop(columns=["id_x", "id_y"], inplace=True)

    return reshaped_df
    

def merge_class_census(class_df, census_df):
    """Function which takes in a state level census data frame and a classification data frame and applies division and region classification data to both 
    current and previous states in census data"""

    # Apply division and region data to census data for the current state
    current_df = census_df.merge(class_df,
                                how="left",
                                left_on="current_state",
                                right_on="abbrv")
    
    # Drop extra columns no longer needed after merge
    current_df.drop(columns=["state", "abbrv"], inplace=True)

    # Rename division/region columns to indicate they reference the current state
    current_df.rename(columns={"division": "current_division",
                             "division_id": "current_division_id",
                             "region": "current_region",
                             "region_id": "current_region_id",
                             "state_id": "current_state_id"}, 
                             inplace=True)

    # Apply division and region data to census data for the previous state
    merge_df = current_df.merge(class_df,
                                how="left",
                                left_on="previous_state",
                                right_on="abbrv")
    
    # Drop extra columns no longer needed after merge
    merge_df.drop(columns=["state", "abbrv"], inplace=True)

    # Rename division/region columns to indicate they reference the previous state
    merge_df.rename(columns={"division": "previous_division",
                             "division_id": "previous_division_id",
                             "region": "previous_region",
                             "region_id": "previous_region_id",
                             "state_id": "previous_state_id"}, 
                             inplace=True)

    return merge_df


def merge_population_census(population_df, census_df):
    """Function which takes in a state level census data frame and a population data frame and appends population data to both 
    current and previous states in census data"""

    # Merge with population data to get population for current state 
    current_df = census_df.merge(population_df,
                                how="left",
                                left_on=["current_state", "year"],
                                right_on=["state", "year"]) 
    
    # Drop extra columns no longer needed after merge
    current_df.drop(columns=["state"], inplace=True)

    # Rename population column to indicate it references the current state
    current_df.rename(columns={"population": "current_population"}, inplace=True)

    # Merge with population data to get population for previous state 
    merge_df = current_df.merge(population_df,
                                how="left",
                                left_on=["previous_state", "year"],
                                right_on=["state", "year"]) 

    # Drop extra columns no longer needed after merge
    merge_df.drop(columns=["state"], inplace=True)

     # Rename population column to indicate it references the previous state
    merge_df.rename(columns={"population": "previous_population"},inplace=True)

    return merge_df


def sum_data(df, col_list):
    """Function which takes in a data frame and aggregates and sums data"""
    
    agg_df = df.groupby(col_list).sum(numeric_only=True).reset_index()
    
    return agg_df


# Citation: https://stackoverflow.com/questions/48350850/subtract-two-columns-in-dataframe
def calculate_bounds(df):
    """"""
    new_df = df.copy(deep=True)

    new_df["estimate_lb"] = new_df.apply(lambda x: max(x['estimate'] - x['margin_of_error'], 0), axis=1)
    new_df["estimate_ub"] = new_df["estimate"] + new_df["margin_of_error"]

    new_df = new_df.astype({"estimate_lb": 'int', "estimate_ub": 'int'})

    return new_df


# Citation: https://stackoverflow.com/questions/44327999/how-to-merge-multiple-dataframes
def merge_datasets(df_list):
    """"""
    merged_df = reduce(lambda  left,right: pd.merge(left,
                                                    right,
                                                    on=['year'],
                                                    how='left'), df_list)
    
    return merged_df




################  Data Analysis Functions ################
def filter_by_state(df, state):
    """Function which takes in a data frame and returns a data frame filtered to the current state"""
    return df.loc[df["current_state"] == state].reset_index(drop=True)

# Citation: https://stackoverflow.com/questions/23394476/keep-other-columns-when-doing-groupby
def find_largest_move(df, state):
    """Returns df indicating which state had the largest number of people move to parameter state per year of data"""
    
    # Creates a new data frame with data only for the current data specified by state parameter
    state_df = df.loc[df["current_state"] == state].reset_index(drop=True)
    
    # Creates a new data frame based on the index locations of the max estimate per year
    largest_df = state_df.loc[state_df.groupby(["year"])['estimate'].idxmax()][['year', 'previous_state']].reset_index(drop=True)
    largest_df.rename(columns={"previous_state": "largest_move_to"}, inplace=True)
    
    return largest_df
    

def find_largest_proportion(df, state):
    """Returns df indicating which state had the largest proportion of its own population move to parameter state per year of data"""
    
    # Creates a new data frame with data only for the current data specified by state parameter
    state_df = df.loc[df["current_state"] == state].reset_index(drop=True)

    # Calculates the number of people who move to the state as a proportion of their previous state's population 
    state_df["move_proportion"] = state_df["estimate"] / state_df["previous_population"]

    # Creates a new data frame based on the index locations of the max proportion per year
    largest_df = state_df.loc[state_df.groupby(["year"])['move_proportion'].idxmax()][['year', 'previous_state']].reset_index(drop=True)
    largest_df.rename(columns={"previous_state": "largest_population_proportion"}, inplace=True)

    return largest_df


def find_move_above(df, state, pop_threshold):
    """Returns df indicating how many states had at least 'pop_threshold' number people move to parameter state per year of data"""
    
    # Creates a new data frame with data only for the current data specified by state parameter
    state_df = df.loc[df["current_state"] == state].reset_index(drop=True)

    # Creates a new data frame with states whose move count is above threshold
    above_df = state_df[state_df['estimate'] > pop_threshold]

    # Creates a new data frame which counts the number of states above threshold by year
    grouped_above_df = above_df.groupby(["year"]).size().reset_index(name='count_above_10000')

    return grouped_above_df


# Citation: https://stackoverflow.com/questions/23377108/pandas-percentage-of-total-with-groupby/57359372#57359372
def find_percentage_outside_division(df, state, division):
    """Returns df indicating what percentage of people who migrated to parameter state that per came from outside of the parameter division"""
    
    # Creates a new data frame with data only for the current data specified by state parameter
    state_df = df.loc[df["current_state"] == state].reset_index(drop=True)

    # Group data by year and division previous state is in
    agg_df = state_df.groupby(["year", "previous_division"])["estimate"].sum(numeric_only=True).reset_index()

    # Calculate what percentage each division represents for each year
    agg_df["div_percent"] =  agg_df['estimate'] / agg_df.groupby('year')['estimate'].transform('sum')

    # Filter a database to remove division from parameter
    filtered_df = agg_df[agg_df["previous_division"] != division].reset_index(drop=True)

    # Group data by year and division
    grouped_df = filtered_df.groupby(["year"])["div_percent"].sum(numeric_only=True).reset_index()

    # Rename column 
    grouped_df.rename(columns={"div_percent": "percent_outside_division"}, inplace=True)

    grouped_df["percent_outside_division"] = round(grouped_df["percent_outside_division"] * 100, 4)

    return grouped_df
