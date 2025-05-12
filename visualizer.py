import matplotlib.pyplot as plt

class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        self.fig, self.ax = plt.subplots()
        
    def plot_maze(self):
        self.ax.clear()
        # Plot walls
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    self.ax.add_patch(plt.Rectangle((x-0.5, y-0.5), 1, 1, color='black'))
        
        # Start and goal markers
        self.ax.plot(0, 0, 'go', markersize=10)  # Start
        self.ax.plot(self.maze.width-1, self.maze.height-1, 'ro', markersize=10)  # Goal
        
        self.ax.set_xlim(-0.5, self.maze.width-0.5)
        self.ax.set_ylim(-0.5, self.maze.height-0.5)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        
    def plot_path(self, path, color='blue', linewidth=2):
        if not path:
            return
        x_coords = [0] + [p[0] for p in path]
        y_coords = [0] + [p[1] for p in path]
        self.ax.plot(x_coords, y_coords, color=color, linewidth=linewidth)
        
    def show(self):
        plt.show()