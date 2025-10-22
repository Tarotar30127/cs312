import math
from matplotlib import pyplot as plt
# from matplotlib.patches import Circle # No longer using separate Circle objects
import pandas as pd
from typing import List, Tuple, Dict, Optional

# Assuming your convex_hull functions are in convex_hull.py
import convex_hull

# --- Heavily Modified Plotting Function ---
def plot_hulls_multilevel(ax,
                          all_points_info: List[Tuple[float, float, str]],
                          overall_hull_points_info: List[Tuple[float, float, str]],
                          country_hulls: Dict[str, List[Tuple[float, float]]],
                          title: str):
    """Plots all points, individual country hulls, the overall hull, and highlights overall vertices."""

    # --- Plot all data points (blue dots) ---
    if not all_points_info:
        ax.set_title(title + "\n(No data)")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True)
        return

    all_x = [p[0] for p in all_points_info]
    all_y = [p[1] for p in all_points_info]
    # Use smaller dots for individual locations
    ax.scatter(all_x, all_y, c='lightblue', label='Reported Locations', s=8, zorder=2, alpha=0.6)

    # --- Plot Individual Country Hulls (if they have >= 3 points) ---
    plotted_country_hull = False
    for country, hull_coords in country_hulls.items():
        if len(hull_coords) >= 3: # Only plot polygons for 3+ points
            try:
                # Sort vertices for plotting line
                cx_c = sum(p[0] for p in hull_coords) / len(hull_coords)
                cy_c = sum(p[1] for p in hull_coords) / len(hull_coords)
                sorted_hull_c = sorted(hull_coords, key=lambda p: math.atan2(p[1] - cy_c, p[0] - cx_c))

                hull_c_x = [p[0] for p in sorted_hull_c]
                hull_c_y = [p[1] for p in sorted_hull_c]
                hull_c_x.append(sorted_hull_c[0][0]) # Close loop
                hull_c_y.append(sorted_hull_c[0][1])

                # Use a less prominent style for country hulls
                ax.plot(hull_c_x, hull_c_y, 'g--', label='Country Hull' if not plotted_country_hull else "", lw=1, zorder=3, alpha=0.7)
                plotted_country_hull = True # Ensure label appears only once in legend
            except Exception as e:
                print(f"  Skipping plotting country hull for {country} due to error: {e}")
        # Optionally, plot lines for 2 points or single points for 1 point
        elif len(hull_coords) == 2:
             ax.plot([hull_coords[0][0], hull_coords[1][0]], [hull_coords[0][1], hull_coords[1][1]], 'g--', lw=1, zorder=3, alpha=0.7)
        # Single points are already covered by the blue dots

    # --- Plot Overall Hull and its Vertices ---
    if not overall_hull_points_info or len(overall_hull_points_info) < 2:
        ax.set_title(title)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend()
        ax.grid(True)
        return

    # Extract coordinates from overall_hull_points_info
    overall_hull_coords = [(p[0], p[1]) for p in overall_hull_points_info]

    # Sort overall hull points for plotting the polygon line
    cx_o = sum(p[0] for p in overall_hull_coords) / len(overall_hull_coords)
    cy_o = sum(p[1] for p in overall_hull_coords) / len(overall_hull_coords)
    overall_hull_info_sorted = sorted(overall_hull_points_info, key=lambda p: math.atan2(p[1] - cy_o, p[0] - cx_o))

    overall_line_x = [p[0] for p in overall_hull_info_sorted]
    overall_line_y = [p[1] for p in overall_hull_info_sorted]
    overall_line_x.append(overall_hull_info_sorted[0][0]) # Close loop
    overall_line_y.append(overall_hull_info_sorted[0][1])

    # Plot the overall hull polygon line (make it prominent)
    ax.plot(overall_line_x, overall_line_y, 'r-', label='Overall Hull', lw=2.5, zorder=4)

    # Plot Overall Hull Vertices, Circles, and Labels
    overall_vertex_x = [p[0] for p in overall_hull_points_info]
    overall_vertex_y = [p[1] for p in overall_hull_points_info]

    # Plot red dots for overall vertices
    ax.scatter(overall_vertex_x, overall_vertex_y, c='red', s=40, zorder=5, label='Overall Hull Vertices')
    # Plot yellow circles around overall vertices
    ax.scatter(overall_vertex_x, overall_vertex_y, s=150, facecolors='none', edgecolors='orange', linewidth=1.5, zorder=6, label='Highlight Overall Vertex')

    # Add country labels near overall vertices
    processed_labels = set() # Avoid overlapping labels if multiple vertices are close
    for lon, lat, country in overall_hull_points_info:
         label_pos = (round(lon, 1), round(lat, 1)) # Group nearby labels
         if label_pos not in processed_labels:
             ax.text(lon + 1, lat + 1, country, fontsize=9, zorder=7, color='black',
                     bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.6))
             processed_labels.add(label_pos)


    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # --- Adjust Legend ---
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = {}
    # Prioritize Overall Hull labels
    priority_labels = ['Overall Hull', 'Overall Hull Vertices', 'Highlight Overall Vertex', 'Country Hull', 'Reported Locations']
    ordered_handles = []
    ordered_labels = []

    # Get handles based on priority
    label_handle_map = dict(zip(labels, handles))
    for label in priority_labels:
        if label in label_handle_map:
            ordered_handles.append(label_handle_map[label])
            ordered_labels.append(label)

    ax.legend(ordered_handles, ordered_labels, loc='lower left', fontsize='small') # Move legend
    ax.grid(True)


# --- Modified Data Loading and Processing Function ---
def run_hull_on_dataset_monthly(filepath: str, months: list[str]):
    """Loads dataset, computes country and overall hulls for months, plots them."""

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
    required_cols = ['observationdate', 'latitude', 'longitude', 'country']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: CSV missing required columns: {required_cols}.")
        missing = [col for col in required_cols if col not in df.columns]
        print(f"Missing: {missing}")
        return

    try:
        df['observationdate'] = pd.to_datetime(df['observationdate'], format='%m/%d/%Y')
    except ValueError as e:
        print(f"Error parsing dates: {e}. Ensure format is MM/DD/YYYY.")
        return

    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df.dropna(subset=['latitude', 'longitude', 'country'], inplace=True)
    df = df[df['country'].str.strip() != '']

    df['year_month'] = df['observationdate'].dt.strftime('%Y-%m')

    # --- Plotting ---
    fig, axes = plt.subplots(1, len(months), figsize=(24, 8))
    if len(months) == 1:
        axes = [axes]

    for i, month_str in enumerate(months):
        ax = axes[i]
        month_data = df[df['year_month'] == month_str].copy()

        print(f"\n--- Processing Month {month_str} ---")

        if month_data.empty:
            print(f"No data found for month {month_str}.")
            plot_hulls_multilevel(ax, [], [], {}, f"Month {month_str}")
            continue

        # 2. Get ALL unique points with country info
        points_info_df = month_data[['longitude', 'latitude', 'country']].drop_duplicates()
        all_points_info = [tuple(x) for x in points_info_df.values] # (lon, lat, country)

        # Get unique coordinates for overall hull computation
        unique_coords_overall_df = month_data[['longitude', 'latitude']].drop_duplicates()
        unique_coords_overall = [tuple(x) for x in unique_coords_overall_df.values] # (lon, lat)

        print(f"Found {len(all_points_info)} unique location/country entries.")
        print(f"Found {len(unique_coords_overall)} unique coordinate pairs overall.")

        plot_title = f"Geographic Hulls for {month_str}"

        # --- Calculate Country-Specific Hulls ---
        country_hulls: Dict[str, List[Tuple[float, float]]] = {}
        grouped_by_country = month_data.groupby('country')

        print("Calculating country-specific hulls:")
        for country, group in grouped_by_country:
            country_coords_df = group[['longitude', 'latitude']].drop_duplicates()
            country_coords = [tuple(x) for x in country_coords_df.values]
            if len(country_coords) >= 1: # Need at least one point to store
                 # Compute hull even for 1 or 2 points (returns the points)
                 country_hull_points = convex_hull.compute_hull_dvcq(list(country_coords))
                 if country_hull_points: # Store if hull computation successful
                     country_hulls[country] = country_hull_points
                     # Only print if it's a polygon hull for brevity
                     if len(country_hull_points) >= 3:
                          print(f"  - {country}: {len(country_hull_points)} vertices")

        # --- Calculate Overall Hull ---
        overall_hull_coords: List[Tuple[float, float]] = []
        overall_hull_points_info: List[Tuple[float, float, str]] = [] # For labeling vertices

        if len(unique_coords_overall) >= 3:
            overall_hull_coords = convex_hull.compute_hull_dvcq(list(unique_coords_overall)) # Pass a copy
            print(f"\nOverall hull contains {len(overall_hull_coords)} vertices.")

            # Find country names for overall hull vertices
            overall_hull_coords_set = set(overall_hull_coords)
            coord_to_country_map = {}
            # Build map preferring non-empty names first if duplicates exist
            for lon, lat, c_name in all_points_info:
                 if (lon, lat) not in coord_to_country_map or not coord_to_country_map.get((lon, lat)):
                     coord_to_country_map[(lon, lat)] = c_name

            for h_lon, h_lat in overall_hull_coords:
                country_name = coord_to_country_map.get((h_lon, h_lat), "Unknown")
                overall_hull_points_info.append((h_lon, h_lat, country_name))
        else:
            print("Not enough unique overall points to compute overall hull.")
            overall_hull_points_info = [] # Ensure it's empty for plotting


        # --- Plot the results ---
        plot_hulls_multilevel(ax, all_points_info, overall_hull_points_info, country_hulls, plot_title)

    fig.suptitle("Overall & Country Convex Hulls of COVID-19 Locations (Monthly)", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    save_path = "covid_multi_hull_monthly_plots.png" # New filename
    try:
        plt.savefig(save_path)
        print(f"\nPlot saved successfully as '{save_path}'")
    except Exception as e:
        print(f"\nError saving plot: {e}")

    plt.show()

if __name__ == "__main__":
    csv_file = "Covid_19_Countrywise_timeseries.csv"
    months_to_plot = ["2020-01", "2020-02", "2020-03"]
    run_hull_on_dataset_monthly(csv_file, months_to_plot)