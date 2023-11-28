import random
import time
import sys
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

def print_simulation_step(memory_access, cache_result, cache, file, print_to_console=False):
  console_output = f"Memory Access: {memory_access}\n"
  console_output += f"Cache Result: {cache_result}\n"
  for i, entry in enumerate(cache.entries):
      console_output += f"Cache Block {i}: Valid={entry.valid}, Tag={entry.tag}, MRU Counter={entry.mru_counter}\n"
  console_output += "\n" + "=" * 50 + "\n"

  if print_to_console:
      print(console_output)

  file.write(console_output)

def run_simulation(cache, memory_accesses, animated_trace=False, test_case_title=None,filename=None):
 cache_hits = 0
 cache_misses = 0

 with open(filename, "w") as file:
    if test_case_title is not None:
        file.write(f"{test_case_title}\n")
        file.write("=" * 50 + "\n")
         
    if animated_trace:
        print("\nStep-by-step animated tracing:")


    for address in memory_accesses:
        result = cache.access(address)
        if result == "hit":
            cache_hits += 1
        else:
            cache_misses += 1

        print_simulation_step(address, result, cache, file, print_to_console=animated_trace)
        
        if animated_trace:
            time.sleep(1) # Pause for 1 second between steps
    else:
        print("Final memory snapshot:")
        cache.display()

 return cache_hits, cache_misses


def main():
  cache_size = 32
  block_size = 16
  num_blocks = int(input("Enter the number of memory blocks: "))
  cache_a = Cache(num_blocks)
  cache_b = Cache(num_blocks)
  cache_c = Cache(num_blocks)

  # Test Case A: Sequential sequence
  test_case_a = list(range(2 * num_blocks)) * 4
  animated_trace_a = input("Do you want to animate trace for Test Case A? (yes/no): ") == "yes"

  # Test Case B: Random sequence
  test_case_b = random.sample(range(4 * num_blocks), 4 * num_blocks)
  animated_trace_b = input("Do you want to animate trace for Test Case B? (yes/no): ") == "yes"

  # Test Case C: Mid-repeat blocks
  mid_repeat = [i % num_blocks for i in range(num_blocks)] * 2 + [i for i in range(num_blocks, 2 * num_blocks)] * 4
  test_case_c = mid_repeat * 4
  animated_trace_c = input("Do you want to animate trace for Test Case C? (yes/no): ") == "yes"

  # Run simulations
  hits_a, misses_a = run_simulation(cache_a, test_case_a, animated_trace=animated_trace_a, test_case_title="Test Case A: Sequential sequence", filename="simulation_trace_a.txt")
  statistics_a = calculate_statistics(len(test_case_a), hits_a, misses_a)

  hits_b, misses_b = run_simulation(cache_b, test_case_b, animated_trace=animated_trace_b, test_case_title="Test Case B: Random sequence", filename="simulation_trace_b.txt")
  statistics_b = calculate_statistics(len(test_case_b), hits_b, misses_b)

  hits_c, misses_c = run_simulation(cache_c, test_case_c, animated_trace=animated_trace_c, test_case_title="Test Case C: Mid-repeat blocks", filename="simulation_trace_c.txt")
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

