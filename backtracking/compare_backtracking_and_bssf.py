import math
import random
import time
from utils import Timer, generate_network
from tsp_solve_backtracking import backtracking, backtracking_bssf

def main():
    # --- Configuration ---
    # We need N to be large enough that regular backtracking can't finish,
    # but small enough that BSSF can make progress.
    N_CITIES = 15       # 15-16 is a good number. 20 is too slow for both.
    TIME_LIMIT_SEC = 60  # A short time limit to show the difference
    GRAPH_SEED = 42     # Use a fixed seed for reproducible results
    # ---------------------
    
    print("--- TSP Backtracking Comparison ---")
    print(f"Settings: N={N_CITIES}, Time Limit={TIME_LIMIT_SEC}s, Seed={GRAPH_SEED}")
    print("Generating graph...")
    locations, edges = generate_network(
        N_CITIES,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=GRAPH_SEED,
    )
    
    # --- Run 1: Regular Backtracking ---
    print("\nRunning 'Regular Backtracking'...")
    timer_reg = Timer(TIME_LIMIT_SEC)
    solutions_reg = backtracking(edges, timer_reg)
    
    if not solutions_reg:
        best_score_reg = math.inf
        print("  ...Timed out before finding any solution.")
    else:
        best_score_reg = solutions_reg[-1].score
        print(f"  ...Found {len(solutions_reg)} solutions.")
        print(f"  Best score found: {best_score_reg}")
        
    # --- Run 2: BSSF Backtracking ---
    print("\nRunning 'BSSF Backtracking'...")
    timer_bssf = Timer(TIME_LIMIT_SEC)
    solutions_bssf = backtracking_bssf(edges, timer_bssf)
    
    if not solutions_bssf:
        best_score_bssf = math.inf
        print("  ...Timed out before finding any solution (or greedy failed).")
    else:
        # The first solution is the greedy one, the last is the best one found
        greedy_score = solutions_bssf[0].score
        best_score_bssf = solutions_bssf[-1].score
        print(f"  ...Initial greedy BSSF: {greedy_score}")
        print(f"  ...Found {len(solutions_bssf)} improving solutions.")
        print(f"  Best score found: {best_score_bssf}")

    # --- Conclusion ---
    print("\n--- FINAL RESULTS ---")
    print(f"Regular Backtracking Best Score: {best_score_reg}")
    print(f"BSSF Backtracking Best Score:    {best_score_bssf}")
    
    if best_score_bssf < best_score_reg:
        print("\nSUCCESS: BSSF Backtracking found a better solution in the same amount of time.")
    elif best_score_bssf == best_score_reg:
        print("\nINTERESTING: Both algorithms found the same solution.")
    else:
        print("\nFAILURE: Regular Backtracking found a better solution (this may indicate a bug).")

if __name__ == "__main__":
    main()