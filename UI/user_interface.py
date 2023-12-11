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

def display_json(content_win, data, indent=2):
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        content_win.clear()
        content_win.addstr(0, 0, f"Error: {str(e)}")
        content_win.refresh()
        content_win.getch()
        return

    formatted_json = json.dumps(json_data, indent=indent).split('\n')
    max_y, max_x = content_win.getmaxyx()
    current_line = 0
    line_count = len(formatted_json)

    while True:
        content_win.clear()
        content_win.addstr(0, 0, "Viewer - Press q to go back. Use arrow keys to scroll.")

        for i in range(1, max_y - 1):  # Adjusted loop to start from 1, leaving space for the header
            if current_line + i < line_count:
                line = formatted_json[current_line + i - 1]
                content_win.addstr(i, 0, line[:max_x-1])

        status_line = f"Line {current_line + 1} of {line_count}"
        content_win.addstr(max_y-1, 0, status_line)

        content_win.refresh()

        key = content_win.getch()
        if key == curses.KEY_DOWN and current_line < line_count - max_y + 2:
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
        elif ch == 8:  # Backspace
            password = password[:-1]
            # Remove the last asterisk
            stdscr.addstr(rows // 2 + 1, cols // 2 + len(password)+2, " ")
            stdscr.move(rows // 2 + 1, cols // 2 + len(password) + 1)
        else:
            password += chr(ch)
            stdscr.addstr(rows // 2 + 1, cols // 2 + len(password) + 1,"*")  # Display an asterisk instead of the character
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

def prompt_names(stdscr, title):
    """Prompt for match number and nomekop based on a title."""
    
    rows, cols = stdscr.getmaxyx()
    curses.echo()
    stdscr.clear()

    # Display title
    title_x = max(0, cols // 2 - len(title) // 2)
    stdscr.addstr(rows // 2 - 2, title_x, title)

    # Prompt for Match number
    match_prompt = "Match number: "
    match_prompt_x = max(0, cols // 2 - len(match_prompt) // 2)
    stdscr.addstr(rows // 2, match_prompt_x, match_prompt)
    curses.echo()
    match_number = stdscr.getstr(rows // 2, match_prompt_x + len(match_prompt)).decode('utf-8')
    curses.noecho()

    stdscr.refresh()
    # Prompt for Nomekop
    nomekop_prompt = "Nomekop: "
    nomekop_prompt_x = max(0, cols // 2 - len(nomekop_prompt) // 2)
    stdscr.addstr(rows // 2 + 1, nomekop_prompt_x, nomekop_prompt)
    curses.echo()
    nomekop = stdscr.getstr(rows // 2 + 1, nomekop_prompt_x + len(nomekop_prompt)).decode('utf-8')
    curses.noecho()

    return (match_number, nomekop)



def authentification_screen(stdscr,content_win):
    options = ["Login", "Create Account"]
    current_selection = 0
    # Enable keypad mode
    content_win.keypad(True)
    while True:
        stdscr.clear()
        stdscr.addstr("Authentification\n\n")
        for idx, option in enumerate(options):
            if idx == current_selection:
                stdscr.addstr(f"> {option}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {option}\n")
        
        stdscr.refresh()
        key = content_win.getch()
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
                content_win.clear()
                content_win.refresh()
                manage_nomekops(menu_win,content_win)
            elif current_selection == 1:
                content_win.clear()
                content_win.refresh()
                interact_with_players(menu_win,content_win)
            elif current_selection == 2:
                content_win.clear()
                content_win.refresh()
                participate_in_community(menu_win,content_win)
            elif current_selection == 3:
                content_win.clear()
                content_win.refresh()
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
                content_win.clear()
                content_win.refresh()
                view_nomekops(content_win)
            if current_selection == 1:
                content_win.clear()
                content_win.refresh()
                view_store_nomekops(content_win)
            elif current_selection == 2:
                content_win.clear()
                content_win.refresh()
                buy_nomekops(content_win, session.cookies.get("session_id"), "Tulup")
            elif current_selection == 3:
                content_win.clear()
                content_win.refresh()
                nomekop_name = prompt_name(stdscr,"Nomekop name:  ","Nomekop stats")
                view_nomekop_stats(content_win, nomekop_name)
            elif current_selection == 4:
                content_win.clear()
                content_win.refresh()
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
                content_win.clear()
                content_win.refresh()
                view_players(content_win)
            elif current_selection == 1:
                content_win.clear()
                content_win.refresh()
                send_message(content_win)
            elif current_selection == 2:
                content_win.clear()
                content_win.refresh()
                see_message(content_win)
            elif current_selection == 3:
                content_win.clear()
                content_win.refresh()
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
                content_win.clear()
                content_win.refresh()
                view_invites(content_win)
            elif current_selection == 1:
                content_win.clear()
                content_win.refresh()
                see_match(content_win)
            elif current_selection == 2:
                content_win.clear()
                content_win.refresh()
                see_match_details(content_win)
            elif current_selection == 3:
                content_win.clear()
                content_win.refresh()
                see_round_details(content_win)
            elif current_selection == 4:
                content_win.clear()
                content_win.refresh()
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
                content_win.clear()
                join_match(content_win)
            elif current_selection == 1:
                content_win.clear()
                content_win.refresh()
                player_name =prompt_name(stdscr,"Player name:  ","Player selection")
                create_match(content_win,player_name)
            elif current_selection == 2:
                content_win.clear()
                content_win.refresh()
                numbered_players = view_nomekops_and_match(content_win)
                (match_number,nomekop) =prompt_names(stdscr,"Pokemon to send to the arena")
                send_nomepok(match_number,nomekop,numbered_players,content_win)
            elif current_selection == 3:
                content_win.clear()
                content_win.refresh()
                see_match_details(content_win)
            elif current_selection == 4:
                content_win.clear()
                content_win.refresh()
                see_round_details(content_win)
            elif current_selection == 5:
                content_win.clear()
                content_win.refresh()
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
    nomekops_player = session.get(f'{base_url}/player/get_nomekops').text
    display_json(stdscr,sanitize_json(nomekops_player))
    pass

def send_message(stdsrc):
    pass

def see_message(stdsrc):
    pass

########## API CALL 2)c)

def view_invites(stdscr):
    pass

def create_match(stdscr,player_name):
    match_msg = session.post(f'{base_url}/player/match/{player_name}').text
    display_json(stdscr,sanitize_json(match_msg))

def see_match(stdscr):
    pass

def see_match_details(stdscr):
    pass

def see_round_details(stdscr):
    pass
                
########## API CALL 2)d)

def join_match(stdscr):
    pass

def view_nomekops_and_match(stdscr):
    # Retrieve match list data
    match_lists_response = session.get(f'{base_url}/matchs')
    match_lists = match_lists_response.json()  # Convert response to JSON

    # Check if match_lists is a list and iterate through it if it is
    numbered_players = []
    numbered_players_dic = {}
    if isinstance(match_lists, list):
        for index, match in enumerate(match_lists):
            if "players" in match:
                # Append player name with a number
                player_name_with_number = f'{index + 1} : {match["players"]}'
                numbered_players.append(player_name_with_number)
                numbered_players_dic[index + 1] = match["players"]
    else:
        raise TypeError("Expected a list in the JSON response")

    # Retrieve pokemon list data
    pokemon_list_response = session.get(f'{base_url}/player/get_nomekops')
    pokemon_list = pokemon_list_response.json()  # Convert response to JSON

    # Combine both JSON data
    combined_data = {
        'match_lists': numbered_players,
        'pokemon_list': pokemon_list
    }
   
    display_json(stdscr, sanitize_json(json.dumps(combined_data, indent=4)))
    return numbered_players_dic


def send_nomepok(match_number,nomekop,numbered_players_dic,content_window):
    print("hey")
    print(numbered_players_dic)
    print("hey")
    player_name,player_request = numbered_players_dic[int(match_number)]
    match_lists_response = session.post(f'{base_url}/match/add_nomekop/{player_name}/{player_request}/{nomekop}')
    prompt_message(content_window,match_lists_response.text)

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