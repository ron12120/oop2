class Observer():
    def __init__(self):
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.add_notification(message)

    def add_notification(self, message):
        self.notifications.append(message)

    def print_notifications(self):
        print(f'{self.name}\'s notifications:')
        for notification in self.notifications:
            print(notification)


class User(Observer):
    def __init__(self, name: str, password: str, network):
        super().__init__()
        self.name = name
        self.password = password
        self.following = []
        self.followers = []
        self.posts = []
        self.notifications = []
        self.network = network

    def follow(self, user):
        self.network.follow(self, user)

    def unfollow(self, user):
        self.network.unfollow(self, user)

    def print_notifications(self):
        for notification in self.notifications:
            print(notification)

    def update(self, message):
        self.notifications.append(message)

    def print_notifications(self):
        print(f'{self.name}\'s notifications:')
        for notification in self.notifications:
            print(notification)

    def publish_post(self, post_type: str, content: str, price: int = 0, location=None):
        post = self.network.create_post(self, post_type, content, price, location)
        if post is not None:
            self.posts.append(post)
            self.notify(f'{self.name} has a new post')
        return post

    def __str__(self):
        return f'User name: {self.name}, Number of posts: {len(self.posts)}, Number of followers: {len(self.observers)}'
