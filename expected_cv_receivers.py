import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

def load_player_data():
    """
    Load mean fantasy points, tds per target, air yards per target, position, player name. 

    *** Get this from a projection source like 4for4 or market-derived projections.
    """
    pass

def fit_model():
    pass

def create_new_columns():
    pass

# Load the new Excel file with the updated data
file_path = './data/nfldatapy/player_fpts_alltime_airyards_processed.xlsx'
df = pd.read_excel(file_path)

# Filter data based on the user's criteria
filtered_df = df[
    (df['position_first'].isin(['WR', 'TE'])) &
    (df['player_display_name_size'] > 16) &
    (df['fantasy_points_ppr_mean'] >= 7)
]

# Select relevant columns including the new 'tds_per_target' variable and excluding 'pct_fpts_ppr_from_receptions'
X = filtered_df[['fantasy_points_ppr_mean', 'tds_per_target', 'air_yards_per_target']]
y = filtered_df['fantasy_points_ppr_cv']

# Standardize the predictors
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit the linear regression model
model = LinearRegression()
model.fit(X_scaled, y)

# Get the coefficients and intercept for the linear equation
coefficients = model.coef_
intercept = model.intercept_

# Predict and create a new column for the predictions
filtered_df['predicted_fantasy_points_ppr_cv'] = model.predict(X_scaled)

# Calculate the averages for air_yards_per_target and tds_per_target
average_air_yards_per_target = X['air_yards_per_target'].mean()
average_tds_per_target = X['tds_per_target'].mean()

# Use player's specific 'fantasy_points_ppr_mean' with average 'air_yards_per_target' and 'tds_per_target'
baseline_df = pd.DataFrame({
    'fantasy_points_ppr_mean': filtered_df['fantasy_points_ppr_mean'],
    'tds_per_target': [average_tds_per_target] * len(filtered_df),
    'air_yards_per_target': [average_air_yards_per_target] * len(filtered_df),
})

# Standardize the baseline data using the same scaler
baseline_scaled = scaler.transform(baseline_df)

# Calculate baseline_cv using the linear regression model
filtered_df['baseline_cv'] = model.predict(baseline_scaled)

# Calculate cv_above_expected
filtered_df['cv_above_expected'] = filtered_df['predicted_fantasy_points_ppr_cv'] - filtered_df['baseline_cv']

# Save the final DataFrame with all required columns to a CSV file
filtered_df = filtered_df.round(3)
final_output_path = './data/nfldatapy/fantasy_points_ppr_cv_with_corrected_baseline.csv'
filtered_df[[
    'player_display_name', 'fantasy_points_ppr_mean', 'tds_per_target', 'air_yards_per_target',
    'fantasy_points_ppr_cv', 'predicted_fantasy_points_ppr_cv', 'baseline_cv', 'cv_above_expected'
]].to_csv(final_output_path, index=False)
