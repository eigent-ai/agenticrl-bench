class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def get_users(self):
        return self.users

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
