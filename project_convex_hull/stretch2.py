import math

from matplotlib import pyplot as plt
from pandas import pandas as pd

import convex_hull


def plot_hull(ax, points: list[tuple[float, float]], hull: list[tuple[float, float]], title: str):
    """Plots all points and the convex hull on a given matplotlib axis."""
    # Extract x (longitude) and y (latitude) for all points
    all_x = [p[0] for p in points]
    all_y = [p[1] for p in points]

    # Plot all data points
    ax.scatter(all_x, all_y, c='blue', label='Reported Locations', s=10, zorder=2)

    if not hull or len(hull) < 2:
        ax.set_title(title)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True)
        return

    # --- Sort hull points for plotting ---
    # Your D&C algorithm might not return points in order. Sort them by angle.
    cx = sum(p[0] for p in hull) / len(hull)
    cy = sum(p[1] for p in hull) / len(hull)
    sorted_hull = sorted(hull, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

    # Extract sorted coordinates and close the loop for plotting
    hull_x = [p[0] for p in sorted_hull]
    hull_y = [p[1] for p in sorted_hull]
    hull_x.append(sorted_hull[0][0])
    hull_y.append(sorted_hull[0][1])

    # Plot the hull polygon lines
    ax.plot(hull_x, hull_y, 'r-', label='Convex Hull', lw=2, zorder=3)
    # Plot the hull vertices
    ax.scatter(hull_x[:-1], hull_y[:-1], c='red', s=30, zorder=4, label='Hull Vertices')

    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend()
    ax.grid(True)


def run_hull_on_dataset_monthly(filepath: str, months: list[str]):
    """Loads dataset, computes hull for specified months, and plots them."""

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        return
    except Exception as e:
        print(f"An error occurred loading the CSV: {e}")
        return

    # --- Data Cleaning ---
    df.columns = df.columns.str.strip().str.lower()
    required_cols = ['observationdate', 'latitude', 'longitude']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: CSV missing required columns: {required_cols}.")
        return

    try:
        # Parse dates using the correct format MM/DD/YYYY
        df['observationdate'] = pd.to_datetime(df['observationdate'], format='%m/%d/%Y')
    except ValueError as e:
        print(f"Error parsing dates: {e}. Ensure format is MM/DD/YYYY.")
        return

    # Convert coordinates to numeric, handling potential errors
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df.dropna(subset=['latitude', 'longitude'], inplace=True)

    # Extract Year-Month for filtering
    df['year_month'] = df['observationdate'].dt.strftime('%Y-%m')

    # --- Plotting ---
    fig, axes = plt.subplots(1, len(months), figsize=(21, 7))
    # Ensure axes is always a list for consistent indexing
    if len(months) == 1:
        axes = [axes]

    for i, month_str in enumerate(months):
        ax = axes[i]  # Select the current subplot axis

        # 1. Filter data for the specific month
        month_data = df[df['year_month'] == month_str].copy()

        if month_data.empty:
            print(f"No data found for month {month_str}.")
            ax.set_title(f"Month {month_str}\n(No data)")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.grid(True)
            continue

        # 2. Get unique (longitude, latitude) points for the entire month
        points_df = month_data[['longitude', 'latitude']].drop_duplicates()
        points = [tuple(x) for x in points_df.values]

        print(f"--- Processing Month {month_str} ---")
        print(f"Found {len(points)} unique locations.")

        if len(points) < 3:
            print("Not enough unique points to compute a hull.")
            ax.set_title(f"Month {month_str}\n(Less than 3 unique points)")
            if points:
                ax.scatter([p[0] for p in points], [p[1] for p in points], c='blue', s=10)
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.grid(True)
            continue

        # 3. Compute the hull using the imported function
        # Pass a copy because the algorithm sorts the list in-place
        hull = convex_hull.compute_hull_dvcq(list(points))

        print(f"Hull contains {len(hull)} vertices.")

        # 4. Plot the result
        plot_title = f"Geographic Hull for {month_str}"
        plot_hull(ax, points, hull, plot_title)

    fig.suptitle("Convex Hull of COVID-19 Reported Locations Over Time (Monthly)", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout

    # Save the figure to a PNG file
    save_path = "covid_hull_monthly_plots.png"
    try:
        plt.savefig(save_path)
        print(f"\nPlot saved successfully as '{save_path}'")
    except Exception as e:
        print(f"\nError saving plot: {e}")

    # Optionally, still show the plot after saving:
    plt.show()


if __name__ == "__main__":
    # Define the file to use
    csv_file = "Covid_19_Countrywise_timeseries.csv"

    # Define the three months to analyze (use YYYY-MM format)
    # Using months based on the sample data you provided
    months_to_plot = ["2020-01", "2020-02", "2020-03"]

    # Run the analysis
    run_hull_on_dataset_monthly(csv_file, months_to_plot)
