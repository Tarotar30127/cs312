import math
import functools


# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point


def find_the_slope(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    if point2[0] == point1[0]:
        if point2[1] > point1[1]:
            return math.inf
        else:
            return -math.inf
    if point2[1] == point1[1]:
        return 0.0

    return (point2[1] - point1[1]) / (point2[0] - point1[0])


def merge(left_hull: list[tuple[float, float]], right_hull: list[tuple[float, float]]) -> list[tuple[float, float]]:
    left_point = max(left_hull, key=lambda p: p[0])
    right_point = min(right_hull, key=lambda p: p[0])
    left_index = left_hull.index(left_point)
    right_index = right_hull.index(right_point)
    len_left = len(left_hull)
    len_right = len(right_hull)

    while True:
        move_left = False
        move_right = False
        current_slope = find_the_slope(left_point, right_point)

        while True:
            next_left_index = (left_index + 1) % len_left
            next_left_point = left_hull[next_left_index]
            new_slope = find_the_slope(next_left_point, right_point)

            if new_slope > current_slope:
                left_point = next_left_point
                left_index = next_left_index
                current_slope = new_slope
                move_left = True
            else:
                break

        while True:
            next_right_index = (right_index - 1 + len_right) % len_right
            next_right_point = right_hull[next_right_index]

            new_slope = find_the_slope(left_point, next_right_point)

            if new_slope < current_slope:
                right_point = next_right_point
                right_index = next_right_index
                current_slope = new_slope
                move_right = True
            else:
                break

        if not move_left and not move_right:
            break

    upper_left = left_point
    upper_right = right_point

    left_point = max(left_hull, key=lambda p: p[0])
    right_point = min(right_hull, key=lambda p: p[0])
    left_index = left_hull.index(left_point)
    right_index = right_hull.index(right_point)

    while True:
        move_left = False
        move_right = False

        current_slope = find_the_slope(left_point, right_point)

        while True:
            prev_left_index = (left_index - 1 + len_left) % len_left
            prev_left_point = left_hull[prev_left_index]
            new_slope = find_the_slope(prev_left_point, right_point)

            if new_slope < current_slope:
                left_point = prev_left_point
                left_index = prev_left_index
                current_slope = new_slope
                move_left = True
            else:
                break

        while True:
            next_right_index = (right_index + 1) % len_right
            next_right_point = right_hull[next_right_index]
            new_slope = find_the_slope(left_point, next_right_point)

            if new_slope > current_slope:
                right_point = next_right_point
                right_index = next_right_index
                current_slope = new_slope
                move_right = True
            else:
                break

        if not move_left and not move_right:
            break

    lower_left = left_point
    lower_right = right_point
    final_hull = []
    temp_index = left_hull.index(upper_left)
    final_hull.append(upper_left)
    while left_hull[temp_index] != lower_left:
        temp_index = (temp_index + 1) % len_left
        final_hull.append(left_hull[temp_index])
    temp_index = right_hull.index(lower_right)
    final_hull.append(lower_right)
    while right_hull[temp_index] != upper_right:
        temp_index = (temp_index + 1) % len_right
        final_hull.append(right_hull[temp_index])
    return final_hull


def find_the_hull(sorted_points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if len(sorted_points) == 1 or len(sorted_points) == 2:
        return sorted_points
    median: int = len(sorted_points) // 2
    left_part = sorted_points[:median]
    right_part = sorted_points[median:]
    left_hull = find_the_hull(left_part)
    right_hull = find_the_hull(right_part)
    return merge(left_hull, right_hull)


def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    points.sort(key=lambda p: p[0])
    final_hull: list[tuple[float, float]] = find_the_hull(points)
    return final_hull


def orientation(p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> int:
    val = (q[1] - p[1]) * (r[0] - q[0]) - \
          (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2


def distance_sq(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def compare_angles(anchor_point: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float]) -> int:
    o = orientation(anchor_point, p1, p2)
    if o == 0:
        return 1 if distance_sq(anchor_point, p2) >= distance_sq(anchor_point, p1) else -1
    elif o == 2:
        return -1
    else:
        return 1


def compute_hull_other(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    anchor_point = min(points, key=lambda p: (p[1], p[0]))
    anchor_index = points.index(anchor_point)
    points[0], points[anchor_index] = points[anchor_index], points[0]
    compare_with_anchor = functools.partial(compare_angles, anchor_point)
    sorted_points = sorted(points[1:], key=functools.cmp_to_key(compare_with_anchor))
    if not sorted_points:
        return [anchor_point]
    hull_stack = []
    hull_stack.append(anchor_point)
    hull_stack.append(sorted_points[0])
    for i in range(1, len(sorted_points)):
        new_point = sorted_points[i]
        while len(hull_stack) > 1 and orientation(hull_stack[-2], hull_stack[-1], new_point) != 2:
            hull_stack.pop()
        hull_stack.append(new_point)

    return hull_stack
