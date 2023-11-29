# fa-mru

# Cache Simulator

This is a cache simulator written in Python using the `ttkbootstrap` library. The simulator models a cache memory system and provides a graphical user interface (GUI) for users to interact with.

## Installation

Before running this code, you must first install the `ttkbootstrap` library. You can do this by running the following command in your terminal:

``` 
pip install ttkbootstrap
```

## Project Specifications:
Number of cache blocks = 32 blocks
Cache line = 16 words
Read policy: Non Load-through
Number of memory blocks = User Input
Cache Mapping Function = Full Associative Mapping (FA)
Cache Replacement Algorithm = Most Recently Used (MRU)

## Terminology:
### Full Associative Cache Mapping: Enables all main memory blocks to be mapped onto any cache block
### Most Recently Used Replacement Algorithm: The MRU assists in identifying which cache block may be overwritten (released) when all cache blocks in the main memory blocks are already in use by replacing the most recently used block.
### Sequential Sequence: Sequential sequence is an access pattern wherein the data is accessed in a sequential or orderly manner based on the addresses assigned to the cache block. To access a memory block, it needs to traverse through the memory addresses in a sequential manner, starting from a known point.
### Random Sequence: Random sequence is an access pattern wherein the data can be accessed from any cache block in the main memory, unpredictably without the need to traverse through intervening addresses.
### Mid-repeat Blocks: Mid-repeat blocks is an access pattern wherein the data is accessed starting from the middle of the cache block in the main memory.
### Cache hit rate: Fraction of memory accesses found in the cache memory
### Cache miss rate: Fraction of memory accesses not found in the cache.
### Average memory access time: Derived from the formula Tavg = hC + (1 - h) * M
### Legend:
h = hit rate
C = cache access time
M = miss penalty


## Running the Simulator

After installing the `ttkbootstrap` library, you can run the simulator by executing the "simulation.py" Python script. The simulator will open a GUI where you can input the number of cache blocks, select a test case, and choose the animation type.

## Usage

The simulator provides two types of animations: "Step-by-step" and "Final Snapshot". In the "Step-by-step" animation, the simulator will step through each memory access one at a time. In the "Final Snapshot" animation, the simulator will run all memory accesses at once and then display the final state of the cache.

The simulator also provides statistics about the cache accesses, including the total number of accesses, the number of hits and misses, the hit rate and miss rate, the average memory access time, and the total memory access time. These statistics are displayed in the GUI and are also logged to a file named "cache_log.txt".
