import sqlite3

class MusicDbManager:
    """
    This class manages database.
    """
    def __init__(self):
        self._connect = sqlite3.connect('database/music.db')
        self._cursor = self._connect.cursor()

    def __del__(self):
        self._connect.commit()
        self._connect.close()

    def create_db(self):
        create_table = """
            CREATE TABLE IF NOT EXISTS music(
                id INTEGER PRIMARY KEY,
                group_name TEXT,
                group_link TEXT,
                genre TEXT
            )
        """
        self._cursor.execute(create_table)

    def write_all_data_to_db(self, group_name: str, group_link: str, genre: str):
        self._cursor.execute(
            """INSERT INTO music(group_name, group_link, genre)
               VALUES(?, ?, ?)
            """,
            (group_name, group_link, genre)
            )

    def show_all_groupnames_or_genges(self, value: str) -> list[str] | set[str]:
        all_data = self._cursor.execute(
            f"""SELECT {value} FROM music"""
        ).fetchall()

        names_list = []

        match value:
            case 'group_name':
                names_list = [name for tpl in all_data for name in tpl]
            case 'genre':
                names_list = {name for tpl in all_data for name in tpl}

        return names_list

    def group_selection(self, choice_of_user: str) -> str:
        user_selected_group = self._cursor.execute(
            """
            SELECT group_link FROM music WHERE group_name = ?
            """,
            (choice_of_user,)
        ).fetchone()
        return user_selected_group[0]

    def get_groups_of_selected_genre(self, *choice_of_user):
        user_selected_group = self._cursor.execute(
                """
                SELECT group_name FROM music WHERE genre = ?
                """,
                (choice_of_user)
                ).fetchall()
        groups_of_chose_genre = [group for i in user_selected_group for group in i]
        return groups_of_chose_genre

