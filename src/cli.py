from typing import Optional

def get_int(msg: Optional[str]) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print('Please enter an integer')
