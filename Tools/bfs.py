import random

#Gets all the adjacent tiles
def adjacent(list, pos):
    row = pos[0]
    col = pos[1]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    adjacent_indices = []

    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < len(list[0]) and 0 <= new_col < len(list):
            adjacent_indices.append((new_row, new_col))

    return adjacent_indices


#A very simple Breadth-first search
def bfs(graph, node, end):
    visited = set()
    queue = [(node,[node])]

    visited.add(node)

    while queue:
        s,path = queue.pop(0)
        
        #If the current node is a wall it continues to ignore that node
        if(graph[s[1]][s[0]] != 0):
            continue

        for n in adjacent(graph, s):
            randNum = random.randint(0,100)
            if(randNum % 5 == 0):
                continue
            if(n == end):
                return path + [n]
            if(graph[n[1]][n[0]] == 0):
                if n not in visited:
                    visited.add(n)
                    queue.append((n, path + [n]))
    
    return []


