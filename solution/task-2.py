from helper_functions import import_file, export_file, flatten_census_hierarchy, merge_class_census, merge_population_census, find_largest_move, find_largest_proportion, find_move_above, find_percentage_outside_division, merge_datasets

def main():

    # Import required files
    class_df = import_file("../problem/census_classification.csv")
    if class_df.empty:
        return

    census_df = import_file("../problem/census_migration_data.csv")
    if census_df.empty:
        return
    
    population_df = import_file("../problem/state_populations.csv")
    if population_df.empty:
        return
    
    # Reshape and merge census data with census classification data and population data to prep for analysis 
    reshaped_df = flatten_census_hierarchy(class_df)
    merged_df = merge_class_census(reshaped_df, census_df).drop(columns=["margin_of_error", "current_state_id", "previous_state_id"])
    prepped_df = merge_population_census(population_df, merged_df)

    # Call four analysis functions which each return aggregated data frame
    largest_move_df = find_largest_move(prepped_df, "NC")
    largest_prop_df = find_largest_proportion(prepped_df, "NC")
    move_above_df = find_move_above(prepped_df, "NC", 10000)
    percent_out_df = find_percentage_outside_division(prepped_df, "NC", "South Atlantic")

    # Combined all data frames into one large data frame
    output_df = merge_datasets([largest_move_df, largest_prop_df, move_above_df, percent_out_df])

    export_file(output_df, "nc_migration.csv")


if __name__ == "__main__":
    main()
