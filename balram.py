# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define a function to change the file format and transpose the data
def file_change(filename):
    # Read the data from the csv file and skip the first 3 rows
    data = pd.read_csv(filename, skiprows=3)
    df = data
    
    # Remove unnecessary columns
    df1 = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], axis=1)
    
    # Set the Country Name column as index and transpose the data
    df1 = df1.set_index('Country Name')
    df1 = df1.transpose()
    
    # Save the transposed data to a new csv file
    df1.to_csv('df1transpose.csv')

    return data, df1

# Specify the filename and call the file_change function to get the transposed data
filename = "API_19_DS2_en_csv_v2_4902199.csv"
df_years, df_countries = file_change(filename)

# Print the descriptive statistics of the transposed data
print(df_countries.describe())

# Check the information of the original data
#df_years.info()

# Check the number of missing values in the original data
#df_years.isnull().sum()

# Replace missing values in the original data with 0
data = df_years.fillna(0)
print(data)

# Define a function to plot a line chart for a given indicator name
def lineplot_corr(df, indicator_name):
    # Save the data to a new csv file
    df.to_csv('data_read122.csv')
    
    # Remove unnecessary columns and set the Indicator Name column as index
    df = df.drop(["Country Code", "Indicator Code"], axis=1)
    df.set_index("Indicator Name", inplace=True)
    
    # Get the data for the specified indicator name and reset the index
    df = df.loc[indicator_name]
    df = df.reset_index(level="Indicator Name")
    
    # Select the countries to plot and plot a line chart
    countries_selected = ["China", "India", "Canada", "Germany","Croatia"]
    df = df[df['Country Name'].isin(countries_selected)]
    df.plot(x="Country Name", y=['1975', '1980', '1985', '1990', '1995', '2000', '2005', '2010', '2015', '2020'], figsize=(15, 5))
    plt.title(indicator_name)
    plt.show()

# Call the lineplot_corr function to plot a line chart for "Population growth (annual %)" indicator
lineplot_corr(data, "Agricultural land (% of land area)")



def barplot_corr(df, indicator_name):
    # Drop unnecessary columns
    df = df.drop(["Country Code","Indicator Code"],axis=1)
    # Set the index to the indicator name
    df.set_index("Indicator Name", inplace=True)
    # Select data for the given indicator
    df = df.loc[indicator_name]
    # Reset the index to get the indicator name back as a column
    df = df.reset_index(level="Indicator Name")
    # Select data for a subset of countries
    countries_selected = ["China", "India", "Canada", "Germany","Croatia"]
    df = df[df['Country Name'].isin(countries_selected)]
    # Create a bar plot
    df.plot(x="Country Name", y=['1975', '1980', '1985', '1990', '1995', '2000', '2005', '2010', '2015', '2020'], kind="bar")
    plt.title(indicator_name)
    plt.show()

# Call the barplot_corr function to create a bar plot for the "Agricultural land (% of land area)" indicator
barplot_corr(data, "Cereal yield (kg per hectare)")

def heatmap_corr():
    # Group the data by country name
    country_group = data.groupby("Country Name")
    # Filter rows related to Brazil
    group_count = country_group.get_group("Brazil")
    grp_data1 = group_count.set_index("Indicator Name")
    # Select data for the years 2000-2020 and transpose the data
    grp_data1 = grp_data1.loc[:, '2000':'2020']
    grp_data1 = grp_data1.transpose()
    # Select a subset of indicators
    indicators_list = ["Forest area (% of land area)",
    "Arable land (% of land area)",
    "Urban population growth (annual %)",
    "Population growth (annual %)",
    "Agricultural land (% of land area)"]
    group_indicators = grp_data1[indicators_list]
    # Compute the correlation matrix
    correlation_matrix = group_indicators.corr()
    # Define the labels for the indicators
    indicator_labels = ["Forest area (% of land area)",
    "Arable land (% of land area)",
    "Urban population growth (annual %)",
    "Population growth (annual %)",
    "Agricultural land (% of land area)"]
    # Create a heatmap of the correlation matrix
    sns.heatmap(correlation_matrix, cmap="magma", annot=True, xticklabels=indicator_labels, yticklabels=indicator_labels)
    plt.title("Brazil Indicators correlation")
    plt.show()

# Call the heatmap_corr function to create a heatmap of indicator correlations for Brazil
heatmap_corr()
