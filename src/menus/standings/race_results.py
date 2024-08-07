from structures import db_structures, app_structures, db_store_history
from menus import main_menu as menu
from colorama import Fore, Back
from tabulate import tabulate
green = Fore.GREEN


class RaceResults(app_structures.BaseMenu):
    def __init__(self):
        self.options = {
            "1": ("View Race Results", self.view_race_results),
            "2": ("Go Back", self.go_back),
        }

    def display_menu(self):
        print("Choose a category: \n")  # Display menu options
        for key, value in self.options.items():
            print(Fore.GREEN + f"{key}. {value[0]}")

    def get_user_choice(self):
        return super().get_user_choice()

    def call_menu(self, choice):
        if choice == "1":
            self.view_race_results()
        elif choice == "2":
            self.go_back()

    def view_race_results(self):
        app_structures.clear()
        print(green + "Choose a year (1950 - 2024): \n")
        year = input()

        try:
            year = int(year)
            if year < 1950 or year > 2024:
                print(Back.RED + "Invalid choice")
                app_structures.load(1)
                return self.view_race_results()
        except ValueError:
            print(Back.RED + "Invalid choice")
            app_structures.load(1)
            return self.view_race_results()

        races = db_structures.get_race_id_by_year(int(year))
        race_head = ["Round No.", "Race Name"]
        print(tabulate(races, headers=race_head, tablefmt="fancy_grid"))
        print(green + "Choose a race \n")
        race = input()
        try:
            results = db_structures.get_standings_after_race(
                type, int(year), int(race))
        except ValueError:
            print(Back.RED + "Invalid choice")
            app_structures.load(1)
            return self.view_race_results()
        results = db_structures.get_race_results(int(year), int(race))
        print(Fore.GREEN + "Getting Results...")
        app_structures.load(2)
        results_head = ["Position", "Driver", "Constructor",
                        "Gap to Leader", "Points", "Grid Position", "Positions Gained"]
        for r in races:
            if str(r[0]) == race:
                race_name = r[1]
                app_structures.clear()
                print(
                    green + app_structures.title_art(f"{race_name} Race Results"))
                break
        print(tabulate(results, headers=results_head, tablefmt="fancy_grid"))
        db_store_history.add_search(f"{race_name} Race Results")

    def go_back(self):
        menu.F1Menu().run()

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            if choice in self.options:
                self.call_menu(choice)
            else:
                # Display error message for invalid choice
                print(Back.RED + "Invalid choice")
                app_structures.load(1)
