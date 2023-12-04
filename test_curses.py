import curses

def display_json(stdscr, data, indent=0):
    try:
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    stdscr.addstr(f"{' ' * indent * 4}{key}:\n")
                    display_json(stdscr, value, indent + 1)
                else:
                    stdscr.addstr(f"{' ' * indent * 4}{key}: {value}\n")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    stdscr.addstr(f"{' ' * indent * 4}[{i}]:\n")
                    display_json(stdscr, item, indent + 1)
                else:
                    stdscr.addstr(f"{' ' * indent * 4}[{i}]: {item}\n")
        else:
            stdscr.addstr(f"{' ' * indent * 4}{data}\n")
    except Exception as e:
        stdscr.addstr(f"Error displaying JSON: {e}\n")

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    json_data = [
        {
            "badges": ["#1 Best Player"],
            "match_lost": 1,
            "match_win": 0,
            "username": "Eloi",
        },
        {
            "badges": [],
            "match_lost": 0,
            "match_win": 1,
            "username": "Nahuel",
        },
    ]

    # Color setup
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Keys color
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # List items color
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Values color

    stdscr.clear()
    display_json(stdscr, json_data)
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
