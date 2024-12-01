import polars as pl
import pyarrow


##### UTILITY FUNCTIONS SECTION ######

# Need to make sure our FIPS codes are read as strings
def pad_code(int):
    """
    Takes:
        int (int): An integer, often a FIPS code that is displaying as a integer
        that we need to convert to a 5-character string

    Returns:
        out (str): A 5-digit fips code string. If the integer given was less than five
        a 0 is added up front.
    """
    string = str(int)
    if len(string) < 2:
        string = "0" + string

    
    return string

def make_juris_labels(int):
    """
    This function recodes 0,1 into string labels for displaying the charts.

    Takes:
        int (int): A 0 or 1 value that is meant to indicate if the state or Tribal
        Authority has criminal jurisdiction on Native American Lands.
    Returns:
        out (str): A string that is either "State" or "Tribal Authority"
    """
    out = "Unknown"
    if int == 1:
        out = "State"
    if int == 0:
        out = "Tribal Authority"
    
    return out

def group_states_mod(df , grp = "State"):

    """
    Groups our dataframe by state (or another category) type applies relevant
    aggregation functions.
    Takes:
    df: A polars dataframe to group
    returns:
    grouped_df: A grouped polars dataframe
    """
    grouped_df = df.group_by(grp).agg(pl.col("population_AIAN").sum(),
                                                   pl.col("deaths_AIAN").sum(),
                                                   pl.col("Jurisdiction").first(),
                                                   pl.col("id").first(),
                                                   pl.col("pop_non_AIAN").sum(),
                                                   pl.col("deaths_non_AIAN").sum())
    
    grouped_df = grouped_df.with_columns((100000*pl.col("deaths_AIAN")/pl.col("population_AIAN")
                                        ).round(decimals = 2).alias("drd_AIAN_p100k"),
                                        (100000*pl.col("deaths_non_AIAN")/pl.col("pop_non_AIAN")
                                        ).alias("drd_non_p100k"))

    return grouped_df


#### CLEANING FUNCTIONS SECTION ######

def clean_states():

    # Load the raw data
    AIAN_deaths = pl.read_csv("data/AIAN_drds_state.csv")

    #These two lines create new variables where instead of using the rate of deaths, we adjust it to be the number of Drug-Related
    # deaths per 100,000 persons.
    AIAN_deaths = AIAN_deaths.with_columns((pl.col("OD_rate_AIAN")*100000).round(decimals = 3).alias("drd_AIAN_p100k"))
    AIAN_deaths = AIAN_deaths.with_columns((pl.col("OD_rate_non_AIAN")*100000).round(decimals = 3).alias("drd_non_p100k"))

    # We use our functions define above to adjust FIPS codes to be strings and to reforumate our state_crim variable to be a string.
    AIAN_deaths = AIAN_deaths.with_columns(pl.col("state_code").map_elements(pad_code, return_dtype= pl.String).alias("id"))
    AIAN_deaths = AIAN_deaths.with_columns(pl.col("state_crim").map_elements(make_juris_labels, return_dtype= pl.String
                                                                            ).alias("Jurisdiction"))
    
    return AIAN_deaths

def load_states():
    AIAN_deaths = clean_states()
    AIAN_deaths = AIAN_deaths.write_csv()
    return AIAN_deaths

def load_state_agg():
    AIAN_deaths = clean_states()
    AIAN_deaths = group_states_mod(df = AIAN_deaths)
    return AIAN_deaths.write_csv()
    
