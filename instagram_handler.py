from instaloader import *
from database_handler import DatabaseHandler

login_name = "alexander_test_test_test"

class InstagramHandler:

    loader = Instaloader()

    def setup_session(self):
        self.loader = Instaloader()
        try:
            self.loader.load_session_from_file(login_name)
        except FileNotFoundError:
            self.loader.context.log("Session file does not exist. Logging in...")
        if not self.loader.context.is_logged_in:
            self.loader.interactive_login(login_name)
            self.loader.save_session_to_file()

    def get_likes(self, photo_id):
        post = instaloader.Post.from_shortcode(self.loader.context, photo_id)
        likes = post.get_likes()
        usernames = []
        for like in likes:
            usernames.append(like.username)
        return usernames

    def get_comments(self, photo_id):
        post = instaloader.Post.from_shortcode(self.loader.context, photo_id)
        comments = post.get_comments()
        usernames = []
        for comment in comments:
            try:
                username = str(comment[3]).split()[1]
            except Exception as error:
                print(error)
                username = ""
            usernames.append(username)
        return usernames


    def check_that_user_liked_all_photos(self, instagram_username):
        database_handler = DatabaseHandler()
        links = database_handler.get_latest_photos(20)
        for link in links:
            usernames = self.get_likes(str(link[0]))
            if not str(instagram_username) in usernames:
                return False
        return True
