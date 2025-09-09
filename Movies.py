# -----------------------------------------------------------
# 📊 Netflix Movie Data Analysis
# -----------------------------------------------------------
# Author  : Pankaj Yadav
# Purpose : Data Cleaning, Transformation, and Visualization
# Dataset : mymoviedb.csv
# -----------------------------------------------------------

# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------------
# 1. Load the dataset
# -----------------------------------------------------------
# NOTE: Change the file path based on your system
df = pd.read_csv(r'"E:\Github Repositories\Netflix-Movies-Analysis-Project\mymoviedb.csv"', lineterminator='\n')

# Quick inspection of dataset (uncomment if needed)
# print(df.head(10))        # Show first 10 rows
# print(df.info())          # Show column info
# print(df.describe())      # Show summary statistics

# -----------------------------------------------------------
# 2. Data Cleaning & Preprocessing
# -----------------------------------------------------------

# Convert 'Release_Date' column from string to datetime
df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')

# Extract only the year from 'Release_Date'
df['Release_Date'] = df['Release_Date'].dt.year

# Drop unnecessary columns to simplify analysis
cols_to_drop = ['Overview', 'Original_Language', 'Poster_Url']
df.drop(cols_to_drop, axis=1, inplace=True)

# -----------------------------------------------------------
# 3. Categorizing 'Vote_Average'
# -----------------------------------------------------------
# Function to categorize numerical columns into groups (bins)
def categorize_col(df, column, labels):
    """
    Categorize a numerical column into bins using quartiles.
    Args:
        df      : DataFrame
        column  : Column name to categorize
        labels  : List of category labels
    Returns:
        df with a new categorized column
    """
    # Create bin edges based on descriptive statistics
    edges = [
        df[column].describe()['min'],   # Minimum value
        df[column].describe()['25%'],   # 25th percentile
        df[column].describe()['50%'],   # Median
        df[column].describe()['75%'],   # 75th percentile
        df[column].describe()['max']    # Maximum value
    ]

    # Apply binning with category labels
    df[column] = pd.cut(df[column], edges, labels=labels, duplicates='drop')
    return df

# Define categories for Vote_Average
labels = ['Not_popular', 'Below_avg', 'Average', 'Popular']
df = categorize_col(df, 'Vote_Average', labels)

# Drop missing values (if any exist after transformations)
df.dropna(inplace=True)

# -----------------------------------------------------------
# 4. Handling Multiple Genres
# -----------------------------------------------------------
# 'Genre' column may contain multiple genres separated by commas.
# Example: "Drama, Thriller, Action"
# We split them into multiple rows (data normalization).

df['Genre'] = df['Genre'].str.split(', ')
df = df.explode('Genre').reset_index(drop=True)

# Convert Genre to a categorical datatype for better efficiency
df['Genre'] = df['Genre'].astype('category')

# -----------------------------------------------------------
# 5. Data Visualization
# -----------------------------------------------------------

# Set seaborn style
sns.set_style('whitegrid')

# 5.1 Most frequent genres
plt.figure(figsize=(10,6))
sns.countplot(y='Genre', data=df, order=df['Genre'].value_counts().index, color='#4287f5')
plt.title('Most Frequent Movie Genres on Netflix', fontsize=14)
plt.xlabel('Count')
plt.ylabel('Genre')
plt.show()

# 5.2 Distribution of Vote_Average categories
plt.figure(figsize=(8,5))
sns.countplot(y='Vote_Average', data=df, order=df['Vote_Average'].value_counts().index, color='#f54291')
plt.title('Vote Average (Rating) Distribution', fontsize=14)
plt.xlabel('Count')
plt.ylabel('Vote Category')
plt.show()

# 5.3 Movie release trend over the years
plt.figure(figsize=(10,6))
df['Release_Date'].hist(bins=30, color="#05436d")
plt.title('Distribution of Movies Released Over the Years', fontsize=14)
plt.xlabel('Release Year')
plt.ylabel('Number of Movies')
plt.show()

# -----------------------------------------------------------
# 6. Insights: Most & Least Popular Movies
# -----------------------------------------------------------

# Most popular movie(s)
most_popular = df[df['Popularity'] == df['Popularity'].max()]
print("🎬 Most Popular Movie(s):")
print(most_popular[['Title', 'Popularity', 'Genre', 'Release_Date']])
print("\n")

# Least popular movie(s)
least_popular = df[df['Popularity'] == df['Popularity'].min()]
print("🎬 Least Popular Movie(s):")
print(least_popular[['Title', 'Popularity', 'Genre', 'Release_Date']])
# -----------------------------------------------------------
# End of Project
# -----------------------------------------------------------
