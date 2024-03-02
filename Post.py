import matplotlib.image as mpimg
import matplotlib.pyplot as plt


class PostFactory:
    def __init__(self , network):
        self.network = network

    def create_post(self, user, post_type, content, price=None, location=None):
        if not self.network.is_active(user):
            raise Exception("you must be logged in to take this action")
        if post_type == "Text":
            return TextPost(user, content)
        elif post_type == "Image":
            return ImagePost(user, content)
        elif post_type == "Sale":
            return SalePost(user, content, price, location)
        else:
            raise Exception("Post type not supported")


class Post:
    def __init__(self, user, content):
        self.user = user
        self.content = content

    def like(self, user):
        if not self.user.network.is_active(user):
            raise Exception("you must be logged in to take this action")
        if user != self.user:
            print(f'notification to {self.user.name}: {user.name} liked your post')
            self.user.add_notification(f'{user.name} liked your post')

    def comment(self, user, message):
        if not self.user.network.is_active(user):
            raise Exception("you must be logged in to take this action")
        if user == self.user:
            return
        print(f'notification to {self.user.name}: {user.name} commented on your post: {message}')
        self.user.add_notification(f'{user.name} commented on your post')



class TextPost(Post):
    def __init__(self, user, content):
        super().__init__(user, content)
        print(f'{self.user.name} published a post:\n"{self.content}"\n')

    def __str__(self):
        return f'{self.user.name} published a post:\n"{self.content}"\n'


class ImagePost(Post):
    def __init__(self, user, content):
        super().__init__(user, content)
        # self.content = plt.imread(content)
        print(f'{self.user.name} posted a picture\n')

    def display(self):
        print("Shows picture")
        image = plt.imread(self.content)
        plt.imshow(image)
        plt.show() # uncomment to show the image

    def __str__(self):
        return f'{self.user.name} posted a picture\n'


class SalePost(Post):
    def __init__(self, user, content, price, location):
        super().__init__(user, content)
        self.price = price
        self.location = location
        self.status = "For sale!"
        print(self)

    def discount(self, amount, password):
        if not self.user.network.is_active(self.user):
            raise Exception("you must be logged in to take this action")

        print(password, self.user.password)
        if password == self.user.password:
            self.price = self.price * (1 - amount / 100)
            print(f'Discount on {self.user.name} product! the new price is: {self.price}')
        else:
            raise Exception("Wrong password")


    def sold(self, password):
        if password == "pass3":
            self.status = "Sold!"
            print(f'{self.user.name}\'s product is sold')
        else:
            print("Wrong password")

    def __str__(self):
        return f'{self.user.name} posted a product for sale:\n{self.status} {self.content}, price: {self.price}, pickup from: {self.location}\n'
