# Project Report - Alignment

## Baseline

### Design Experience

*For my baseline design experience, I talked to Kyle Mak and Collin Verbanatz about Unrestricted Alignment algorithm by 
walking through a problem by hand. We used the example from the slides to walk through the base cases of "THARS" vs 
"OTHER". I will create 2 arrays for and loop through both and then create a dictionary to control the cost values. For 
dynamic programming will use more data structure increasing the space complexity of the function.*

### Theoretical Analysis - Unrestricted Alignment

#### Time 

```python
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
    penalty: dict = {"sub": 0, "match": 0, "insert_delete": 0}                      # O(1) set up dict
    row = len(seq2) + 1                                                             # O(1) set row varible 
    col = len(seq1) + 1                                                             # O(1) set col varible 
    matrix = np.empty((row, col), dtype=object)                                     # O(m*n) creating a matrix base on the col and row
    matrix[0, 0] = (0, "START")                                                     # O(1) setting the start
    for i in range(1, row):                                                         # O(m) runs m times
        score = matrix[i - 1, 0][0] + indel_penalty                                 # O(1) set matrix
        matrix[i, 0] = (score, "UP")                                                # O(1) set matrix
    for j in range(1, col):                                                         # O(n) runs n times
        score = matrix[0, j - 1][0] + indel_penalty                                 # O(1) create varible
        matrix[0, j] = (score, "LEFT")                                              # O(1) set constant

    for i in range(1, row):                                                         # O(m) runs m times
        for j in range(1, col):                                                     # O(n) runs n times 
            diag_score, direction_string = matrix[i - 1, j - 1]                     # O(1) calling location in matrix
            up_score, direction_string = matrix[i - 1, j]                           # O(1) calling up
            left_score, direction_string = matrix[i, j - 1]                         # O(1) calling score and up or left
            if seq2[i - 1] == seq1[j - 1]:                                          # O(1) comparing constants
                diag_cost = diag_score + match_award                                # O(1) set varible
            else:                                                                   # O(1) comparing constants
                diag_cost = diag_score + sub_penalty                                # O(1) set varible

            up_cost = up_score + indel_penalty                                      # O(1) set varible
            left_cost = left_score + indel_penalty                                  # O(1) set varible
            min_cost = min(diag_cost, up_cost, left_cost)                           # O(1) find the min of 3 variables
            if min_cost == diag_cost:                                               # O(1) compare 2 constants
                matrix[i, j] = (min_cost, "DIAG")                                   # O(1) set a variable 
            elif min_cost == up_cost:                                               # O(1) compare 2 constants
                matrix[i, j] = (min_cost, "UP")                                     # O(1) set a variable 
            else:                                                                   # O(1) else 
                matrix[i, j] = (min_cost, "LEFT")                                   # O(1) set a variable 

    aligned_seq1 = ""                                                               # O(1) create an empty string
    aligned_seq2 = ""                                                               # O(1) create an empty string

    i, j = row - 1, col - 1                                                         # O(1) setting the new row and col

    final_score, _ = matrix[i, j]                                                   # O(1) call a constant
    while i > 0 or j > 0:                                                           # O(m+n) runs m and n times
        direction_string, direction = matrix[i, j]                                  # O(1) set a variable 
        if direction == "DIAG":                                                     # O(1) compare constants
            aligned_seq1 = seq1[j - 1] + aligned_seq1                               # O(1) simple addition and constant
            aligned_seq2 = seq2[i - 1] + aligned_seq2                               # O(1) add to the string
            if seq2[i - 1] == seq1[j - 1]:                                          # O(1) compare constant
                penalty["match"] += 1                                               # O(1) add to the dictionary
            else:                                                                   # O(1) else
                penalty["sub"] += 1                                                 # O(1) add to the dictionary
            i -= 1                                                                  # O(1) simple subtraction
            j -= 1                                                                  # O(1) simple subtraction
        elif direction == "UP":                                                     # O(1) compare constants
            aligned_seq1 = gap + aligned_seq1                                       # O(1) add to string
            aligned_seq2 = seq2[i - 1] + aligned_seq2                               # O(1) add to string
            penalty["insert_delete"] += 1                                           # O(1) add to the dictionary
            i -= 1                                                                  # O(1) simple subtraction
        elif direction == "LEFT":                                                   # O(1) compare constants
            aligned_seq1 = seq1[j - 1] + aligned_seq1                               # O(1) add to string
            aligned_seq2 = gap + aligned_seq2                                       # O(1) add to string
            penalty["insert_delete"] += 1                                           # O(1) add to the dictionary
            j -= 1                                                                  # O(1) simple subtraction
    return final_score, aligned_seq1, aligned_seq2                                  # O(1)
```

*I found the total time complexity to be O(m*n) because I have 1 for loop what runs n and another for loop that 
runs m times then I have my nested loop which is O(m*n) then my last while loop is m+n because it goes through both.*

#### Space

```python
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
    penalty: dict = {"sub": 0, "match": 0, "insert_delete": 0}                      # O(1) small dict constant space 
    row = len(seq2) + 1                                                             # O(1) constant space 
    col = len(seq1) + 1                                                             # O(1) constant integer
    matrix = np.empty((row, col), dtype=object)                                     # O(m*n) grows to m*n
    matrix[0, 0] = (0, "START")                                                     # O(1) edit tuple 
    for i in range(1, row):                                                         # O(1) loop constant
        score = matrix[i - 1, 0][0] + indel_penalty                                 # O(1) set variable
        matrix[i, 0] = (score, "UP")                                                # O(1) set variable
    for j in range(1, col):                                                         # O(1) loop constant
        score = matrix[0, j - 1][0] + indel_penalty                                 # O(1) set variable 
        matrix[0, j] = (score, "LEFT")                                              # O(1) set tuple variable
    for i in range(1, row):                                                         # O(1) loop constant
        for j in range(1, col):                                                     # O(1) loop constant
            diag_score, _ = matrix[i - 1, j - 1]                                    # O(1) set variable
            up_score, _ = matrix[i - 1, j]                                          # O(1) set variable
            left_score, _ = matrix[i, j - 1]                                        # O(1) set variable
            if seq2[i - 1] == seq1[j - 1]:                                          # O(1) compare constant
                diag_cost = diag_score + match_award                                # O(1) set variable
            else:                                                                   # O(1) else
                diag_cost = diag_score + sub_penalty                                # O(1) set variable
            up_cost = up_score + indel_penalty                                      # O(1) set variable
            left_cost = left_score + indel_penalty                                  # O(1) set variable
            min_cost = min(diag_cost, up_cost, left_cost)                           # O(1) set variable
            if min_cost == diag_cost:                                               # O(1) compare constant
                matrix[i, j] = (min_cost, "DIAG")                                   # O(1) set tuple 
            elif min_cost == up_cost:                                               # O(1) compare constant
                matrix[i, j] = (min_cost, "UP")                                     # O(1) set tuple 
            else:                                                                   # O(1) else
                matrix[i, j] = (min_cost, "LEFT")                                   # O(1) set tuple 
    aligned_seq1 = ""                                                               # O(1) empty string
    aligned_seq2 = ""                                                               # O(1) empty string
    i, j = row - 1, col - 1                                                         # O(1) set variables
    final_score, _ = matrix[i, j]                                                   # O(1) set variable
    while i > 0 or j > 0:                                                           # O(1) loop constant overhead
        _, direction = matrix[i, j]                                                 # O(1) call variable
        if direction == "DIAG":                                                     # O(1) compare variable 
            aligned_seq1 = seq1[j - 1] + aligned_seq1                               # O(n+m) max it can grow n+m length
            aligned_seq2 = seq2[i - 1] + aligned_seq2                               # O(n+m) max it can grow n+m length
            if seq2[i - 1] == seq1[j - 1]:                                          # O(1) compare constant
                penalty["match"] += 1                                               # O(1) add to dictionary
            else:                                                                   # O(1) next
                penalty["sub"] += 1                                                 # O(1) add to dictionary
            i -= 1                                                                  # O(1) subtraction
            j -= 1                                                                  # O(1) subtraction

        elif direction == "UP":                                                     # O(1) compare constant
            aligned_seq1 = gap + aligned_seq1                                       # O(n+m) max it can grow n+m length
            aligned_seq2 = seq2[i - 1] + aligned_seq2                               # O(n+m) max it can grow n+m length
            penalty["insert_delete"] += 1                                           # O(1) add to dictionary
            i -= 1                                                                  # O(1) subtraction

        elif direction == "LEFT":                                                   # O(1) compare constant
            aligned_seq1 = seq1[j - 1] + aligned_seq1                               # O(n+m) max it can grow n+m length
            aligned_seq2 = gap + aligned_seq2                                       # O(n+m) max it can grow n+m length
            penalty["insert_delete"] += 1                                           # O(1) add to dictionary
            j -= 1                                                                  # O(1) subtraction
            
    return final_score, aligned_seq1, aligned_seq2                                  # O(1) - Returns pointers to existing objects
```
*The total space is dominated by matrix (O(m*n)) because the matrix is m+1 times n+1 size.*

### Empirical Data - Unrestricted Alignment

| N    | time (ms) |
|------|-----------|
| 500  | 135       |
| 1000 | 465       |
| 1500 | 1045      |
| 2000 | 1946      |
| 2500 | 2954      |
| 3000 | 4296      |


### Comparison of Theoretical and Empirical Results - Unrestricted Alignment

- Theoretical order of growth: O(m*n)
- Empirical order of growth (if different from theoretical): 4.841313827920842e-07

![3d_baseline.png](3d_baseline.png)
![Baseline_anaylsis.png](Baseline_anaylsis.png)

*The theoretical model best fits the observed data for both graphs which means that there was no reason to find a empirical 
order of growth. The 2D plot confirms that runtime grows O(n*m) perfectly matching the theoretical O(n*m).
The 3D plot shows that the observed runtimes for all combinations of m and n follow the theoretical O(m*n) predicted.*

## Core

### Design Experience

*For my core design experience, I talked to Kyle Mak and Collin Verbanatz about the alignment banded algorithm and walked
the homework problem. The alignment algorithm computes the scores in a narrow diagonal strip of the matrix and assumes
the best alignment is close to the main diagonal. The alignment algorithm cuts the complexity by ignoring the cells that
are on the outside. A limitation is that is can fail to find the optimal alignment if it falls outside the strip. We talked 
about using a matrix and then restricting the columns.*


### Theoretical Analysis - Banded Alignment

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data - Banded Alignment

| N     | time (ms) |
|-------|-----------|
| 100   |           |
| 1000  |           |
| 5000  |           |
| 10000 |           |
| 15000 |           |
| 20000 |           |
| 25000 |           |
| 30000 |           |

### Comparison of Theoretical and Empirical Results - Banded Alignment

- Theoretical order of growth: 
- Empirical order of growth (if different from theoretical): 


![](fill-me-in.png)

*Fill me in*

### Relative Performance Of Unrestricted Alignment versus Banded Alignment

*Fill me in*


## Stretch 1

### Design Experience

*Fill me in*

### Code

```python
# Fill me in
```

### Alignment Scores

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Empirical Data - Using Affine Penalties

| N    | time (ms) |
|------|-----------|
| 500  |           |
| 1000 |           |
| 1500 |           |
| 2000 |           |
| 2500 |           |
| 3000 |           |

### Empirical Outcome Comparisons

*Fill me in*

### Alignment Outcome Comparisons

##### Sequences and Alignments

*Fill me in*

##### Chosen Parameters and Better Alignments Discussion

*Fill me in*

## Project Review

*Fill me in*
