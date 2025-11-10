from typing import Any

import logging

class BottomBar:
    """Use of ANSI escape codes to maintain a fixed-height section at the bottom of the terminal."""
    def __init__(self, bar_height: int):
        """Use of ANSI escape codes to maintain a fixed-height section at the bottom of the terminal.
        
        Args:
            bar_height (int): The number of lines for the bottom bar.
        """        
        assert bar_height > 0, "bar_height must be positive"
        self._bar_height = bar_height

    def __enter__(self):
        self.init()
        return self
    
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: Any | None) -> None:
        self.print_final_line()

    def init(self) -> None:
        """Initialize the bottom bar by printing empty lines. Should be called once at the start."""
        for _ in range(self._bar_height - 1):
            print()
        print("", end='')  # No new line at the end

    def print_line(self, *content: Any) -> None:
        """Print a line on the top part."""
        print(end="\n") # New line at the bottom
        print(f"\033[{self._bar_height}A", end='')  # Move cursor up
        print("\033[1L", end='')  # Insert 1 line
        print(*content, end='')  # Print content
        print(f"\033[{self._bar_height}B", end='')  # Move cursor down
        print("\033[E", end='')  # Move cursor to beginning of line

    def print_bar_line(self, y: int, *content: Any) -> None:
        """Print a line in the print bar at the specified y position of the bar.
        Args:
            y (int): The line number in the print bar (0-indexed, from top).
            *content (Any): The content to print.
        """
        assert 0 <= y < self._bar_height, "y must be within the print bar height"
        if y == self._bar_height - 1: # Last line special case
            print("\033[2K", end='')  # Clear line
            print(*content, end='')  # Print content
            print("\033[E", end='')  # Move cursor to beginning of line
            return
        
        print(f"\033[{self._bar_height - y - 1}A", end='')  # Move cursor up
        print("\033[2K", end='') # Clear line
        print(*content, end='') # Print content
        print(f"\033[{self._bar_height - y - 1}B", end='') # Move cursor down
        print("\033[E", end='')  # Move cursor to beginning of line

    def print_final_line(self) -> None:
        """Print a final line below the print bar, should be called when exiting."""
        print("", end='\n')  # New line at the bottom

class LoggingBottomBarHandler(logging.Handler):
    """A logging-compatible handle compatible with BottomBar."""
    def __init__(self, bar: BottomBar):
        """A logging-compatible handle compatible with BottomBar.
        Args:
            bar (BottomBar): The BottomBar instance to print logs to.
        """
        super().__init__()
        self.bar = bar

    def emit(self, record: logging.LogRecord) -> None:
        log_entry = self.format(record)
        self.bar.print_line(log_entry)
    
if __name__ == '__main__': 
    import time  
    # Example usage
    with BottomBar(bar_height=4) as bar:
        N = 10
        for i in range(N//2):
            time.sleep(0.2)
            bar.print_line(f"Main Line {i+1}")

        bar.print_bar_line(0, "============== BottomBar ==============")
        bar.print_bar_line(1, "Bar Line 2")
        bar.print_bar_line(2, "Bar Line 3")
        bar.print_bar_line(3, "=======================================")

        for i in range(N//2, N):
            time.sleep(0.2)
            bar.print_line(f"Main Line {i+1}")

        bar.print_bar_line(1, "Bar Line 2 bis")
        bar.print_bar_line(2, "Bar Line 3 bis")
        
    # Example usage of BottomBar with logging
    logger = logging.getLogger("BottomBarLogger")
    logger.setLevel(logging.DEBUG)
    # Add BottomBar handler
    with BottomBar(bar_height=3) as bar:
        handler = LoggingBottomBarHandler(bar)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Bar
        bar.print_bar_line(0, "=========== Logging Bottom Bar ==========")
        bar.print_bar_line(1, " Logs will appear above this bar. ")
        bar.print_bar_line(2, "=========================================")

        for i in range(2):
            logger.info(f"Info message {i+1}")
            logger.debug(f"Debug message {i+1}")
            logger.warning(f"Warning message {i+1}")
            logger.error(f"Error message {i+1}")
            time.sleep(0.2)