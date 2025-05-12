class PathOptimizer:
    def __init__(self, maze):
        self.maze = maze
        
    def smooth_path(self, path):
        """Remove unnecessary waypoints using line-of-sight checks"""
        if len(path) < 2:
            return path
            
        smoothed = [path[0]]
        current = 0
        
        while current < len(path)-1:
            for lookahead in range(len(path)-1, current, -1):
                if self._has_line_of_sight(smoothed[-1], path[lookahead]):
                    smoothed.append(path[lookahead])
                    current = lookahead
                    break
            else:
                smoothed.append(path[current+1])
                current += 1
                
        return smoothed
        
    def _has_line_of_sight(self, p1, p2):
        """Bresenham's line algorithm to check obstacle-free path"""
        x1, y1 = p1
        x2, y2 = p2
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            if self.maze.grid[y1][x1] == 1:
                return False
            if x1 == x2 and y1 == y2:
                break
            e2 = 2*err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
                
        return True