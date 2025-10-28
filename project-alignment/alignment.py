
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
    banded = (banded_width != -1)

    if banded and abs(len(seq1) - len(seq2)) > banded_width:
        return float('inf'), None, None

    matrix: list[list[tuple[float, str]]]
    if banded:
        bandwidth = 2 * banded_width + 1
        matrix = [[(float('inf'), "NULL") for _ in range(bandwidth)] for _ in range(row)]

        def get_val(row_i, col_j) -> tuple[float, str]:
            j_band = col_j - row_i + banded_width
            if row_i < 0 or col_j < 0 or j_band < 0 or j_band >= bandwidth:
                return float('inf'), "NULL"
            return matrix[row_i][j_band]

        def set_val(row_i, col_j, val: tuple[float, str]):
            j_band = col_j - row_i + banded_width
            if 0 <= row_i < row and 0 <= j_band < bandwidth:
                matrix[row_i][j_band] = val

    else:
        matrix = [[(float('inf'), "NULL") for _ in range(col)] for _ in range(row)]

        def get_val(row_i, col_j) -> tuple[float, str]:
            if row_i < 0 or col_j < 0:
                return float('inf'), "NULL"
            if row_i >= row or col_j >= col:
                return float('inf'), "NULL"
            return matrix[row_i][col_j]

        def set_val(row_i, col_j, val: tuple[float, str]):
            matrix[row_i][col_j] = val

    set_val(0, 0, (0, "START"))

    for i in range(1, row):
        if not banded or i <= banded_width:
            score = get_val(i - 1, 0)[0] + indel_penalty
            if i > 1:
                score += gap_open_penalty
            set_val(i, 0, (score, "UP"))

    for j in range(1, col):
        if not banded or j <= banded_width:
            score = get_val(0, j - 1)[0] + indel_penalty
            if j > 1:
                score += gap_open_penalty
            set_val(0, j, (score, "LEFT"))

    for i in range(1, row):
        start = 1
        end = col
        if banded:
            start = max(1, i - banded_width)
            end = min(col, i + banded_width + 1)

        for j in range(start, end):
            diag_score, _ = get_val(i - 1, j - 1)
            up_score, up_dir = get_val(i - 1, j)
            left_score, left_dir = get_val(i, j - 1)

            if seq2[i - 1] == seq1[j - 1]:
                diag_cost = diag_score + match_award
            else:
                diag_cost = diag_score + sub_penalty

            if up_dir == "UP":
                up_cost = up_score + indel_penalty
            else:
                up_cost = up_score + indel_penalty + gap_open_penalty

            if left_dir == "LEFT":
                left_cost = left_score + indel_penalty
            else:
                left_cost = left_score + indel_penalty + gap_open_penalty

            min_cost = min(diag_cost, up_cost, left_cost)

            if min_cost == diag_cost:
                set_val(i, j, (min_cost, "DIAG"))
            elif min_cost == up_cost:
                set_val(i, j, (min_cost, "UP"))
            else:
                set_val(i, j, (min_cost, "LEFT"))

    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = row - 1, col - 1

    final_score, _ = get_val(i, j)

    if final_score == float('inf'):
        return float('inf'), None, None

    while i > 0 or j > 0:
        score, direction = get_val(i, j)

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
        elif direction == "START":
            break
        elif direction == "NULL":
            break

    return final_score, aligned_seq1, aligned_seq2