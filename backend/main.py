#Main.py
import users
from colorama import init, Style, Fore
init(autoreset=True)

class App():
    def __init__(self, name):
        self.name = name


    def run_main_menu(self):
        while True:
            print(Fore.CYAN+ Style.BRIGHT + f"\n***Main-Menu***\n",
                "1. Create new user\n",
                "2. Create new database\n", #Remove this option before deployment!
                "3. Choice 3\n",
                "4. Choice 4\n",
                "5. Choice 5\n",
                "6. Exit" + Fore.RESET)
            try:
                mm_choice = int(input("Please choose a menu-choice from 1-6: "))
                if mm_choice == 1:
                    users.new_user()
                elif mm_choice ==2:
                    users.create_db()
                elif mm_choice == 3:
                    print(Fore.YELLOW + "Choice 3 here")
                elif mm_choice == 4:
                    print(Fore.YELLOW + "Choice 4 here")
                elif mm_choice == 5:
                    print(Fore.YELLOW + "Choice 5 here" + Fore.RESET)
                elif mm_choice == 6:
                    print(Fore.MAGENTA + "Logging off...")
                    break
                else:
                    print(Fore.RED + "Wrong choice, please enter a choice from 1-6: ")
            except ValueError:
                print(Fore.RED + "Wrong value-input. Only integers are allowed!")

testapp = App(name="Vincent")
testapp.run_main_menu()