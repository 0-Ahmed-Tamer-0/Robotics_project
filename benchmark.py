import time
import numpy as np
import json
from scipy.stats import ttest_ind
from maze_generator import MazeGenerator
from aco_solver import ACOSolver
from pso_solver import PSOSolver
from abc_solver import ABCSolver

def run_benchmark(config, num_mazes=3, iterations=5):
    results = []
    
    for maze_num in range(num_mazes):
        maze = MazeGenerator(config['maze_size'], config['maze_size'])
        
        # Initialize solvers with tuned parameters
        solvers = {
            'ACO': ACOSolver(maze, **config['aco_params']),
            'PSO': PSOSolver(maze, **config['pso_params']),
            'ABC': ABCSolver(maze, **config['abc_params'])
        }
        
        maze_results = {}
        
        for algo_name, solver in solvers.items():
            start_time = time.time()
            solver.solve(iterations)
            elapsed = time.time() - start_time
            
            maze_results[algo_name] = {
                'length': solver.best_length if solver.best_length < float('inf') else None,
                'time': elapsed,
                'success': solver.best_length < float('inf'),
                'iterations': solver.iteration
            }
            
        results.append(maze_results)
        print(f"Completed maze {maze_num+1}/{num_mazes}")
        
    return results

def analyze_results(results):
    metrics = {}
    
    for algo in ['ACO', 'PSO', 'ABC']:
        algo_data = [r[algo] for r in results]
        
        # Success rate
        success_rate = np.mean([1 if d['success'] else 0 for d in algo_data])
        
        # Path length (only successful runs)
        lengths = [d['length'] for d in algo_data if d['success']]
        avg_length = np.mean(lengths) if lengths else float('inf')
        std_length = np.std(lengths) if lengths else 0
        
        # Computation time
        times = [d['time'] for d in algo_data]
        avg_time = np.mean(times)
        std_time = np.std(times)
        
        metrics[algo] = {
            'success_rate': success_rate,
            'avg_length': avg_length,
            'std_length': std_length,
            'avg_time': avg_time,
            'std_time': std_time
        }
    
    # Statistical comparisons
    comparisons = {}
    for a1, a2 in [('ACO', 'PSO'), ('ACO', 'ABC'), ('PSO', 'ABC')]:
        lengths1 = [r[a1]['length'] for r in results if r[a1]['success']]
        lengths2 = [r[a2]['length'] for r in results if r[a2]['success']]
        _, p_length = ttest_ind(lengths1, lengths2, nan_policy='omit')
        
        times1 = [r[a1]['time'] for r in results]
        times2 = [r[a2]['time'] for r in results]
        _, p_time = ttest_ind(times1, times2)
        
        comparisons[f"{a1}_vs_{a2}"] = {
            'path_length_p': p_length,
            'time_p': p_time
        }
    
    return {
        'metrics': metrics,
        'comparisons': comparisons
    }

def save_report(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    # Load tuned parameters (replace with actual values from tuning)
    config = {
        'maze_size': 15,
        'aco_params': {'n_ants': 30, 'evaporation': 0.5, 'alpha': 1, 'beta': 2},
        'pso_params': {'n_particles': 30, 'w': 0.6, 'c1': 1.5, 'c2': 2.0},
        'abc_params': {'n_employed': 20, 'limit': 50}
    }
    
    print("Running benchmark...")
    results = run_benchmark(config, num_mazes=3)
    analysis = analyze_results(results)
    
    print("\n=== Benchmark Results ===")
    for algo, stats in analysis['metrics'].items():
        print(f"\n{algo}:")
        print(f"  Success Rate: {stats['success_rate']*100:.1f}%")
        print(f"  Avg Path Length: {stats['avg_length']:.1f} ± {stats['std_length']:.1f}")
        print(f"  Avg Time: {stats['avg_time']:.2f}s ± {stats['std_time']:.2f}")
    
    print("\n=== Statistical Significance ===")
    for comp, pvals in analysis['comparisons'].items():
        print(f"\n{comp}:")
        print(f"  Path Length p-value: {pvals['path_length_p']:.4f}")
        print(f"  Computation Time p-value: {pvals['time_p']:.4f}")
    
    save_report(analysis, 'benchmark_results.json')