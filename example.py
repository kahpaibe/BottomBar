import time
from BottomBar import BottomBar

def _factorial(n):
    if n == 0:
        return 1
    else:
        return n * _factorial(n - 1)
    
def factorial(n): # Just add processing time
    time.sleep(n/10) # Simulate some processing time
    return _factorial(n)

if __name__ == '__main__':
    start_time = time.time()
    N = 50
    with BottomBar(bar_height=5) as bar:
        # Define Bar
        bar.print_bar_line(0, "============== factorial ==============")
        bar.print_bar_line(1, " Just a simple factorial calculator !")
        bar.print_bar_line(2, f" Computed : 0 / {N}")
        bar.print_bar_line(3, f" Elapsed Time: {time.time() - start_time:.2f} seconds")
        bar.print_bar_line(4, "=======================================")

        for i in range(N):
            result = factorial(i)
            bar.print_line(f"Factorial of {i} is {result}")
            bar.print_bar_line(2, f" Computed : {i + 1} / {N}")
            bar.print_bar_line(3, f" Elapsed Time: {time.time() - start_time:.2f} seconds")