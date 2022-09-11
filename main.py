# Dependencies
import pandas as pd
import nfl_data_py as nfl
import os
import urllib.request
import get_logos

# MPL Dependencies
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.lines
from matplotlib.transforms import Bbox, TransformedBbox
from matplotlib.legend_handler import HandlerBase
from matplotlib.image import BboxImage

# Define the matchup parameters
year = int(input("Enter the year (data starts 1999): "))
year_string = str(year)
week = input("Enter the week the game was played (format: 01, 05, 12): ")
away_team = input("Enter the away team (format: NE, KC, GB): ")
home_team = input("Enter the home team (format: NE, KC, GB): ")

# Use the get logos function
logo_df = get_logos.get_logos()

# Load the NFL PBP data
pbp_df = nfl.import_pbp_data([year])

# Filter down to a single game
pbp_df = pbp_df[pbp_df['game_id'] == f'{year_string}_{week}_{away_team}_{home_team}']

# Filter down to necessary columns
pbp_df = pbp_df[['posteam', 'game_seconds_remaining', 'away_wp', 'home_wp']]

# Rename posteam to team_abbr
pbp_df = pbp_df.rename(columns={'posteam':'team_abbr'})

# Join logo_df on pbp_df to get colors and logos
vis_df = pd.merge(pbp_df, logo_df)

# Define home and away color variables
away_color = vis_df[vis_df['team_abbr'] == away_team].iloc[0]['team_color']
home_color = vis_df[vis_df['team_abbr'] == home_team].iloc[0]['team_color']

# Define home and away logo paths
away_path = str(vis_df[vis_df['team_abbr'] == away_team].iloc[0]['logo_path'])
home_path = str(vis_df[vis_df['team_abbr'] == home_team].iloc[0]['logo_path'])

# Taken from https://stackoverflow.com/questions/42155119/replace-matplotlib-legends-labels-with-image
class HandlerLineImage(HandlerBase):

    def __init__(self, path, space=15, offset=10):
        self.space = space
        self.offset = offset
        self.image_data = plt.imread(path)
        super(HandlerLineImage, self).__init__()

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):

        l = matplotlib.lines.Line2D([xdescent+self.offset, xdescent+(width-self.space)/3.+self.offset],
                                    [ydescent+height/2., ydescent+height/2.])
        l.update_from(orig_handle)
        l.set_clip_on(False)
        l.set_transform(trans)

        bb = Bbox.from_bounds(xdescent + (width+self.space)/3.+self.offset,
                              ydescent,
                              height *
                              self.image_data.shape[1] /
                              self.image_data.shape[0],
                              height)

        tbb = TransformedBbox(bb, trans)
        image = BboxImage(tbb)
        image.set_data(self.image_data)

        self.update_prop(image, orig_handle, legend)
        return [l, image]

# Style the chart
plt.style.use('fivethirtyeight')

# Define plot size and autolayout
plt.rcParams["figure.figsize"] = [12, 9]
plt.rcParams["figure.autolayout"] = True

# Define the subplot
fig, ax = plt.subplots()

# Plot the data on the subplots
home_line, = ax.plot(pbp_df['game_seconds_remaining'],
                     pbp_df['away_wp'], color=away_color, linewidth=5)
away_line, = ax.plot(pbp_df['game_seconds_remaining'],
                     pbp_df['home_wp'], color=home_color, linewidth=5)

# Chart parameters
plt.title(f'Week {week}, {year} - {away_team} @ {home_team} Win Probabilities',
          fontdict={'fontsize': 30})
plt.xlim((0, 3600))
plt.xlabel("Game Seconds Remaining", {'fontsize': 25})
plt.ylabel("Win Probability %", {'fontsize': 25})

# Define the chart legend
plt.legend([away_line, home_line], ["", ""],
           handler_map={home_line: HandlerLineImage(
               away_path), away_line: HandlerLineImage(home_path)},
           handlelength=2, labelspacing=0.0, fontsize=45, borderpad=0.15, loc=3,
           handletextpad=0.2, borderaxespad=0.15)

# Invert the x-axis so that it ends when there are 0 second remaining
ax.invert_xaxis()

plt.show()
