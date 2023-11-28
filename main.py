import random
import time

class CacheEntry:
    def __init__(self, tag=-1):
        self.valid = False
        self.tag = tag
        self.mru_counter = 0

class Cache:
    def __init__(self, num_blocks):
        self.num_blocks = num_blocks
        self.entries = [CacheEntry() for _ in range(num_blocks)]
        self.mru_counter = 0

    def access(self, address):
        # Check for cache hit
        for entry in self.entries:
            if entry.valid and entry.tag == address:
                entry.mru_counter = self.mru_counter
                self.mru_counter += 1
                return "hit"

        # Cache miss
        # Find the empty block if available
        empty_block = next((entry for entry in self.entries if not entry.valid), None)
        if empty_block is not None:
            empty_block.valid = True
            empty_block.tag = address
            empty_block.mru_counter = self.mru_counter
            self.mru_counter += 1
            return "miss"

        # If no empty blocks, find the most recently used block
        mru_block = max(self.entries, key=lambda entry: entry.mru_counter)
        mru_block.valid = True
        mru_block.tag = address
        mru_block.mru_counter = self.mru_counter
        self.mru_counter += 1
        return "miss"
    
    def display(self):
        for i, entry in enumerate(self.entries):
            print(f"Cache Block {i}: Valid={entry.valid}, Tag={entry.tag}, MRU Counter={entry.mru_counter}")

def calculate_statistics(memory_access_count, cache_hit_count, cache_miss_count):
    cache_hit_rate = cache_hit_count / memory_access_count
    cache_miss_rate = cache_miss_count / memory_access_count
    average_memory_access_time = 1 + cache_miss_rate
    total_memory_access_time = memory_access_count * average_memory_access_time

    return {
        "memory_access_count": memory_access_count,
        "cache_hit_count": cache_hit_count,
        "cache_miss_count": cache_miss_count,
        "cache_hit_rate": cache_hit_rate,
        "cache_miss_rate": cache_miss_rate,
        "average_memory_access_time": average_memory_access_time,
        "total_memory_access_time": total_memory_access_time
    }

def print_simulation_step(memory_access, cache_result, cache):
    print(f"Memory Access: {memory_access}")
    print(f"Cache Result: {cache_result}")
    cache.display()
    print("\n" + "=" * 50 + "\n")

def run_simulation(cache, memory_accesses, animated_trace=False):
    cache_hits = 0
    cache_misses = 0

    if animated_trace:
        print("Step-by-step animated tracing:")

    for i, address in enumerate(memory_accesses, start=1):
        result = cache.access(address)
        if result == "hit":
            cache_hits += 1
        else:
            cache_misses += 1

        if animated_trace:
            print_simulation_step(address, result, cache)
            time.sleep(1)  # Pause for 1 second between steps

    if not animated_trace:
        print("Final memory snapshot:")
        cache.display()

    return cache_hits, cache_misses

def main():
    cache_size = 32
    block_size = 16
    num_blocks = int(input("Enter the number of memory blocks: "))
    cache = Cache(num_blocks)

    # Test Case A: Sequential sequence
    test_case_a = list(range(2 * num_blocks)) * 4
    hits_a, misses_a = run_simulation(cache, test_case_a, animated_trace=True)
    statistics_a = calculate_statistics(len(test_case_a), hits_a, misses_a)

    # Test Case B: Random sequence
    test_case_b = random.sample(range(4 * num_blocks), 4 * num_blocks)
    hits_b, misses_b = run_simulation(cache, test_case_b)
    statistics_b = calculate_statistics(len(test_case_b), hits_b, misses_b)

    # Test Case C: Mid-repeat blocks
    mid_repeat = [i % num_blocks for i in range(num_blocks)] * 2 + [i for i in range(num_blocks, 2 * num_blocks)] * 4
    test_case_c = mid_repeat * 4
    hits_c, misses_c = run_simulation(cache, test_case_c)
    statistics_c = calculate_statistics(len(test_case_c), hits_c, misses_c)

    # Output
    print("\nTest Case A Statistics (Sequential sequence):")
    for key, value in statistics_a.items():
        print(f"{key}: {value}")

    print("\nTest Case B Statistics (Random sequence):")
    for key, value in statistics_b.items():
        print(f"{key}: {value}")

    print("\nTest Case C Statistics (Mid-repeat blocks):")
    for key, value in statistics_c.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
