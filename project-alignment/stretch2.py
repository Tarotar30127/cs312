import sys

# Set a very low number for negative infinity
NEG_INF = -sys.maxsize


def align_affine(seq1: str, seq2: str, match: int, mismatch: int, gap_open: int, gap_extend: int):
    """
    Performs a global alignment with affine gap penalties (Gotoh algorithm).

    Args:
        seq1: The first sequence string.
        seq2: The second sequence string.
        match: Score for a match.
        mismatch: Penalty for a mismatch.
        gap_open: Penalty to open a new gap. (e.g., -10)
        gap_extend: Penalty to extend an existing gap. (e.g., -2)

    Returns:
        A tuple: (final_score, aligned_seq1, aligned_seq2)
    """
    m = len(seq1)
    n = len(seq2)

    # Initialize the three dynamic programming tables
    # M: Score ending with a match/mismatch
    # X: Score ending with a gap in seq2 (deletion from seq1)
    # Y: Score ending with a gap in seq1 (insertion into seq2)
    M = [[0] * (n + 1) for _ in range(m + 1)]
    X = [[NEG_INF] * (n + 1) for _ in range(m + 1)]
    Y = [[NEG_INF] * (n + 1) for _ in range(m + 1)]

    # --- 1. Fill DP Tables ---

    # Initialize the origin
    M[0][0] = 0
    # Initialize first row (gaps in seq1)
    for j in range(1, n + 1):
        Y[0][j] = gap_open + (j - 1) * gap_extend
    # Initialize first column (gaps in seq2)
    for i in range(1, m + 1):
        X[i][0] = gap_open + (i - 1) * gap_extend

    # Fill the rest of the tables
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Score for a match or mismatch
            s = match if seq1[i - 1] == seq2[j - 1] else mismatch

            # M[i][j] can come from M, X, or Y in the (i-1, j-1) cell
            M[i][j] = s + max(M[i - 1][j - 1], X[i - 1][j - 1], Y[i - 1][j - 1])

            # X[i][j] (gap in seq2) can come from opening a new gap from M, or extending an existing gap from X
            X[i][j] = max(M[i - 1][j] + gap_open,
                          X[i - 1][j] + gap_extend)

            # Y[i][j] (gap in seq1) can come from opening a new gap from M, or extending an existing gap from Y
            Y[i][j] = max(M[i][j - 1] + gap_open,
                          Y[i][j - 1] + gap_extend)

    # --- 2. Find Final Score ---
    # The final score is the max of the three tables at the bottom-right corner
    final_score = max(M[m][n], X[m][n], Y[m][n])

    # --- 3. Traceback ---
    align1 = ""
    align2 = ""
    i, j = m, n

    # Start in the table that gave the max score
    if final_score == M[m][n]:
        current_table = 'M'
    elif final_score == X[m][n]:
        current_table = 'X'
    else:
        current_table = 'Y'

    while i > 0 or j > 0:
        if current_table == 'M':
            # Came from a match/mismatch
            s = match if seq1[i - 1] == seq2[j - 1] else mismatch
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2

            # Check which table we came from
            if M[i][j] == M[i - 1][j - 1] + s:
                current_table = 'M'
            elif M[i][j] == X[i - 1][j - 1] + s:
                current_table = 'X'
            else:
                current_table = 'Y'
            i -= 1
            j -= 1

        elif current_table == 'X':
            # Came from a gap in seq2 (deletion)
            align1 = seq1[i - 1] + align1
            align2 = "-" + align2

            # Check if we opened or extended this gap
            if X[i][j] == X[i - 1][j] + gap_extend:
                current_table = 'X'
            else:  # X[i][j] == M[i-1][j] + gap_open
                current_table = 'M'
            i -= 1

        else:  # current_table == 'Y'
            # Came from a gap in seq1 (insertion)
            align1 = "-" + align1
            align2 = seq2[j - 1] + align2

            # Check if we opened or extended this gap
            if Y[i][j] == Y[i][j - 1] + gap_extend:
                current_table = 'Y'
            else:  # Y[i][j] == M[i][j-1] + gap_open
                current_table = 'M'
            j -= 1

    return final_score, align1, align2


# --- Main execution ---

# Hard-code the sequences
S1 = "ATGGCGTGTTTGTTTTTTAT"
S2 = "ATGGCGTTTTTGAT"

# --- Scoring Parameters ---
MATCH_SCORE = 5  # Score for a perfect match
MISMATCH_PENALTY = -4  # Penalty for a mismatch

print(f"Aligning S1: {S1}")
print(f"Aligning S2: {S2}")
print("-" * 30)

# --- Case 1: Affine Gap Penalty (Your "gap-aware" algorithm) ---
# High cost to open a gap, low cost to extend it.
# This encourages grouping gaps together.
OPEN_1 = -10
EXTEND_1 = -2

print(f"--- Case 1: Affine Gap (Open={OPEN_1}, Extend={EXTEND_1}) ---")
score1, align1_1, align2_1 = align_affine(S1, S2, MATCH_SCORE, MISMATCH_PENALTY, OPEN_1, EXTEND_1)
print(f"Score: {score1}")
print(align1_1)
print(align2_1)
print("\n")

# --- Case 2: Linear Gap Penalty (Your "original" algorithm) ---
# We simulate this by making the open and extend penalties identical.
# The algorithm has no preference for grouping gaps.
OPEN_2 = -8
EXTEND_2 = -8

print(f"--- Case 2: Linear Gap (Simulated) (Open={OPEN_2}, Extend={EXTEND_2}) ---")
score2, align1_2, align2_2 = align_affine(S1, S2, MATCH_SCORE, MISMATCH_PENALTY, OPEN_2, EXTEND_2)
print(f"Score: {score2}")
print(align1_2)
print(align2_2)