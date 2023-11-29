import ttkbootstrap as tk
import tkinter.ttk as ttk
import random
import os

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
      for entry in self.entries:
          if entry.valid and entry.tag == address:
              entry.mru_counter = self.mru_counter
              self.mru_counter += 1
              return "hit"

      empty_block = next((entry for entry in self.entries if not entry.valid), None)
      if empty_block is not None:
          empty_block.valid = True
          empty_block.tag = address
          empty_block.mru_counter = self.mru_counter
          self.mru_counter += 1
          return "miss"

      mru_block = max(self.entries, key=lambda entry: entry.mru_counter)
      mru_block.valid = True
      mru_block.tag = address
      mru_block.mru_counter = self.mru_counter
      self.mru_counter += 1
      return "miss"
  

class CacheGUI:
   def __init__(self):
        self.root = tk.Window(themename="minty")
        self.root.title("Cache Simulator")
        self.root.resizable(True, True) # Set window size to 1000x600
        self.root.minsize(1800, 600) # Set the minimum size
        #self.root.maxsize(1000, 800) # Set the maximum size
        style = tk.Style()
        style.configure('.', font=("Roboto", 14))
        style.configure('TEntry', font=("Roboto", 14))
        style.configure('Custom.Treeview',
                    height=100,
                    rowheight=50)
        
        # Configure the rows and columns
        for i in range(100):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_columnconfigure(4, weight=1)

        self.num_blocks_label = tk.Label(self.root, text="Enter Number of Blocks:")
        self.num_blocks_label.grid(row=0, column=0, sticky='ew', padx=(50,0))

        self.num_blocks = tk.Entry(self.root)
        self.num_blocks.grid(row=0, column=1, sticky='ew')
        
        self.test_case_label = tk.Label(self.root, text="Select Test Case:")
        self.test_case_label.grid(row=1, column=0, sticky='ew', padx=(50,0))
        
        self.test_case = tk.Combobox(self.root, values=["Sequential sequence", "Random sequence", "Mid-repeat blocks"])
        self.test_case.grid(row=1, column=1, sticky='ew')
        
        self.animation_type_label = tk.Label(self.root, text="Select Animation Type:")
        self.animation_type_label.grid(row=2, column=0, sticky='ew', padx=(50,0))

        self.animation_type = tk.Combobox(self.root, values=["Step-by-step", "Final Snapshot"])
        self.animation_type.grid(row=2, column=1, sticky='ew')

        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=3, column=0, sticky='ew', padx=(50,20))

        self.log_button = tk.Button(self.root, text="Open Log", command=self.open_log, state='disabled')
        self.log_button.grid(row=3, column=1, sticky='ew')
        
        self.statistics_frame = tk.Frame(self.root, borderwidth=0, relief='solid')
        self.statistics_frame.grid(row=0, column=2, rowspan=7, sticky="ns", pady=(10,0), padx=(50,50)) 
        

            # Statistics labels
        self.total_accesses_label = tk.Label(self.statistics_frame, justify='center')
        self.total_accesses_label.grid(row=0, column=0)

        self.hits_label = tk.Label(self.statistics_frame, justify='center')
        self.hits_label.grid(row=1, column=0)

        self.misses_label = tk.Label(self.statistics_frame, justify='center')
        self.misses_label.grid(row=2, column=0)

        self.hit_rate_label = tk.Label(self.statistics_frame, justify='center')
        self.hit_rate_label.grid(row=3, column=0)

        self.miss_rate_label = tk.Label(self.statistics_frame, justify='center')
        self.miss_rate_label.grid(row=4, column=0)

        self.average_mem_label = tk.Label(self.statistics_frame, justify='center')
        self.average_mem_label.grid(row=5, column=0)

        self.total_mem_label = tk.Label(self.statistics_frame, justify='center')
        self.total_mem_label.grid(row=6, column=0)
        
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.grid(row=0, column=5, rowspan=12, pady=(20,0), padx=(10,50), sticky='ne')

        # Create table
        self.memory_table = ttk.Treeview(self.table_frame, columns=("Memory Blocks", "Hit", "Miss"), style='Custom.Treeview', height=7)
        self.memory_table.grid(sticky='nsew')

        # Create a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.memory_table.yview)
        self.scrollbar.grid(sticky='ns', row=0, column=1, rowspan=7)

        # Configure the Treeview to update the scrollbar when it's scrolled
        self.memory_table.configure(yscrollcommand=self.scrollbar.set)

        # Configure column headers
        self.memory_table.heading("#0", text="")
        self.memory_table.heading("Memory Blocks", text="Memory Blocks")
        self.memory_table.heading("Hit", text="Hit")
        self.memory_table.heading("Miss", text="Miss")

        # Configure column widths
        self.memory_table.column("#0", width=0)
        self.memory_table.column("Memory Blocks")
        self.memory_table.column("Hit", width=80)
        self.memory_table.column("Miss", width=80)

        # Configure column heights
        self.memory_table.column("#0", width=0)
        self.memory_table.column("Memory Blocks", width=150, anchor='center')
        self.memory_table.column("Hit", width=60, anchor='center')
        self.memory_table.column("Miss", width=100, anchor='center')
        
        self.reset_button = tk.Button(self.root, text="Reset Simulation", command=self.reset_simulation)
        self.reset_button.grid(row=12, column=5, sticky='ew', padx=(0,50))


        
   def update_memory_table(self, index, memory_address, hit):
        # Check if item with same index already exists
        if self.memory_table.exists(index):
            if hit == 1:
                self.memory_table.item(index, values=(memory_address, "*", ""))
            else:
                self.memory_table.item(index, values=(memory_address, "", "*"))
        else:
            if hit == 1:
                self.memory_table.insert("", "end", iid=index, values=(memory_address, "*", ""))
            else:
                self.memory_table.insert("", "end", iid=index, values=(memory_address, "", "*"))
        self.memory_table.yview_moveto(1)


   def create_entries(self, num_blocks):
    self.entries = []
    self.labels = [] # Create a list to store the labels
    for i in range(num_blocks):
        header1 = tk.Label(self.root, text="Data")
        header1.grid(row=7, column=1)
        self.labels.append(header1) # Add the label to the list

        header2 = tk.Label(self.root, text="Counter")
        header2.grid(row=7, column=2) 
        self.labels.append(header2) # Add the label to the list

        label = tk.Label(self.root, text=f"Cache Block {i}:")
        label.grid(row=i+8, column=0)
        self.labels.append(label) # Add the label to the list

        tag_entry = tk.Entry(self.root)
        tag_entry.grid(row=i+8, column=1)

        mru_counter_entry = tk.Entry(self.root)
        mru_counter_entry.grid(row=i+8, column=2)
        
        self.entries.append((tag_entry, mru_counter_entry)) # Store a tuple of Entry widgets in self.entries


   def update_entries(self):
    for i, entry in enumerate(self.cache.entries):
        tag_entry, mru_counter_entry = self.entries[i] # Unpack the tuple of Entry widgets

        tag_entry.delete(0, tk.END)
        tag_entry.insert(0, str(entry.tag))

        mru_counter_entry.delete(0, tk.END)
        mru_counter_entry.insert(0, str(entry.mru_counter))


   def run(self):
       self.root.mainloop()

   def start_simulation(self):
        # Clear the log file
        with open("cache_log.txt", "w") as file:
            pass

        num_blocks = int(self.num_blocks.get())
        self.cache = Cache(num_blocks)
        self.create_entries(num_blocks)
        self.memory_accesses = self.generate_memory_accesses()
        self.current_access = 0
        self.hits = 0
        self.misses = 0
        if self.animation_type.get() == "Step-by-step":
            self.root.after(1000, self.step) # Run step every 1000 ms
        else:
            self.run_final_snapshot()
            
   def run_final_snapshot(self):
        for address in self.memory_accesses:
            result = self.cache.access(address)
            is_hit = 0
            if result == "hit":
                self.hits += 1
                is_hit = 1
                self.update_memory_table(self.current_access, address, is_hit)
            else:
                self.misses += 1
                is_hit = 0
                self.update_memory_table(self.current_access, address, is_hit)
            self.current_access += 1
            self.log_cache_state(address, result)    
            self.update_entries()
        self.calculate_and_print_statistics()
        
   def generate_memory_accesses(self):
       num_blocks = int(self.num_blocks.get())
       test_case = self.test_case.get()
       if test_case == "Sequential sequence":
           return list(range(2 * num_blocks)) * 4
       elif test_case == "Random sequence":
           return random.sample(range(4 * num_blocks), 4 * num_blocks)
       elif test_case == "Mid-repeat blocks":
           mid_blocks = [0] + (list(range(1, num_blocks-1)) * 2) + list(range(num_blocks-1, 2 * num_blocks))
           return mid_blocks * 4

   def step(self):
        if self.current_access < len(self.memory_accesses):
            address = self.memory_accesses[self.current_access]
            result = self.cache.access(address)
            is_hit = 0
            
            if result == "hit":
                self.hits += 1
                is_hit = 1
                self.update_memory_table(self.current_access, address, is_hit)
            else:
                self.misses += 1
                is_hit = 0
                self.update_memory_table(self.current_access, address, is_hit)
            self.current_access += 1

            self.update_entries()
            
            self.log_cache_state(address, result)

            if self.current_access == len(self.memory_accesses):
                self.calculate_and_print_statistics()

            self.root.after(1000, self.step) # Run step every 1000 ms



   def calculate_and_print_statistics(self):
       mem_accesses = len(self.memory_accesses)
       hit_rate = round(self.hits / mem_accesses, 4)
       miss_rate = round(self.misses / mem_accesses, 4)
       ave_mem = round(1 + hit_rate, 4)
       total_mem = round(ave_mem * mem_accesses, 4)

       self.total_accesses_label.config(text=f"Total Accesses: {mem_accesses}")
       self.hits_label.config(text=f"Hits: {self.hits}")
       self.misses_label.config(text=f"Misses: {self.misses}")
       self.hit_rate_label.config(text=f"Hit Rate: {hit_rate}")
       self.miss_rate_label.config(text=f"Miss Rate: {miss_rate}")
       self.average_mem_label.config(text=f"Average Memory Access Time: {ave_mem}")
       self.total_mem_label.config(text=f"Total Memory Access Time: {total_mem}")
          
       
   def log_cache_state(self, memory_access, cache_result):
    with open("cache_log.txt", "a") as file:
        file.write(f"Memory Access: {memory_access}\n")
        file.write(f"Cache Result: {cache_result}\n")
        for i, entry in enumerate(self.cache.entries):
            file.write(f"Cache Block {i}: Valid={entry.valid}, Tag={entry.tag}, MRU Counter={entry.mru_counter}\n")
        file.write("=" * 50 + "\n")
        self.log_button.config(state='normal')
        
   def open_log(self):
       os.startfile("cache_log.txt")
       
   def reset_simulation(self):
    # Clear all the cache entries
    for entry in self.entries:
       tag_entry, mru_counter_entry = entry
       tag_entry.destroy()
       mru_counter_entry.destroy()

    # Clear the labels
    for label in self.labels:
        label.config(text="") # Clear the content of the label

    # Clear the memory table
    for i in self.memory_table.get_children():
        self.memory_table.delete(i)

    # Clear the statistics labels
    self.total_accesses_label.config(text="")
    self.hits_label.config(text="")
    self.misses_label.config(text="")
    self.hit_rate_label.config(text="")
    self.miss_rate_label.config(text="")
    self.average_mem_label.config(text="")
    self.total_mem_label.config(text="")

    # Disable the log button
    self.log_button.config(state='disabled')

    

       
if __name__ == "__main__":
  gui = CacheGUI()
  gui.run()