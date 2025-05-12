from maze_generator import MazeGenerator
from aco_solver import ACOSolver
from pso_solver import PSOSolver
from abc_solver import ABCSolver
from visualizer import MultiAlgorithmVisualizer

# Create 15x15 maze with 20% obstacles
maze = MazeGenerator(15, 15, obstacle_density=0.2)

# Initialize solvers with matching parameters
solvers = [
    ACOSolver(maze, n_ants=30),
    PSOSolver(maze, n_particles=30),
    ABCSolver(maze, n_employed=30)
]

# Create and run visualizer
visualizer = MultiAlgorithmVisualizer(maze, solvers)
visualizer.animate()
