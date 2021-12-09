class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def reachable(self, start):
        visited = set()
        unvisited = [start]

        while unvisited:
            current = unvisited.pop()
            visited.add(current)

            for next_vert in self.edges[current]:
                if next_vert in visited:
                    continue
                unvisited.append(next_vert)

        return visited

