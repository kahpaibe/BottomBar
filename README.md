# BottomBar

A simple Python utility to create a persistent zone at the bottom of the terminal for displaying status information, while allowing regular output above it. It makes use of ANSI escape codes to manipulate cursor position and clear lines, should allow widely compatibility across different terminal emulators.

## Overview

From [example.py](./example.py)

<img height="300" alt="image" src="https://github.com/user-attachments/assets/39c1cd06-003b-440f-8765-d6fbed793bcc" />

## Requirements
- Python 3.10+

## Usage

The user should call `bottom_bar.init()` before printing anything and `bottom_bar.print_final_line()` before exiting the program to ensure the terminal state is clean. Using a context manager is recommended to handle this automatically.

Basic Example:
```python
from BottomBar import BottomBar
bar = BottomBar(bar_height=2)
bar.init() # Initialize the bottom bar at the start
for i in range(5):
    bar.print_line(f"Main Line {i+1}")

bar.print_bar_line(0, "Status: Running")
bar.print_bar_line(1, "Progress: 50%")
bar.print_final_line() # Clean up the terminal before exiting
```
Above example may erase last line if an exception occurs before `print_final_line()` is called. To avoid this, use a context manager or finally block.

Clean Example, no context manager:
```python
from BottomBar import BottomBar
bar = BottomBar(bar_height=3)
bar.init() # Initialize the bottom bar at the start
try:
    for i in range(10):
        bar.print_line(f"Main Line {i+1}")
    
    bar.print_bar_line(0, "Status: Running")
    bar.print_bar_line(1, "Progress: 50%")
    bar.print_bar_line(2, "Errors: 0")
finally:
    bar.print_final_line() # Ensure terminal is cleaned up
```

Clean Example, context manager.
```python
from BottomBar import BottomBar

with BottomBar(bar_height=3) as bar:
    for i in range(10):
        bar.print_line(f"Main Line {i+1}")
    
    bar.print_bar_line(0, "Status: Running")
    bar.print_bar_line(1, "Progress: 50%")
    bar.print_bar_line(2, "Errors: 0")
```

## Issues

The library is very basic, issues will arise easily... For example, resizing the terminal while the program is running may cause display issues.