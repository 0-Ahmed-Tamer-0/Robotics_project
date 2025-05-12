import json
import matplotlib.pyplot as plt
import numpy as np

def plot_results(filename):
    with open(filename) as f:
        data = json.load(f)
    
    metrics = data['metrics']
    algorithms = list(metrics.keys())
    
    # Success Rate Plot
    plt.figure(figsize=(10, 5))
    success_rates = [metrics[algo]['success_rate']*100 for algo in algorithms]
    plt.bar(algorithms, success_rates)
    plt.title('Success Rate Comparison')
    plt.ylabel('Success Rate (%)')
    plt.ylim(0, 100)
    plt.savefig('success_rate.png')
    
    # Path Length Comparison
    plt.figure(figsize=(10, 5))
    avg_lengths = [metrics[algo]['avg_length'] for algo in algorithms]
    std_devs = [metrics[algo]['std_length'] for algo in algorithms]
    plt.bar(algorithms, avg_lengths, yerr=std_devs, capsize=5)
    plt.title('Average Path Length Comparison')
    plt.ylabel('Path Length (steps)')
    plt.savefig('path_lengths.png')
    
    # Computation Time
    plt.figure(figsize=(10, 5))
    times = [metrics[algo]['avg_time'] for algo in algorithms]
    time_std = [metrics[algo]['std_time'] for algo in algorithms]
    plt.bar(algorithms, times, yerr=time_std, capsize=5)
    plt.title('Computation Time Comparison')
    plt.ylabel('Time (seconds)')
    plt.savefig('computation_times.png')

if __name__ == "__main__":
    plot_results('benchmark_results.json')
    plt.show()