# fa-mru

# Cache Simulator

This is a cache simulator written in Python using the `ttkbootstrap` library. The simulator models a cache memory system and provides a graphical user interface (GUI) for users to interact with.

## Installation

Before running this code, you must first install the `ttkbootstrap` library. You can do this by running the following command in your terminal:

bash pip install ttkbootstrap

## Running the Simulator

After installing the `ttkbootstrap` library, you can run the simulator by executing the "simulation.py" Python script. The simulator will open a GUI where you can input the number of cache blocks, select a test case, and choose the animation type.

## Usage

The simulator provides two types of animations: "Step-by-step" and "Final Snapshot". In the "Step-by-step" animation, the simulator will step through each memory access one at a time. In the "Final Snapshot" animation, the simulator will run all memory accesses at once and then display the final state of the cache.

The simulator also provides statistics about the cache accesses, including the total number of accesses, the number of hits and misses, the hit rate and miss rate, the average memory access time, and the total memory access time. These statistics are displayed in the GUI and are also logged to a file named "cache_log.txt".