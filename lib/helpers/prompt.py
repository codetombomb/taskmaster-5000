from simple_term_menu import TerminalMenu
from prettycli import color

class Prompt():
    
    def ask(self, question):
        user_input = input(question + " ")
        confirmed = self.confirm(user_input)
        if confirmed:
            return user_input
        else:
            return self.ask(question)
    
    def confirm(self, user_input):
        print(f"You entered: {user_input} ")
        yes_no = self.yes_no()
        return yes_no == "yes"
        
    def yes_no(self):
        options =["yes", "no"]
        menu = TerminalMenu(options, menu_highlight_style=("fg_cyan",))
        selection = menu.show()
        return options[selection]