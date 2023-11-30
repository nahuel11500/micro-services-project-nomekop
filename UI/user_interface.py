## For UI
import curses

# For API request
import requests
session = requests.Session()
base_url = 'http://localhost:3200'

def main(stdscr):
    # Start with the authentication screen
    authentication_screen(stdscr)

    # After authentication, proceed to the main menu
    main_menu(stdscr)


####Authentification Screen 

def prompt_message(stdscr, message):
    stdscr.clear()
    stdscr.addstr(message)
    stdscr.addstr("\n\nPress any key to continue...")
    stdscr.refresh()
    stdscr.getch()

def prompt_credentials(stdscr, title):
    curses.echo()  # Enable echoing of characters
    stdscr.clear()
    stdscr.addstr(title)
    stdscr.addstr("\nUsername: ")
    username = stdscr.getstr().decode('utf-8')
    stdscr.addstr("Password: ")
    password = stdscr.getstr().decode('utf-8')
    curses.noecho()  # Disable echoing of characters
    return username, password

def authentication_screen(stdscr):
    options = ["Login", "Create Account"]
    current_selection = 0

    while True:
        stdscr.clear()
        stdscr.addstr("Authentication\n\n")
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
            
            prompt_message(stdscr, message)
            if success:
                break



################ Main Menu

def main_menu(stdscr):
    """This is the main menu for the player"""
    menu_items = ["Manage Creatures", "Interact with Players", "Community", "Matches"]
    current_selection = 0
    while True:
        stdscr.clear()
        stdscr.addstr("Main Menu\n\n")
        for idx, item in enumerate(menu_items):
            if idx == current_selection:
                stdscr.addstr(f"> {item}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {item}\n")
        
        key = stdscr.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_items) - 1:
            current_selection += 1
        elif key in [curses.KEY_ENTER, 10]:
            if current_selection == 0:
                manage_creatures(stdscr)
            elif current_selection == 1:
                interact_with_players(stdscr)
            elif current_selection == 2:
                participate_in_community(stdscr)
            elif current_selection == 3:
                participate_in_match(stdscr)


########## Sub_Menu
def manage_creatures(stdscr):
    menu_items = ["View Nomekops", "Buy Nomekops", "Go Back", "Matches"]
    current_selection = 0
    while True:
        stdscr.clear()
        stdscr.addstr("Nomekops Management\n\n")
        for idx, item in enumerate(menu_items):
            if idx == current_selection:
                stdscr.addstr(f"> {item}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {item}\n")
        
        key = stdscr.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_items) - 1:
            current_selection += 1
        elif key in [curses.KEY_ENTER, 10]:
            if current_selection == 0:
                view_nomekops(stdscr)
            elif current_selection == 1:
                buy_nomekops(stdscr)
            elif current_selection == 2:
                break



#### API CALLS


####Authentification API

def create_account(username, password):
    login_data = {'username': username, 'password': password}
    login_response = session.post(f'{base_url}/create_account', json=login_data)
    if login_response.ok:
        # Handle successful login
        response_data = login_response.json()
        session_id = response_data.get('Session_Id')
        session.cookies.set('session_id', session_id)
        return True, f"Successful Account creation with username : {username} and password : {password}"
    else:
        # Handle failed login
        return False, f"Unsuccessful connection. Reason: {login_response.text}"

def login(username, password):
    login_data = {'username': username, 'password': password}
    login_response = session.post(f'{base_url}/login', json=login_data)
    if login_response.ok:
        # Handle successful login
        response_data = login_response.json()
        session_id = response_data.get('Session_Id')
        session.cookies.set('session_id', session_id)
        return True, "Successful connection."
    else:
        # Handle failed login
        return False, f"Unsuccessful connection. Reason: {login_response.text}"






# Function placeholders for API interactions
def view_nomekops():
    pass  # API call to get creatures

def buy_nomekops():
    pass  # API call to buy a creature

def view_players():
    pass  # API call to get player list

# ... Other API interaction functions ...

def interact_with_players(stdscr):
    # Implementation of player interaction
    pass

def participate_in_community(stdscr):
    # Implementation of community participation
    pass

def participate_in_match(stdscr):
    # Implementation of match participation
    pass



curses.wrapper(main)