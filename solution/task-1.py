from helper_functions import import_file, export_file, flatten_census_hierarchy, merge_class_census, sum_data

def main():

    # Import required files
    class_df = import_file("../problem/census_classification.csv")
    if class_df.empty:
        return

    census_df = import_file("../problem/census_migration_data.csv")
    if census_df.empty:
        return

    # Prep files by reshaping census classification data and merge with census data 
    reshaped_df = flatten_census_hierarchy(class_df)
    merged_df = merge_class_census(reshaped_df, census_df).drop(columns=["margin_of_error", "current_state_id", "previous_state_id"])

    # With files now shaped, aggregate at the appropriate grain
    agg_df = sum_data(merged_df, ["year", "previous_division", "previous_division_id", "current_region", "current_region_id"])

    # Export aggregated file 
    export_file(agg_df, "aggregated_migration.csv")


if __name__ == "__main__":
    main()
