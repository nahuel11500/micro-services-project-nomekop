## For UI
import curses

## For json
import json

# For API request
import requests
session = requests.Session()
base_url = 'http://localhost:3200'



def create_newwin(height, width, starty, startx):
    # Create a new window
    win = curses.newwin(height, width, starty, startx)
    # Draw a border around the window
    win.box()
    # Refresh the window to show the border
    win.refresh()
    return win

def main(stdscr):
    # Clear screen and initialize curses
    stdscr.clear()
    curses.curs_set(0)  # Hide the cursor

    # Create two windows
    height, width = stdscr.getmaxyx()
    content_win = create_newwin(int(height // 1.5), width, 0, 0)
    menu_win = create_newwin(height // 3, width, int(height // 1.5), 0)

    # Start with the authentification screen
    authentification_screen(menu_win,content_win)

    # After authentification, proceed to the main menu
    main_menu(menu_win,content_win)

    # Wait for user input before exiting
    stdscr.getch()

### UI TESTs

### display functions


def prompt_message(content_win, message):
    rows, cols = content_win.getmaxyx()
    msg_win_height, msg_win_width = 5, 60
    msg_win = create_newwin(msg_win_height, msg_win_width, rows // 2 - msg_win_height // 2, cols // 2 - msg_win_width // 2)
    
    msg_win.addstr(1, 1, message)
    msg_win.refresh()
    content_win.getch()  # Wait for key press
    del msg_win

def sanitize_json(data):
    # Convert the JSON data to a string and back to JSON to remove any non-printable characters
    sanitized_data = json.loads(json.dumps(data))
    return sanitized_data

def display_json(content_win, data, indent=0):
    # Attempt to load JSON data
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        content_win.addstr(0, 0, f"Error: {e}")
        content_win.refresh()
        content_win.getch()
        return

    # Convert JSON to a formatted string
    formatted_json = json.dumps(json_data, indent=indent)

    # Initialize variables for scrolling
    max_y, max_x = content_win.getmaxyx()
    current_line = 0
    line_count = formatted_json.count('\n') + 1

    while True:
        content_win.clear()

        # Display a portion of the JSON data
        for i, line in enumerate(formatted_json.split('\n')):
            if current_line <= i < current_line + max_y:
                content_win.addstr(i - current_line, 0, line)

        content_win.refresh()

        # Handle key presses for scrolling
        key = content_win.getch()
        if key == curses.KEY_DOWN and current_line < line_count - max_y:
            current_line += 1
        elif key == curses.KEY_UP and current_line > 0:
            current_line -= 1
        elif key == ord('q'):
            break


####Authentification Screen 


    
def prompt_credentials(stdscr, title):
    rows, cols = stdscr.getmaxyx()
    curses.echo()
    stdscr.clear()
    stdscr.addstr(rows // 2 - 2, cols // 2 - len(title) // 2, title)
    stdscr.addstr(rows // 2, cols // 2 - 10, "Username: ")
    username = stdscr.getstr(rows // 2, cols // 2 + 2).decode('utf-8')
    curses.noecho()
    stdscr.addstr(rows // 2 + 1, cols // 2 - 10, "Password: ")
    curses.cbreak()
    password = ''
    while True:
        ch = stdscr.getch()
        if ch == 10:  # Enter key
            break
        elif ch == 127:  # Backspace
            password = password[:-1]
        else:
            password += chr(ch)
    curses.echo()
    return username, password

def prompt_name(stdscr, title, argument_name):
    rows, cols = stdscr.getmaxyx()
    curses.echo()
    stdscr.clear()
    stdscr.addstr(rows // 2 - 2, cols // 2 - len(title) // 2, title)
    stdscr.addstr(rows // 2, cols // 2 - len(argument_name), argument_name)
    name = stdscr.getstr(rows // 2, cols // 2 + 2).decode('utf-8')
    curses.cbreak()
    return name

def authentification_screen(stdscr,content_win):
    options = ["Login", "Create Account"]
    current_selection = 0

    while True:
        stdscr.clear()
        stdscr.addstr("Authentification\n\n")
        for idx, option in enumerate(options):
            if idx == current_selection:
                stdscr.addstr(f"> {option}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {option}\n")
        
        key = stdscr.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(options) - 1:
            current_selection += 1
        elif key in [curses.KEY_ENTER, 10]:
            username, password = prompt_credentials(stdscr, options[current_selection])
            success, message = login(username, password) if current_selection == 0 else create_account(username, password)
            
            prompt_message(content_win, message)
            if success:
                break



################ Main Menu

def main_menu(menu_win,content_win):
    """This is the main menu for the player"""
    menu_items = ["Manage Nomekops", "Interact with Players", "Community", "Matches"]
    current_selection = 0

    # Enable keypad mode
    menu_win.keypad(True)
    rows, cols = menu_win.getmaxyx()
    while True:
        # Clear the window
        menu_win.clear()

        menu_win.addstr("Main Menu\n\n")
        for idx, item in enumerate(menu_items):
            if idx == current_selection:
                menu_win.addstr(idx+2, cols // 2 - 10,f"> {item}\n", curses.A_REVERSE)
            else:
                menu_win.addstr(idx+2, cols // 2 - 10,f"  {item}\n")

        # Refresh the window to apply changes
        menu_win.refresh()

        key = menu_win.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_items) - 1:
            current_selection += 1
        elif key in [curses.KEY_ENTER, 10]:
            if current_selection == 0:
                manage_nomekops(menu_win,content_win)
            elif current_selection == 1:
                interact_with_players(menu_win,content_win)
            elif current_selection == 2:
                participate_in_community(menu_win,content_win)
            elif current_selection == 3:
                participate_in_match(menu_win,content_win)


########################### Sub_Menu PLayer #########################
def manage_nomekops(stdscr,content_win):
    menu_items = ["View my nomekops", "View store nomekops","Buy nomekops", "View nomekop stats", "Go back"]
    current_selection = 0
    rows, cols = stdscr.getmaxyx()

    while True:
        stdscr.clear()
        stdscr.addstr("Nomekops Management\n\n")
        for idx, item in enumerate(menu_items):
            if idx == current_selection:
                stdscr.addstr(idx+2, cols // 2 - 10,f"> {item}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(idx+2, cols // 2 - 10,f"  {item}\n")
        
        key = stdscr.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_items) - 1:
            current_selection += 1
        elif key in [curses.KEY_ENTER, 10]:
            if current_selection == 0:
                view_nomekops(content_win)
            if current_selection == 1:
                view_store_nomekops(content_win)
            elif current_selection == 2:
                nomekop_name_buy = prompt_name(stdscr, "Nomekop to buy", "Nomekop name: ")
                buy_nomekops(content_win, session.cookies.get("session_id"), nomekop_name_buy)
            elif current_selection == 3:
                nomekop_name = prompt_name(stdscr, "Nomekop stats", "Nomekop name: ")
                view_nomekop_stats(content_win, nomekop_name)
            elif current_selection == 4:
                break


def interact_with_players(menu_win,content_win):
    # Implementation of player interaction
    menu_items = ["See the list of players", "Send a message to a player","See my private messages","Go Back"]
    current_selection = 0
    rows, cols = menu_win.getmaxyx()

    while True:
        menu_win.clear()
        menu_win.addstr("Player Interaction\n\n")
        for idx, item in enumerate(menu_items):
            if idx == current_selection:
                menu_win.addstr(idx+2, cols // 2 - 10,f"> {item}\n", curses.A_REVERSE)
            else:
                menu_win.addstr(idx+2, cols // 2 - 10,f"  {item}\n")
        
        key = menu_win.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_items) - 1:
            current_selection += 1
        elif key in [curses.KEY_ENTER, 10]:
            if current_selection == 0:
                view_players(content_win)
            elif current_selection == 1:
                send_message(content_win)
            elif current_selection == 2:
                see_message(content_win)
            elif current_selection == 3:
                break

def participate_in_community(stdscr,content_win):
    # Implementation of community participation
    menu_items = ["See my invites","See match list","see match details","See round details","Go Back"]
    current_selection = 0
    rows, cols = stdscr.getmaxyx()
    
    while True:
        stdscr.clear()
        stdscr.addstr("Community\n\n")
        for idx, item in enumerate(menu_items):
            if idx == current_selection:
                stdscr.addstr(idx+2, cols // 2 - 10,f"> {item}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(idx+2, cols // 2 - 10,f"  {item}\n")
        
        key = stdscr.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_items) - 1:
            current_selection += 1
        elif key in [curses.KEY_ENTER, 10]:
            if current_selection == 0:
                view_invites(content_win)
            elif current_selection == 1:
                see_match(content_win)
            elif current_selection == 2:
                see_match_details(content_win)
            elif current_selection == 3:
                see_round_details(content_win)
            elif current_selection == 4:
                break

def participate_in_match(stdscr,content_win):
    # Implementation of match participation
    menu_items = ["Join a match","Create a match", "Send a nomekop to the arena","see match details","See round details","Go Back"]
    current_selection = 0
    rows, cols = stdscr.getmaxyx()
    while True:
        stdscr.clear()
        stdscr.addstr("Match\n\n")
        for idx, item in enumerate(menu_items):
            if idx == current_selection:
                stdscr.addstr(idx+2, cols // 2 - 10,f"> {item}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(idx+2, cols // 2 - 10,f"  {item}\n")
        
        key = stdscr.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_items) - 1:
            current_selection += 1
        elif key in [curses.KEY_ENTER, 10]:
            if current_selection == 0:
                join_match(content_win)
            elif current_selection == 1:
                create_match(content_win)
            elif current_selection == 2:
                send_nomepok(content_win)
            elif current_selection == 3:
                see_match_details(content_win)
            elif current_selection == 4:
                see_round_details(content_win)
            elif current_selection == 5:
                break


############## Sub Sub Menu

########## API CALL 2)a)
# Function placeholders for API interactions
def view_store_nomekops(stdscr):
    nomekops = session.get(f'{base_url}/store/getNomekopsPrices').text
    display_json(stdscr,sanitize_json(nomekops))

def view_nomekop_stats(stdscr, nomekop):
    nomekop_stats = session.get(f'{base_url}/nomekops/nomekopstats/{nomekop}').text
    display_json(stdscr,sanitize_json(nomekop_stats))

def buy_nomekops(stdscr, player, nomekop):
    nomekop_msg = session.put(f'{base_url}/player/buyNomekop/{nomekop}').text
    display_json(stdscr, sanitize_json(nomekop_msg))

########## API CALL 2)b)
def view_players(stdscr):
    players= session.get(f'{base_url}/player/get_info_other_player').text
    display_json(stdscr,sanitize_json(players))

def view_nomekops(stdscr):
    pass

def send_message(stdsrc):
    pass

def see_message(stdsrc):
    pass

########## API CALL 2)c)

def view_invites(stdscr):
    pass

def create_match(stdscr):
    pass

def see_match(stdscr):
    pass

def see_match_details(stdscr):
    pass

def see_round_details(stdscr):
    pass
                
########## API CALL 2)d)

def join_match(stdscr):
    pass

def send_nomepok(stdscr):
    pass


############################# API CALLS


####Authentification API

def create_account(username, password):
    try:
        login_data = {'username': username, 'password': password}
        login_response = session.post(f'{base_url}/create_account', json=login_data)
        if login_response.ok:
            response_data = login_response.json()
            session_id = response_data.get('Session_Id')
            session.cookies.set('session_id', session_id)
            return True, f"Successful Account creation with username: {username}"
        else:
            return False, f"Unsuccessful connection. Reason: {login_response.text}"
    except requests.RequestException as e:
        return False, f"Error connecting to server: {e}"

def login(username, password):
    try:
        login_data = {'username': username, 'password': password}
        login_response = session.post(f'{base_url}/login', json=login_data)
        if login_response.ok:
            response_data = login_response.json()
            session_id = response_data.get('Session_Id')
            session.cookies.set('session_id', session_id)
            return True, "Successful connection."
        else:
            return False, f"Unsuccessful connection. Reason: {login_response.text}"
    except requests.RequestException as e:
        return False, f"Error connecting to server: {e}"


############################ Sub Menu API ###########








##### WRAP
curses.wrapper(main)