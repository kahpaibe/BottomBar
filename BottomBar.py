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

    def print(self, content_str: str, **kwargs: Any) -> None:
        """Prints given string on the top part.
        
        Args:
            content_str (str): The string to print above the bottom bar. Can contain new lines.
            **kwargs (Any): Additional keyword arguments for the print function.

        Note:
            The 'end' parameter is reserved and cannot be used.
        """
        assert "end" not in kwargs, "end parameter is reserved and cannot be used."
        n = content_str.count('\n') + 1
        
        # Note: Merging several print statements to avoid flickering
        # Cursor manipulation to insert n lines above the bar
        str_manip_start = ""
        str_manip_start += "\n"*n                              # Add new lines at the bottom
        str_manip_start += f"\033[{self._bar_height + n - 1}A" # Move cursor up
        str_manip_start += f"\033[{n}L"                        # Insert n lines
        
        # Cursor manipulation to go back to initial cursor position
        str_manip_end = ""
        str_manip_end += f"\033[{self._bar_height}B"  # Move cursor
        str_manip_end += "\033[E"                     # Move cursor to beginning of line
        
        # Final string payload
        payload_str = str_manip_start + content_str + str_manip_end
        print(payload_str, end='', **kwargs)

    def print_bar_line(self, y: int, content_str: str) -> None:
        """Prints a line in the print bar at the specified y position of the bar.
        Args:
            y (int): The line number in the print bar (0-indexed, from top).
            content_str (str): The content to print.
        
        Note:
            content_str must be a single line without new lines.
        """
        assert 0 <= y < self._bar_height, "y must be within the print bar height"
        assert '\n' not in content_str, "content_str must be a single line without new lines"

        if y == self._bar_height - 1: # Last line special case
            payload_str = "\033[2K" + content_str + "\033[E"
            print(payload_str, end='')
            return
        
        payload_str = ""
        payload_str += f"\033[{self._bar_height - y - 1}A" # Move cursor up
        payload_str += "\033[2K"                           # Clear line
        payload_str += content_str                         # Add content
        payload_str += f"\033[{self._bar_height - y - 1}B" # Move cursor down
        payload_str += "\033[E"                            # Move cursor to beginning of line
        print(payload_str, end='')

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
        self.bar.print(log_entry)
    
if __name__ == '__main__': 
    import time  
    # Example usage
    with BottomBar(bar_height=4) as bar:
        N = 100

        bar.print_bar_line(0, "============== BottomBar ==============")
        bar.print_bar_line(1, "Bar Line 2")
        bar.print_bar_line(2, "Bar Line 3")
        bar.print_bar_line(3, "=======================================")

        for i in range(N//2, N):
            time.sleep(0.2)
            bar.print("\n".join([f"Main Line {i+1}, j={j}" for j in range(3)]))

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