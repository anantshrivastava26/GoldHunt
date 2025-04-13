import random
from collections import deque

class Game:
    def __init__(self, size):
        self.size = size
        self.grid = [["" for _ in range(size)] for _ in range(size)]
        self.player_pos = [0, 0]
        self.knowledge = [[False for _ in range(size)] for _ in range(size)]
        self.status = "Playing"
        self.generate_map()

    def generate_map(self):
        self.gold_pos = [random.randint(0, self.size-1), random.randint(0, self.size-1)]
        while self.gold_pos == [0, 0]:
            self.gold_pos = [random.randint(0, self.size-1), random.randint(0, self.size-1)]
        self.grid[self.gold_pos[0]][self.gold_pos[1]] = "G"

        danger_count = self.size
        for _ in range(danger_count):
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if self.grid[x][y] == "" and [x, y] != [0, 0]:
                self.grid[x][y] = "D"
                for dx, dy in [(0,1), (1,0), (-1,0), (0,-1)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[nx][ny] == "":
                        self.grid[nx][ny] = "W"

        while not self.validate_path():
            self.__init__(self.size)

        self.update_knowledge(self.player_pos)

    def validate_path(self):
        queue = deque([[0, 0]])
        visited = set()
        while queue:
            x, y = queue.popleft()
            if [x, y] == self.gold_pos:
                return True
            for dx, dy in [(0,1),(1,0),(-1,0),(0,-1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if (nx, ny) not in visited and self.grid[nx][ny] != "D":
                        visited.add((nx, ny))
                        queue.append([nx, ny])
        return False

    def move_player(self, direction):
        if self.status != "Playing":
            return
        dx, dy = {"up": (-1,0), "down": (1,0), "left": (0,-1), "right": (0,1)}[direction]
        nx, ny = self.player_pos[0]+dx, self.player_pos[1]+dy
        if 0 <= nx < self.size and 0 <= ny < self.size:
            self.player_pos = [nx, ny]
            self.check_status()
            self.update_knowledge(self.player_pos)

    def check_status(self):
        x, y = self.player_pos
        cell = self.grid[x][y]
        if cell == "D":
            self.status = "Game Over - Fell in a Pit!"
        elif cell == "G":
            self.status = "You Won - Found the Gold!"

    def update_knowledge(self, pos):
        x, y = pos
        self.knowledge[x][y] = True
        for dx, dy in [(0,1),(1,0),(-1,0),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                self.knowledge[nx][ny] = True

    def get_visible_grid(self):
        visible = [["hidden" for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.knowledge[i][j]:
                    if self.player_pos == [i, j]:
                        visible[i][j] = "player"
                    elif self.grid[i][j] == "G" and self.status != "Playing":
                        visible[i][j] = "gold"
                    elif self.grid[i][j] == "D" and self.status != "Playing":
                        visible[i][j] = "danger"
                    elif self.grid[i][j] == "W":
                        visible[i][j] = "warning"
                    else:
                        visible[i][j] = "empty"
        return visible

    def run_ai_trace(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        visited = set()
        queue = deque()
        came_from = {}

        start = tuple(self.player_pos)
        goal = tuple(self.gold_pos)

        queue.append(start)
        visited.add(start)
        found = False

        while queue:
            current = queue.popleft()
            if current == goal:
                found = True
                break
            for d in directions:
                ni, nj = current[0] + d[0], current[1] + d[1]
                neighbor = (ni, nj)
                if 0 <= ni < self.size and 0 <= nj < self.size:
                    if neighbor not in visited and self.grid[ni][nj] != "D":
                        visited.add(neighbor)
                        queue.append(neighbor)
                        came_from[neighbor] = current

        if not found:
            return [{"pos": self.player_pos, "grid": self.get_visible_grid(), "status": "No path found"}]

        # Reconstruct path
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()

        # Simulate the player's step-by-step journey
        steps = []
        for pos in path:
            self.player_pos = list(pos)
            self.update_knowledge(pos)
            self.check_status()
            steps.append({
                "pos": list(pos),
                "grid": self.get_visible_grid(),
                "status": self.status if pos == goal else "Playing"
            })

        return steps
