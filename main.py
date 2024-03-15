"""Työ ajanhallinta skripti"""

import maskpass
import colors
import functions

if __name__ == "__main__":
    LOGGED_IN = False
    ADMIN_ID = '1'
    USER_ID = None

    while True:
        # Display the menu
        print(
            f"""{colors.BLUEBOX} AJANHALLINTA  [-][=]{colors.RBWT}[X]{colors.RESET}
{colors.BLUEBOX} {colors.RESET}{colors.RYBG}* 0. Luo käyttäjä     {colors.BLUEBOX} {colors.RESET}
{colors.BLUEBOX} {colors.RESET}{colors.GYBG}* 1. Poista käyttäjä  {colors.BLUEBOX} {colors.RESET}
{colors.BLUEBOX} {colors.RESET}{colors.YYBG}* 2. Kirjaudu sisään  {colors.BLUEBOX} {colors.RESET}
{colors.BLUEBOX} {colors.RESET}{colors.BYBG}* 3. Kirjaudu ulos    {colors.BLUEBOX} {colors.RESET}
{colors.BLUEBOX} {colors.RESET}{colors.MYBG}* 4. Tarkista status  {colors.BLUEBOX} {colors.RESET}
{colors.BLUEBOX} {colors.RESET}{colors.CYBG}* 5. Poistu           {colors.BLUEBOX} {colors.RESET}"""
        )

        # Get user choice
        choice = input(
            f"{colors.BLUEBOX} {colors.RESET}{colors.BTWBG}VALITSE TOIMINTO: {colors.RESET}"
        )

        if choice == '0':
            input_user = input("Käyttäjätunnus: ")
            input_name = input("Nimi: ")
            input_pass = maskpass.askpass(prompt="Salasana: ")
            functions.create_user(input_user, input_name, input_pass)
        elif choice == '1':
            if LOGGED_IN:
                if USER_ID == ADMIN_ID:
                    user_id_delete = input("Poistettavan käyttäjätunnus: ")
                    functions.del_user(ADMIN_ID, user_id_delete)
                else:
                    print("Vain pääkäyttäjällä on oikeus poistaa käyttäjiä.")
            else:
                print("Et ole kirjautunut sisään.")
        elif choice == '2':
            input_user = input("Käyttäjätunnus: ")
            input_pass = maskpass.askpass(prompt="Salasana: ")
            logged_user_id, session_token = functions.login(input_user, input_pass)
            if logged_user_id:
                LOGGED_IN = True
                USER_ID = logged_user_id
        elif choice == '3':
            if LOGGED_IN:
                functions.logout(input_user)
                LOGGED_IN = False
                USER_ID = None
            else:
                print("Et ole kirjautunut sisään.")
        elif choice == '4':
            input_status = input("Käyttäjätunnus: ")
            functions.check_status(input_status)
        elif choice == '5':
            print("Poistutaan...")
            break
        else:
            print("Virheellinen valinta. Valitse 0, 1, 2, 3, 4 tai 5.")
