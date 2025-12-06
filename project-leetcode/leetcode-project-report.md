# Project Leetcode

## Baseline 

### Baseline Problem 1

#### Problem Information

Problem Name: *102. Binary Tree Level Order Traversal*

[Submission Link](https://leetcode.com/problems/binary-tree-level-order-traversal/submissions/1847972188/)

![102-Binary-Tree-Level-Order-Traversal.png](102-Binary-Tree-Level-Order-Traversal.png)

#### Time Complexity

```python
class Solution:
    def levelOrder(self, root) -> List[List[int]]:
        output = []                                  # O(1) Constant
        count = TreeNode                             # O(1) unused variable
        queue = deque([root])                        # O(1) initialize queue with root
        while queue:                                 
            level_nodes = []                         # O(1) new list for current level
            level_size = len(queue)                  # O(1) check current width
            for _ in range(level_size):              # O(n) time n time
                curr = queue.popleft()               # O(1) - Deque pop is constant time
                if curr is not None:                 # O(1) - Check
                    level_nodes.append(curr.val)     # O(1) - Append to list
                    if curr.left:                    # O(1) - Check child
                        queue.append(curr.left)      # O(1) - Add to queue
                    if curr.right:                   # O(1) - Check child
                        queue.append(curr.right)     # O(1) - Add to queue
            if len(level_nodes) == 0:                # O(1) - Edge case check (e.g., root is None)
                break                                # O(1) - Exit
            else:                                    #
                output.append(level_nodes)           # O(1) - Add level list to output
        return output                                # O(1) - Return result
```

*Fill me in*

#### Space Complexity

```python
class Solution:
    def levelOrder(self, root) -> List[List[int]]:
        output = []                                  # O(1) Constant
        count = TreeNode                             # O(1) unused variable
        queue = deque([root])                        # O(1) initialize queue with root
        while queue:                                 
            level_nodes = []                         # O(1) new list for current level
            level_size = len(queue)                  # O(1) check current width
            for _ in range(level_size):              # O(n) time n time
                curr = queue.popleft()               # O(1) - Deque pop is constant time
                if curr is not None:                 # O(1) - Check
                    level_nodes.append(curr.val)     # O(1) - Append to list
                    if curr.left:                    # O(1) - Check child
                        queue.append(curr.left)      # O(1) - Add to queue
                    if curr.right:                   # O(1) - Check child
                        queue.append(curr.right)     # O(1) - Add to queue
            if len(level_nodes) == 0:                # O(1) - Edge case check (e.g., root is None)
                break                                # O(1) - Exit
            else:                                    #
                output.append(level_nodes)           # O(1) - Add level list to output
        return output                                # O(1) - Return result
```

*Fill me in*

----

### Baseline Problem 2

#### Problem Information

Problem Name: *547. Number of Provinces*

[Submission Link](https://leetcode.com/problems/number-of-provinces/submissions/1847985668/)

![547-Number-of-Provinces.png](547-Number-of-Provinces.png)

#### Time Complexity

```python
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        connections = set()
        visited = set()
        provinces = 0
        for i in range(len(isConnected)):
            if i not in visited:
                provinces += 1
                visited.add(i)
                stack = [i]
                while stack:
                    curr = stack.pop()
                    for j in range(len(isConnected)):
                        if isConnected[curr][j] == 1 and j not in visited:
                            visited.add(j)
                            stack.append(j)
        return provinces
```

*Fill me in*

#### Space Complexity

```python
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        connections = set()
        visited = set()
        provinces = 0
        for i in range(len(isConnected)):
            if i not in visited:
                provinces += 1
                visited.add(i)
                stack = [i]
                while stack:
                    curr = stack.pop()
                    for j in range(len(isConnected)):
                        if isConnected[curr][j] == 1 and j not in visited:
                            visited.add(j)
                            stack.append(j)
        return provinces
```

*Fill me in*

----

### Baseline Problem 3

#### Problem Information

Problem Name: *120. Triangle*

[Submission Link](https://leetcode.com/problems/triangle/submissions/1847991928/)

![120-Triangles.png](120-Triangles.png)

#### Time Complexity

```python
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        for row in range(1, len(triangle)):
            for col in range(len(triangle[row])):
                if col == 0:
                    triangle[row][col] += triangle[row-1][col]
                elif col == len(triangle[row]) - 1:
                    triangle[row][col] += triangle[row-1][col-1]
                else:
                    triangle[row][col] += min(triangle[row-1][col-1], triangle[row-1][col])
        return min(triangle[-1])  
```

*Fill me in*

#### Space Complexity

```python
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        for row in range(1, len(triangle)):
            for col in range(len(triangle[row])):
                if col == 0:
                    triangle[row][col] += triangle[row-1][col]
                elif col == len(triangle[row]) - 1:
                    triangle[row][col] += triangle[row-1][col-1]
                else:
                    triangle[row][col] += min(triangle[row-1][col-1], triangle[row-1][col])
        return min(triangle[-1])  
```

*Fill me in*

----


## Core

### Core Problem 1

#### Problem Information

Problem Name: *279. Perfect Squares*

[Submission Link](https://leetcode.com/problems/perfect-squares/submissions/1848007048/)

![279-perfect-squares.png](279-perfect-squares.png)

#### Time Complexity

```python
class Solution:
    def numSquares(self, n: int) -> int:
        squares = []
        i = 1
        while i * i <= n:
            squares.append(i * i)
            i += 1
        queue = deque([(n, 0)]) 
        visited = {n}
        while queue:
            curr, step = queue.popleft()
            
            for sq in squares:
                remainder = curr - sq
                if remainder == 0:
                    return step + 1
                
                if remainder > 0 and remainder not in visited:
                    visited.add(remainder)
                    queue.append((remainder, step + 1))
                    
        return n
            

                
```
*Fill me in*

#### Space Complexity

```python
class Solution:
    def numSquares(self, n: int) -> int:
        squares = []
        i = 1
        while i * i <= n:
            squares.append(i * i)
            i += 1
        queue = deque([(n, 0)]) 
        visited = {n}
        while queue:
            curr, step = queue.popleft()
            
            for sq in squares:
                remainder = curr - sq
                if remainder == 0:
                    return step + 1
                
                if remainder > 0 and remainder not in visited:
                    visited.add(remainder)
                    queue.append((remainder, step + 1))
                    
        return n
            

                
```

*Fill me in*

----

### Core Problem 2

#### Problem Information

Problem Name: *1042. Flower Planting With No Adjacent*

[Submission Link](https://leetcode.com/problems/flower-planting-with-no-adjacent/submissions/1848054416/)

![1042-Flower-Planting-With-No-Adjacent.png](1042-Flower-Planting-With-No-Adjacent.png)

#### Time Complexity

*Fill me in*

#### Space Complexity

*Fill me in*

----

### Core Problem 3

#### Problem Information

Problem Name: *fill me in*

[Submission Link]()

![Screenshot of successful submission]()

#### Time Complexity

*Fill me in*

#### Space Complexity

*Fill me in*

----

## Stretch 1

### Stretch 1 Problem 1

#### Problem Information

Problem Name: *fill me in*

[Submission Link]()

![Screenshot of successful submission]()

#### Time Complexity

*Fill me in*

#### Space Complexity

*Fill me in*

----

## Stretch 2

### Stretch 2 Problem 1

#### Problem Information

Problem Name: *fill me in*

[Submission Link]()

![Screenshot of successful submission]()

#### Time Complexity

*Fill me in*

#### Space Complexity

*Fill me in*

## Project Review

*Fill me in*
