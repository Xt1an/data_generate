import pandas as pd
import matplotlib.pyplot as plt

def load_and_display_data(csv_file):
    """
    Load data from a CSV file and display a table and a graph.
    
    Parameters:
    csv_file (str): Path to the CSV file containing the data.
    """
    try:
        # Load data from CSV
        data = pd.read_csv(csv_file)

        # Display the first few rows of the data
        print("Data Preview:")
        print(data.head())
        
        # Ensure required columns exist
        required_columns = {"Date", "Quantity", "Usage", "Denial"}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"The CSV file must contain the following columns: {required_columns}")
        
        # Convert 'Date' column to datetime if it's not already
        data["Date"] = pd.to_datetime(data["Date"])

        # Plot the data
        plt.figure(figsize=(12, 6))
        plt.plot(data["Date"], data["Quantity"], label="Quantity (Max)", linestyle="--", color="grey")
        plt.plot(data["Date"], data["Usage"], label="Usage", marker="o")
        plt.scatter(data["Date"], data["Denial"], label="Denial", color="red")
        plt.title("Loaded Data from CSV")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid()
        plt.show()
        
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
csv_file_path = "generated_graph_data.csv"  # Replace with the path to your CSV file
load_and_display_data(csv_file_path)
