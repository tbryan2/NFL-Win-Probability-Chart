import urllib.request
import os
import nfl_data_py as nfl
import pandas as pd


def get_logos():

    # Pull the team description
    logos = nfl.import_team_desc()

    # Keep only the necessary columns in the logos DataFrame
    logos = logos[['team_abbr', 'team_logo_espn', 'team_color']]

    # Initialize an empty list for the logo file paths
    logo_paths = []

    # Initialize an empty list for the team abbreviations
    team_abbr = []

    # Initialize an empty list for the team colors
    team_color = []

    # Create a folder for the image files if it doesn't exist
    if not os.path.exists("logos"):
        os.makedirs("logos")

    # Pull the team logos from the URL and save them in the logos folder, save the file paths to
    for team in range(len(logos)):
        urllib.request.urlretrieve(
            logos['team_logo_espn'][team], f"logos/{logos['team_abbr'][team]}.tif")
        logo_paths.append(f"logos/{logos['team_abbr'][team]}.tif")
        team_abbr.append(logos['team_abbr'][team])
        team_color.append(logos['team_color'][team])


    # Create a dictionary to put logo_paths and team_abbr in
    data = {'team_abbr': team_abbr,
            'logo_path': logo_paths, 'team_color': team_color}

    # Create a DataFrame from the dictionary
    logo_df = pd.DataFrame(data)

    return logo_df
