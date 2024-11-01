import pandas as pd

# Define the path to the dataset
file_path = 'Laboratorio 8: Datasets/iris/bezdekIris.data'

# Define the column names
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

# Read the dataset
DataFrame = pd.read_csv(file_path, header=None, names=column_names)

# Display the first few rows of the dataframe
print(DataFrame.head())