from .prompt import Prompt
from prettycli import red


prompt = Prompt()

class SignUp:

    def get_first_name(self):
        return prompt.ask("What is your first name? ")

    def get_last_name(self):
        return prompt.ask("What is your last name? ")

    def get_username(self, session, Table):
        username = prompt.ask("Please enter a username: ")
        if session.query(Table).filter(Table.username.like(username)).first():
            print(red(f"That username is taken"))
            return self.get_username(session, Table)
        else:
            return username
        

    def get_birthday(self):
        pass

    def __repr__(self):
        return f"<SignUp first_name={self.first_name}, last_name={self.last_name}, username={self.username}>"
