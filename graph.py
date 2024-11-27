import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_fake_data_with_extended_denials(start_date, end_date, max_quantity, num_points=100):
    # Generate dates
    date_range = pd.date_range(start=start_date, end=end_date, periods=num_points)
    
    # Initialize usage and denial lists
    usage = [0] * num_points
    denial = [0] * num_points  # Initialize denial data with zeros
    
    # Generate two peaks at random positions
    peaks = sorted(np.random.choice(range(1, num_points - 6), 2, replace=False))  # Leave space for 3-6 days of denials
    
    # Generate usage and denial data
    for i in range(num_points):
        if i in peaks:
            denial_duration = np.random.randint(3, 7)  # Randomly choose 3-6 days for denials
            for j in range(denial_duration):
                if i + j < num_points:
                    usage[i + j] = max_quantity  # Keep usage at peak for denial days
                    denial[i + j] = np.random.randint(3, 6)  # Random denial count (3-5 per day)
        elif usage[i] == 0:  # Non-peak usage fluctuates
            fluctuation = np.random.randint(-10, 10)
            prev_usage = usage[i - 1] if i > 0 else np.random.randint(0, max_quantity // 2)
            usage[i] = max(0, min(max_quantity, prev_usage + fluctuation))  # Ensure within bounds

    # Create DataFrame
    data = pd.DataFrame({
        "Date": date_range,
        "Quantity": max_quantity,
        "Usage": usage,
        "Denial": denial
    })
    
    return data

# Parameters
start_date = "2024-11-01"
end_date = "2024-12-30"
max_quantity = 150

# Generate data
data = generate_fake_data_with_extended_denials(start_date, end_date, max_quantity)

# Display the data
# import ace_tools as tools; tools.display_dataframe_to_user(name="Generated Graph Data with Delays", dataframe=data)
# Display the data
print(data)  # Print the first few rows of the dataframe
data.to_csv("generated_graph_data.csv", index=False)
print("Data saved to generated_graph_data.csv")


# Plotting the data
plt.figure(figsize=(12, 6))
plt.plot(data["Date"], data["Quantity"], label="Quantity (Max)", linestyle="--", color="grey")
plt.plot(data["Date"], data["Usage"], label="Usage", marker="o")
plt.scatter(data["Date"], data["Denial"], label="Denial", color="red")
plt.title("Fake Data with Extended Denials (3-6 Days After Peaks)")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.grid()
plt.show()



