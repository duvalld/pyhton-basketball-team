import sqlite3

class DatabaseManager:
    """ A class for managing SQLITE database operations """
    def __init__(self):
        self._database_name = "rmbc_db.db"

    def open_db(self):
        """Open a connection to the database."""
        self._conn = sqlite3.connect(self._database_name)
        self._cursor = self._conn.cursor()

    def close_db(self):
        """Close the database connection."""
        self._cursor.close()
        self._conn.close()

    def create_table(self, query):
        """Create a table in the database."""
        self.open_db()
        self._cursor.execute(query)
        self._conn.commit()
        self.close_db()

    def insert_record(self, query, col_values, table):
        """Insert a record into the specified table."""
        self.open_db()
        self._cursor.execute(query, col_values)
        self._conn.commit()
        print(f"{table} successfuly added!")

    def entry_checker(self, table, column, id):
        """
        Check if an entry with the given ID exists in the specified table.

        Returns:
            bool: True if the entry exists, False otherwise.
        """
        query = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {
            column} = ? LIMIT 1)"
        try:
            self.open_db()
            self._cursor.execute(query, (id))
            result = self._cursor.fetchone()[0]
            return bool(result)
        except sqlite3.Error as e:
            print(f"Error checking entry: {e}")
            return False
        finally:
            self.close_db()
            
db_manager = DatabaseManager()
cities_rep_table_query = """
    CREATE TABLE IF NOT EXISTS cities(
        id INTEGER PRIMARY KEY
        ,city TEXT NOT NULL
    )
"""
teams_table_query = """
    CREATE TABLE IF NOT EXISTS teams(
        id INTEGER PRIMARY KEY
        ,team TEXT NOT NULL
        ,city_id INTEGER NOT NULL
    )
"""
players_table_query = """
    CREATE TABLE IF NOT EXISTS players(
        id INTEGER PRIMARY KEY
        ,name TEXT NOT NULL
        ,team_id INTEGER NOT NULL
    )
"""
coaches_table_query = """
    CREATE TABLE IF NOT EXISTS coaches(
        id INTEGER PRIMARY KEY
        ,name TEXT NOT NULL
        ,role TEXT NOT NULL
        ,team_id INTEGER NOT NULL
    )
"""
seasons_table_query = """
    CREATE TABLE IF NOT EXISTS seasons(
        id INTEGER PRIMARY KEY
        ,season TEXT NOT NULL
    )
"""
games_item_table_query = """
    CREATE TABLE IF NOT EXISTS games(
        id INTEGER PRIMARY KEY
        ,season_id INTEGER NOT NULL
        ,home_team_id INTEGER NOT NULL
        ,visitor_team_id INTEGER NOT NULL
        ,result TEXT
    )
"""
table_list = [
    cities_rep_table_query
    ,teams_table_query
    ,players_table_query
    ,coaches_table_query
    ,seasons_table_query
    ,games_item_table_query
]

for table in table_list:
    db_manager.create_table(table)

def show_cities():
    db_manager.open_db()
    sql_query = """
        SELECT
            id
            ,city
        FROM cities
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'City':<20}"
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_city) = row
        print(f"{row_id:>4} | {row_city:<20}")
    db_manager.close_db()
    
def show_teams():
    db_manager.open_db()
    sql_query = """
        SELECT
            teams.id
            ,teams.team
            ,cities.city
            ,(SELECT COUNT(*) FROM players WHERE team_id = teams.id) as player_count
            ,(SELECT COUNT(*) FROM coaches WHERE team_id = teams.id) as count_count
        FROM teams
        LEFT JOIN cities 
        ON teams.city_id = cities.id
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'City':<20} | {'Team':<20} | {'Players':<10} | {'Coaches':<10} "
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_team, row_city, row_player_count, row_coach_count) = row
        print(f"{row_id:>4} | {row_city:<20} | {row_team:<20} | {row_player_count:<10} | {row_coach_count:<10}")
    db_manager.close_db()

def show_players():
    db_manager.open_db()
    sql_query = """
        SELECT
            players.id
            ,players.name
            ,teams.team
        FROM players
        LEFT JOIN teams
        ON players.team_id = teams.id
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'Team':<20} | {'Player':<20}"
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_player, row_team) = row
        print(f"{row_id:>4} | {row_team:<20} | {row_player:<20}")
    db_manager.close_db()

def show_coaches():
    db_manager.open_db()
    sql_query = """
        SELECT
            coaches.id
            ,coaches.name
            ,teams.team
            ,coaches.role
        FROM coaches
        LEFT JOIN teams ON coaches.team_id = teams.id
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'Team':<20} | {'Coach':<20} | {'Role':<20}"
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_coach, row_team, row_role) = row
        print(f"{row_id:>4} | {row_team:<20} | {row_coach:<20} | {row_role:<20}")
    db_manager.close_db()

def show_seasons():
    db_manager.open_db()
    sql_query = """
        SELECT
            id
            ,season
        FROM seasons
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'Seasons':<20} "
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_season) = row
        print(f"{row_id:>4} | {row_season:<20} ")
    db_manager.close_db()

def show_games():
    db_manager.open_db()
    sql_query = """
        SELECT
            games.id
            ,seasons.season
            ,(SELECT team FROM teams WHERE id = games.home_team_id) as home_team
            ,(SELECT team FROM teams WHERE id = games.visitor_team_id) as visitor_team
            ,games.result
        FROM games
        LEFT JOIN seasons
        ON games.season_id = seasons.id
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'Season':<20} | {'Home Team':<20} | {'Vistor Team':<20}  | {'Result':<20} "
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_season, row_home, row_visitor, row_result) = row
        print(f"{row_id:>4} | {row_season:<20} | {row_home:<20} | {row_visitor:<20}  | {row_result if row_result != None else '':<20} ")
    db_manager.close_db()
    

program_running = True
while program_running:
    main_menu_input = int(input("Enter 1: Cities, 2: Teams, 3: Players, 4: Coaches, 5: Seasons, 6: Games : "))
    if main_menu_input == 1:
        print("Cities")
        city_men_input = int(input("Enter 1: View, 2: Add New : "))
        if city_men_input == 1:
            show_cities()
        elif city_men_input == 2:
            try:
                city_input = input("City: ")
                db_manager.open_db()
                db_manager.insert_record("INSERT INTO cities (city) VALUES (?)", (city_input,), "City")
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 2:
        print("Teams")
        team_menu_input = int(input("Enter 1: View, 2: Add New : "))
        if team_menu_input == 1:
            show_teams()
        elif team_menu_input == 2:
            try:
                team_input = input("Team: ")
                show_cities()
                city_input = input("City (ID): ")
                db_manager.open_db()
                db_manager.insert_record("INSERT INTO teams (team, city_id) VALUES (?, ?)", (team_input, city_input), "Team")
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 3:
        print("Players")
        player_menu_input = int(input("Enter 1: View, 2: Add New : "))
        if player_menu_input == 1:
            show_players()
        elif player_menu_input == 2:
            try:
                player_input = input("Player: ")
                show_teams()
                team_input = input("Team (ID): ")
                db_manager.open_db()
                db_manager.insert_record("INSERT INTO players (name, team_id) VALUES (?, ?)", (player_input, team_input), "Player")
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 4:
        print("Coaches")
        coach_menu_input = int(input("Enter 1: View, 2: Add New : "))
        if coach_menu_input == 1:
            show_coaches()
        elif coach_menu_input == 2:
            try:
                coach_input = input("Coach: ")
                role_input = input("Role: ")
                show_teams()
                team_input = input("Team (ID): ")
                db_manager.open_db()
                db_manager.insert_record("INSERT INTO coaches (name, role, team_id) VALUES (?, ?, ?)", (coach_input, role_input, team_input), "Coach")
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 5:
        print("Season")
        season_menu_input = int(input("Enter 1: View, 2: Add New : "))
        if season_menu_input == 1:
            show_seasons()
        elif season_menu_input == 2:
            try:
                season_input = input("Season: ")
                db_manager.open_db()
                db_manager._cursor.execute("INSERT INTO seasons (season) VALUES (?)", (season_input,))
                db_manager._conn.commit()
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 6:
        print("Games")
        game_menu_input = int(input("Enter 1: View, 2: Add New : "))
        if game_menu_input == 1:
            show_games()
        elif game_menu_input == 2:
            try:
                show_seasons()
                season_input = input("Season (ID): ")
                show_teams()
                home_team_input = input("Home Team (ID): ")
                show_teams()
                visitor_team_input = input("Visitor Team (ID): ")
                db_manager.open_db()
                db_manager._cursor.execute("INSERT INTO games (season_id, home_team_id, visitor_team_id) VALUES (?, ?, ?)", (season_input, home_team_input, visitor_team_input))
                db_manager._conn.commit()
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 7:
        program_running = False
