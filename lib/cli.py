import time
from session import session
from helpers import Banner, Prompt, SignUp
from simple_term_menu import TerminalMenu
from prettycli import red, yellow
from datetime import datetime, date
from models import User, Task

banner = Banner()
prompt = Prompt()

class Cli:
    def __init__(self):
        self.current_user = None
        self.page_is_main = False

    def start(self):
        self.clear_screen()
        banner.welcome()
        options = []
        if self.current_user:
            options.extend(
                ["New Task", "My Tasks", "Completed", "Task By Date", "Logout"]
            )
            print(yellow(f"Welcome, {self.current_user.username}! 👋😃\n"))
        else:
            options.extend(["Sign Up", "Login"])
        menu_selection = self.render_options(options)
        self.handle_selection(menu_selection)

    def clear_screen(self):
        print("\n" * 40)

    def render_options(self, options):
        if not self.current_user:
            options.append("Quit")
        if self.page_is_main:
            options.append("Exit")

        menu = TerminalMenu(options)
        selection = menu.show()
        return options[selection]

    def render_main_menu(self):
        self.page_is_main = True
        self.clear_screen()
        banner.main_menu()
        print(yellow(f"Welcome, {self.current_user.username}! 👋😃\n"))
        options = ["New Task", "My Tasks", "Completed", "Task By Date"]
        menu_selection = self.render_options(options)
        self.page_is_main = False
        self.handle_selection(menu_selection)

    def render_my_tasks(self):
        self.clear_screen()
        banner.my_tasks()
        active_tasks = [
            f"{task.id} - {task.description}"
            for task in self.current_user.tasks
            if task.complete == False
        ]
        active_tasks.append("Back")
        if len(active_tasks) == 1:
            print(yellow("You do not have any active tasks.").bold())
            time.sleep(2)
            self.render_main_menu()
            return
        selection = self.render_options(active_tasks)

        if selection == "Back":
            self.render_main_menu()
        else:
            selection_id = int(selection.split("-")[0].strip())
            self.render_task_options(
                session.query(Task).get(selection_id), "render_my_tasks"
            )

    def render_completed_tasks(self):
        self.clear_screen()
        banner.completed_tasks()
        completed = [
            f"{task.id} - {task.description}"
            for task in self.current_user.tasks
            if task.complete == True
        ]
        completed.append("Back")
        if len(completed) == 1:
            print(yellow("You do not have any completed tasks.").bold())
            time.sleep(2)
            self.render_main_menu()
            return
        selection = self.render_options(completed)

        if selection == "Back":
            self.render_main_menu()
        else:
            selection_id = int(selection.split("-")[0].strip())
            self.render_task_options(
                session.query(Task).get(selection_id), "render_completed_tasks"
            )

    def render_tasks_by_date(self):
        self.clear_screen()
        banner.tasks_by_date()
        user_tasks_query = (
            session.query(Task)
            .filter(Task.user_id == self.current_user.id)
            .order_by(Task.due_date.desc())
            .all()
        )
        user_tasks = [
            f"{task.id} - {task.description} - Due: {str(task.due_date).split(' ')[0]}"
            for task in user_tasks_query
            if task.complete == False
        ]
        user_tasks.append("Back")
        if len(user_tasks) == 1:
            print(yellow("You do not have any tasks.").bold())
            time.sleep(2)
            self.render_main_menu()
            return
        selection = self.render_options(user_tasks)

        if selection == "Back":
            self.render_main_menu()
        else:
            selection_id = int(selection.split("-")[0].strip())
            self.render_task_options(
                session.query(Task).get(selection_id), "render_tasks_by_date"
            )

    def render_task_options(self, task, page):
        self.clear_screen()
        print(task.description)
        options = ["Delete", "Back"]
        if not task.complete:
            options.extend(["Mark Complete", "Update"])
        selection = self.render_options(options)
        if selection == "Mark Complete":
            task.mark_complete(session)
            self.render_completed_tasks()
        if selection == "Update":
            description = Task.get_description()
            task.update(session, description)
            self.render_my_tasks()
        if selection == "Delete":
            task.delete(session)
            self.render_completed_tasks()
        if selection == "Back":
            if page == "render_my_tasks":
                self.render_my_tasks()
            elif page == "render_tasks_by_date":
                self.render_tasks_by_date()
            elif page == "render_completed_tasks":
                self.render_completed_tasks()

    def handle_selection(self, selection):
        switch = {
            "Sign Up": self.handle_sign_up,
            "Login": self.handle_login,
            "Logout": self.handle_logout,
            "New Task": self.handle_new_task,
            "My Tasks": self.render_my_tasks,
            "Completed": self.render_completed_tasks,
            "Task By Date": self.render_tasks_by_date,
            "Exit": self.exit,
            "Quit": self.quit,
        }
        switch[selection]()

    def handle_sign_up(self):
        sign_up = SignUp()

        first_name = sign_up.get_first_name()
        last_name = sign_up.get_last_name()
        username = sign_up.get_username(session, User)

        self.current_user = User.save_user(
            session, first_name=first_name, last_name=last_name, username=username
        )

        self.render_main_menu()

    def handle_login(self):
        username = prompt.ask("What is your username?")
        user = User.find_by(session, username=username)
        if user:
            self.current_user = user
            self.render_main_menu()
        else:
            print("🤔 That user was not found. \nWould you like to sign up?")
            yes_no = prompt.yes_no()
            if yes_no == "yes":
                self.handle_sign_up()
            else:
                self.start()

    def handle_logout(self):
        self.current_user = None
        self.start()

    def handle_new_task(self):
        description = Task.get_description()
        print("Enter due date manually or use today?")
        options = ["Today", "Manual"]
        manual_or_today = self.render_options(options)
        if manual_or_today == "Manual":
            year = Task.get_year()
            month = Task.get_month()
            day = Task.get_day()

            date_string = Task.create_date_string(year, month, day)
            if date_string:
                new_task = Task(
                    description=description,
                    due_date=datetime.strptime(date_string, "%Y-%m-%d"),
                    user_id=self.current_user.id,
                )
                session.add(new_task)
                session.commit()
                self.render_main_menu()
            else:
                print(red("That date is not valid. Please try again."))
                self.handle_new_task()
        else:
            new_task = Task(
                description=description,
                due_date=datetime.now(),
                user_id=self.current_user.id,
            )
            session.add(new_task)
            session.commit()
            self.render_main_menu()

    def exit(self):
        self.start()

    def quit(self):
        self.clear_screen()
        banner.goodbye()
        self.current_user = None

    def __repr__(self):
        return f"<Cli " + f"current_user={self.current_user} " + ">"
