import matplotlib.pyplot as plt
import pandas as pd
import copy
import numpy as np

# Import your project modules
from tsp_core import generate_network, Timer
from tsp_solve import branch_and_bound, branch_and_bound_smart


def run_comparison():
    # --- CONFIGURATION ---
    NUM_SEEDS = 20
    START_SEED = 100  # Starting seed number
    N_CITIES = 15  # N=15 is a good balance (Standard B&B finishes, but works hard)
    TIMEOUT = 60  # Seconds per solver

    results = []

    print(f"{'=' * 60}")
    print(f"Running Comparison on {NUM_SEEDS} seeds (N={N_CITIES})")
    print(f"{'=' * 60}")

    for i in range(NUM_SEEDS):
        seed = START_SEED + i

        # 1. Generate Problem
        # Use deepcopy to ensure both solvers get the exact same fresh list
        locations, edges = generate_network(N_CITIES, seed=seed)

        # 2. Run Standard Branch and Bound
        timer_std = Timer(TIMEOUT)
        try:
            stats_std = branch_and_bound(copy.deepcopy(edges), timer_std)
            score_std = stats_std[-1].score if stats_std else float('inf')
            time_std = stats_std[-1].time if stats_std else TIMEOUT
        except Exception as e:
            score_std = float('inf')
            time_std = TIMEOUT
            print(f"Seed {seed}: Standard Failed ({e})")

        # 3. Run Smart Branch and Bound
        timer_smart = Timer(TIMEOUT)
        try:
            stats_smart = branch_and_bound_smart(copy.deepcopy(edges), timer_smart)
            score_smart = stats_smart[-1].score if stats_smart else float('inf')
            time_smart = stats_smart[-1].time if stats_smart else TIMEOUT
        except Exception as e:
            score_smart = float('inf')
            time_smart = TIMEOUT
            print(f"Seed {seed}: Smart Failed ({e})")

        # 4. Calculate Improvement
        # (Standard - Smart) / Standard
        if score_std > 0 and score_std != float('inf'):
            improvement = (score_std - score_smart)
            pct_improvement = (improvement / score_std) * 100
        else:
            pct_improvement = 0.0

        print(
            f"Seed {seed}: Std={score_std:.2f} ({time_std:.2f}s) vs Smart={score_smart:.2f} ({time_smart:.2f}s) -> Diff: {pct_improvement:.1f}%")

        results.append({
            "Seed": seed,
            "Standard Cost": score_std,
            "Smart Cost": score_smart,
            "Standard Time": time_std,
            "Smart Time": time_smart,
            "% Improvement": pct_improvement
        })

    # --- DATAFRAME & TABLE ---
    df = pd.DataFrame(results)

    print("\n" + "=" * 80)
    print("FINAL COMPARISON TABLE")
    print("=" * 80)
    print(df.to_string(index=False, float_format="%.2f"))

    # Calculate Averages
    avg_std_score = df["Standard Cost"].mean()
    avg_smart_score = df["Smart Cost"].mean()
    avg_improvement = df["% Improvement"].mean()

    print("-" * 80)
    print(
        f"AVERAGES | Std Cost: {avg_std_score:.2f} | Smart Cost: {avg_smart_score:.2f} | Improvement: {avg_improvement:.2f}%")
    print("-" * 80)

    # --- PLOTTING ---
    fig, axes = plt.subplots(2, 1, figsize=(10, 12))

    # Plot 1: Cost Comparison
    x = np.arange(len(df["Seed"]))
    width = 0.35

    axes[0].bar(x - width / 2, df["Standard Cost"], width, label='Standard B&B', color='skyblue')
    axes[0].bar(x + width / 2, df["Smart Cost"], width, label='Smart B&B', color='orange')

    axes[0].set_ylabel('Tour Cost (Lower is Better)')
    axes[0].set_title(f'Solution Quality Comparison (N={N_CITIES})')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(df["Seed"])
    axes[0].legend()
    axes[0].grid(axis='y', linestyle='--', alpha=0.5)

    # Plot 2: Time Comparison (Optional but useful)
    axes[1].plot(df["Seed"].astype(str), df["Standard Time"], marker='o', label='Standard Time', linestyle='--')
    axes[1].plot(df["Seed"].astype(str), df["Smart Time"], marker='o', label='Smart Time')

    axes[1].set_ylabel('Time (Seconds)')
    axes[1].set_xlabel('Seed')
    axes[1].set_title('Execution Time Comparison')
    axes[1].legend()
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('comparison_report.png')
    print("\nPlot saved as 'comparison_report.png'")
    plt.show()


if __name__ == "__main__":
    run_comparison()