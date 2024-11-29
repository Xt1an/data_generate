import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_controlled_data(start_date, end_date, max_quantity, num_points=100):
    """
    Generate data with controlled peaks and denial periods.
    Usage increases randomly by 5–40 units before reaching each peak.
    Usage between peaks ranges from half the maximum quantity ±20.
    Usage does not reach the maximum quantity for 10 days after the second peak.

    Parameters:
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.
    max_quantity (int): Maximum value for the quantity and usage.
    num_points (int): Total number of data points.

    Returns:
    pd.DataFrame: Generated dataset with Date, Quantity, Usage, and Denial columns.
    """
    # Generate dates
    date_range = pd.date_range(start=start_date, end=end_date, periods=num_points)
    
    # Initialize usage and denial lists
    usage = [0] * num_points
    denial = [0] * num_points  # Initialize denial data with zeros
    
    # Generate the first peak after 5-8 days
    first_peak_day = np.random.randint(5, 9)
    # Generate the second peak 5-10 days after the first peak
    second_peak_day = first_peak_day + np.random.randint(20, 30)
    if second_peak_day >= num_points - 16:  # Ensure space for 10 days post-peak
        second_peak_day = num_points - 17
    
    # Peak positions
    peaks = [first_peak_day, second_peak_day]
    
    # Random incremental logic
    def random_increment(start, peak_day):
        """Generate random increments from start to the peak day."""
        increments = []
        current = start
        for _ in range(peak_day):
            step = np.random.randint(5, 41)  # Random increment between 5 and 40
            current = min(current + step, max_quantity)  # Cap at max_quantity
            increments.append(current)
        return increments

    # Generate random usage between peaks
    def random_between_peaks(length, base):
        """Generate random values within the range base ± 20."""
        return [base + np.random.randint(-20, 21) for _ in range(length)]
    
    # Gradually increase usage before peaks
    usage[:peaks[0]] = random_increment(0, peaks[0])
    usage[peaks[0]:peaks[1]] = random_between_peaks(peaks[1] - peaks[0], max_quantity // 2)
    
    # Generate peak and denial data
    for i in range(num_points):
        if i in peaks:
            # Add denial data after each peak
            denial_duration = np.random.randint(3, 7)  # Randomly choose 3-6 days for denials
            for j in range(denial_duration):
                if i + j < num_points:
                    usage[i + j] = max_quantity  # Keep usage at peak for denial days
                    denial[i + j] = np.random.randint(3, 6)  # Random denial count (3-5 per day)
        elif peaks[1] < i <= peaks[1] + 10:  # 10 days after the second peak
            # Ensure usage does not reach max_quantity
            fluctuation = np.random.randint(-10, 10)
            prev_usage = usage[i - 1] if i > 0 else max_quantity // 2
            usage[i] = max(0, min(max_quantity - 1, prev_usage + fluctuation))  # Keep below max_quantity
        elif i > peaks[1] + 10:  # After the 10-day restricted period
            # Allow usage to fluctuate randomly
            fluctuation = np.random.randint(-10, 10)
            prev_usage = usage[i - 1] if i > 0 else max_quantity // 2
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
max_quantity = 100

# Generate controlled data
data = generate_controlled_data(start_date, end_date, max_quantity)

# Save the data
data.to_csv("generated_graph_data.csv", index=False)
print("Data saved to generated_graph_data.csv")

# Display the data
print(data.head())  # Print the first few rows of the dataframe

# Plotting the data
plt.figure(figsize=(12, 6))
plt.plot(data["Date"], data["Quantity"], label="Quantity (Max)", linestyle="--", color="grey")
plt.plot(data["Date"], data["Usage"], label="Usage", marker="o")
plt.scatter(data["Date"], data["Denial"], label="Denial", color="red")
plt.title("Controlled Data with Post-Second Peak Restrictions")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.grid()
plt.show()
