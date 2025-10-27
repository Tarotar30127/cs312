import numpy as np


def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap_open_penalty=0,
        gap='-',
) -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap_open_penalty: how much it costs to open a gap. If 0, there is no gap_open penalty
        :param gap: the character to use to represent gaps in the alignment strings
    """
    penalty: dict = {"sub": 0, "match": 0, "insert_delete": 0}
    row = len(seq2) + 1
    col = len(seq1) + 1

    matrix = np.empty((row, col), dtype=object)
    matrix[0, 0] = (0, "START")

    for i in range(1, row):
        score = matrix[i - 1, 0][0] + indel_penalty
        matrix[i, 0] = (score, "UP")

    for j in range(1, col):
        score = matrix[0, j - 1][0] + indel_penalty
        matrix[0, j] = (score, "LEFT")

    for i in range(1, row):
        for j in range(1, col):
            diag_score, direction_string = matrix[i - 1, j - 1]
            up_score, direction_string = matrix[i - 1, j]
            left_score, direction_string = matrix[i, j - 1]
            if seq2[i - 1] == seq1[j - 1]:
                diag_cost = diag_score + match_award
            else:
                diag_cost = diag_score + sub_penalty

            up_cost = up_score + indel_penalty
            left_cost = left_score + indel_penalty
            min_cost = min(diag_cost, up_cost, left_cost)

            if min_cost == diag_cost:
                matrix[i, j] = (min_cost, "DIAG")
            elif min_cost == up_cost:
                matrix[i, j] = (min_cost, "UP")
            else:
                matrix[i, j] = (min_cost, "LEFT")

    aligned_seq1 = ""
    aligned_seq2 = ""

    i, j = row - 1, col - 1

    final_score, direction_string = matrix[i, j]

    while i > 0 or j > 0:
        direction_string, direction = matrix[i, j]

        if direction == "DIAG":
            aligned_seq1 = seq1[j - 1] + aligned_seq1
            aligned_seq2 = seq2[i - 1] + aligned_seq2

            if seq2[i - 1] == seq1[j - 1]:
                penalty["match"] += 1
            else:
                penalty["sub"] += 1

            i -= 1
            j -= 1

        elif direction == "UP":
            aligned_seq1 = gap + aligned_seq1
            aligned_seq2 = seq2[i - 1] + aligned_seq2
            penalty["insert_delete"] += 1
            i -= 1

        elif direction == "LEFT":
            aligned_seq1 = seq1[j - 1] + aligned_seq1
            aligned_seq2 = gap + aligned_seq2
            penalty["insert_delete"] += 1
            j -= 1

    return final_score, aligned_seq1, aligned_seq2
