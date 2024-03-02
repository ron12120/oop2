from User import User
from Post import PostFactory


class SocialNetwork():
    # using Singleton design pattern
    __instance = None

    def __new__(cls, name):
        if cls.__instance is None:
            cls.__instance = super(SocialNetwork, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, name):
        if self.__initialized:
            return

        self.__initialized = True # to avoid reinitialization
        self.name = name # name of the social network
        self.post_factory = PostFactory(self) # factory to create posts
        self.users = {} # dictionary of users
        self.logged_in = {} # dictionary of logged in users

        print("The social network", name, "was created!")

    def sign_up(self, username, password) -> User:
        if username in self.users.keys(): # check if username already exists
            raise Exception("Username already exists")
        if not len(password) in range(4, 9): # check if password is between 4 and 8 characters
            raise Exception("Password must be between 4 and 8 characters")

        user = User(username, password, self) # create a new user
        self.users[username] = user # add user to the dictionary of users
        self.logged_in[username] = True # change the status of the user to logged in
        return user

    def log_in(self, username, password):
        if username in self.users: # check if username exists
            user = self.users[username]  # get the user object
            if user.password == password: # check if the password is correct
                self.logged_in[username] = True # change the status of the user to logged in
                print(username, "connected")

    def log_out(self, username):
        if username in self.users: # check if username exists
            self.logged_in[username] = False # change the status of the user to logged out
            print(username, "disconnected")

    def is_active(self, user):
        return self.logged_in[user.name] # return the status of the user (logged in or not)


    def follow(self, user1: User, user2:User):
        if not self.follow_is_valid(user1, user2): # check if the follow action is valid (users exist and user1 is logged in)
            return
        if user1 not in user2.observers: # check if user1 is already following user2
            user2.register(user1) # add user1 to the list of followers of user2 (observers)
            print(f"{user1.name} started following {user2.name}")

    def unfollow(self, user1, user2): # user1 unfollows user2
        if not self.follow_is_valid(user1, user2): # check if the unfollow action is valid (users exist and user1 is logged in)
            return
        if user1 in user2.observers: # check if user1 is following user2
            user2.unregister(user1) # remove user1 from the list of followers of user2 (observers)
            print(f"{user1.name} unfollowed {user2.name}")

    def create_post(self, user, post_type, content, price=None, location=None): # create a post
        if not self.is_active(user): # check if the user is logged in
            raise Exception("you must be logged in to take this action")

        post = self.post_factory.create_post(user, post_type, content, price, location) # create a post using the post factory

        return post

    def __str__(self):
        return f'{self.name} social network:\n' + '\n'.join([str(user) for user in self.users.values()]) + '\n'

    def follow_is_valid(self, user1, user2):
        if (user1 and user2) not in self.users.values(): # check if the users exist
            raise Exception("user does not exist")
        if not self.is_active(user1): # check if user1 is logged in
            raise Exception("you must be logged in to take this action")
        return True








