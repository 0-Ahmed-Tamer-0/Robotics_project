# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from aco_solver import ACOSolver
# class MazeVisualizer:
#     def __init__(self, maze):
#         self.maze = maze
#         self.fig, self.ax = plt.subplots()
        
#     def plot_maze(self):
#         self.ax.clear()
#         # Plot walls
#         for y in range(self.maze.height):
#             for x in range(self.maze.width):
#                 if self.maze.grid[y][x] == 1:
#                     self.ax.add_patch(plt.Rectangle((x-0.5, y-0.5), 1, 1, color='black'))
        
#         # Start and goal markers
#         self.ax.plot(0, 0, 'go', markersize=10)  # Start
#         self.ax.plot(self.maze.width-1, self.maze.height-1, 'ro', markersize=10)  # Goal
        
#         self.ax.set_xlim(-0.5, self.maze.width-0.5)
#         self.ax.set_ylim(-0.5, self.maze.height-0.5)
#         self.ax.set_aspect('equal')
#         self.ax.invert_yaxis()
        
#     def plot_path(self, path, color='blue', linewidth=2):
#         if not path:
#             return
#         x_coords = [0] + [p[0] for p in path]
#         y_coords = [0] + [p[1] for p in path]
#         self.ax.plot(x_coords, y_coords, color=color, linewidth=linewidth)
        
#     def show(self):
#         plt.show()
        

# class AnimatedVisualizer(MazeVisualizer):
#     def __init__(self, maze, solver):
#         super().__init__(maze)
#         self.solver = solver
#         self.path_line, = self.ax.plot([], [], 'b-', linewidth=2)
#         self.animation_running = True
        
#         if isinstance(solver, ACOSolver):
#             self.pheromone_plot = self.ax.imshow(
#                 solver.pheromones, 
#                 cmap='hot', 
#                 alpha=0.3,
#                 origin='lower',
#                 extent=(-0.5, maze.width-0.5, -0.5, maze.height-0.5)
#             )
            
#     def update_frame(self, frame):
#         if not self.animation_running:
#             return
#         # Run one iteration of the solver
#         if self.solver.iteration < self.solver.max_iter:
#             self.solver._run_single_iteration()
#         # Update algorithm visualization
#         if isinstance(self.solver, ACOSolver):
#             self.pheromone_plot.set_data(self.solver.pheromones)
#             self.pheromone_plot.autoscale()
            
#         # Update path
#         x_coords = [0] + [p[0] for p in self.solver.best_path]
#         y_coords = [0] + [p[1] for p in self.solver.best_path]
#         self.path_line.set_data(x_coords, y_coords)
        
#         self.fig.canvas.draw_idle()
#         return self.path_line, self.pheromone_plot
        
#     def animate(self):
#         timer = self.fig.canvas.new_timer(interval=100)
#         timer.add_callback(self.update_frame, None)
#         timer.start()
#         plt.show()
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from aco_solver import ACOSolver

# class MultiAlgorithmVisualizer:
#     def __init__(self, maze, solvers):
#         self.maze = maze
#         self.solvers = solvers
#         self.fig, self.axs = plt.subplots(1, 3, figsize=(15, 5))
#         self.lines = []
#         self.heatmaps = []

#         # Initialize plots
#         for i, (ax, solver) in enumerate(zip(self.axs, solvers)):
#             ax.set_title(f"{type(solver).__name__}")
#             ax.imshow(maze.grid, cmap='binary', origin='lower')
#             ax.plot(0, 0, 'go', markersize=10)  # Start
#             ax.plot(maze.width-1, maze.height-1, 'ro', markersize=10)  # Goal
#             line, = ax.plot([], [], 'b-', lw=2)
#             self.lines.append(line)
            
#             if isinstance(solver, ACOSolver):
#                 heatmap = ax.imshow(solver.pheromones, cmap='hot', alpha=0.3)
#                 self.heatmaps.append(heatmap)
#             else:
#                 self.heatmaps.append(None)

#     def update(self, frame):
#         for i, solver in enumerate(self.solvers):
#             if solver.iteration < 100:  # Max iterations
#                 solver._run_single_iteration()
                
#                 # Update path line
#                 x = [0] + [p[0] for p in solver.best_path or []]
#                 y = [0] + [p[1] for p in solver.best_path or []]
#                 self.lines[i].set_data(x, y)
                
#                 # Update pheromone heatmap for ACO
#                 if isinstance(solver, ACOSolver):
#                     self.heatmaps[i].set_data(solver.pheromones)
                    
#         return [*self.lines, *[h for h in self.heatmaps if h is not None]]

#     def animate(self):
#         ani = FuncAnimation(self.fig, self.update, interval=50, blit=True)
#         plt.show()
class MultiAlgorithmVisualizer:
    def __init__(self, maze, solvers):
        self.maze = maze
        self.solvers = solvers
        self.fig, self.axs = plt.subplots(1, 3, figsize=(15, 5))
        self.lines = []
        self.heatmaps = []
        self.max_iterations = 200  # Add iteration limit

        # Initialize plots with proper limits
        for i, (ax, solver) in enumerate(zip(self.axs, solvers)):
            ax.set_title(f"{type(solver).__name__}")
            ax.set_xlim(-0.5, maze.width-0.5)
            ax.set_ylim(-0.5, maze.height-0.5)
            ax.imshow(maze.grid, cmap='binary', origin='lower')
            ax.plot(0, 0, 'go', markersize=10)  # Start
            ax.plot(maze.width-1, maze.height-1, 'ro', markersize=10)  # Goal
            line, = ax.plot([], [], 'b-', lw=2)
            self.lines.append(line)
            
            if isinstance(solver, ACOSolver):
                heatmap = ax.imshow(solver.pheromones, cmap='hot', alpha=0.3,
                                   extent=(-0.5, maze.width-0.5, -0.5, maze.height-0.5))
                self.heatmaps.append(heatmap)
            else:
                self.heatmaps.append(None)

    def update(self, frame):
        for i, solver in enumerate(self.solvers):
            if solver.iteration < self.max_iterations:
                solver._run_single_iteration()
                
                # Get current path or empty list
                current_path = solver.best_path if solver.best_path else []
                
                # Convert path to plot coordinates
                x = [0] + [p[0] for p in current_path]
                y = [0] + [p[1] for p in current_path]
                self.lines[i].set_data(x, y)
                
                # Update pheromone heatmap for ACO
                if isinstance(solver, ACOSolver):
                    self.heatmaps[i].set_data(solver.pheromones)
                    self.heatmaps[i].autoscale()
                    
        return [*self.lines, *[h for h in self.heatmaps if h is not None]]

    def animate(self):
        ani = FuncAnimation(
            self.fig,
            self.update,
            frames=self.max_iterations,  # Explicit frame count
            interval=50,
            blit=True,
            cache_frame_data=False  # Disable caching
        )
        plt.show()