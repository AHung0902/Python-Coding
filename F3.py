class UserProfile:
    def __init__(self, username, password):
        """
        Initialize a user.

        Parameters:
        - username (str): The username.
        - password (str): The password.
        """
        self.username = username
        self.password = password
        self.media_list = {}

    def add_to_list(self, media_title, media_type, rating, review=None):
        """
        Adds a media title, type, rating, and review to a user's watched list.
        Parameters:
        - media_title (str): The name of the media.
        - media_type (str): The type of media the media is (book/movie).
        - rating (int): The rating the user gives to the media (1-5, only whole numbers).
        - review (str): Default none, however the user can choose to write their own review.
        """
        key = (media_title, media_type)
        if key not in self.media_list:
            self.media_list[key] = {"rating": rating, "review": review}
            print(f"{media_title} ({media_type}) added to your list.")
        else:
            print(f"You've already added {media_title} ({media_type}) to your list.")

    def upload_review(self, media_title, media_type):
        key = (media_title, media_type)
        if key in self.media_list:
            review = self.media_list[key]
            print(f"Review uploaded for {media_title} ({media_type}): Rating - {review['rating']}, Review - {review['review']}")
        else:
            print(f"You haven't added {media_title} ({media_type}) to your list yet.")


class ReviewCatalog:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def create_user_profile(self, username, password):
        """
            Checks for unique usernames.
            """
        if username not in self.users:
            self.users[username] = UserProfile(username, password)
            print(f"Profile created for {username}.")
        else:
            print("Username already exists. Please choose another.")

    def login(self, username, password):
        """
            Checks for correct login.
            """
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Welcome, {username}!")
        else:
            print("Invalid username or password.")

    def logout(self):
        self.current_user = None
        print("Logged out successfully.")

    def get_written_reviews(self, media_title, media_type):
        """
        Retrieves only the written reviews for a specific media.
        """
        key = (media_title, media_type)
        written_reviews = []

        for user in self.users.values():
            if key in user.media_list and user.media_list[key]['review']:
                written_reviews.append(f"{user.username}: {user.media_list[key]['review']}")

        if written_reviews:
            print(f"\nWritten reviews for {media_title} ({media_type}):")
            for review in written_reviews:
                print(review)
        else:
            print(f"No written reviews found for {media_title} ({media_type}).")

    def view_own_reviews(self):
        if self.current_user:
            user = self.current_user
            print(f"\nYour Reviews:")
            for key, review in user.media_list.items():
                media_title, media_type = key
                print(f"{media_title} ({media_type}): Rating - {review['rating']}, Review - {review['review']}")
        else:
            print("Please log in to view your reviews.")
    
    def get_reviews(self, media_title, media_type):
        """
        Retrieves the reviews and ratings created by the user and adds them to their review list.
        """
        key = (media_title, media_type)
        ratings = []
        reviews = []

        for user in self.users.values():
            if key in user.media_list:
                review = user.media_list[key]
                ratings.append(review['rating'])
                if review['review']:
                    reviews.append(f"{user.username}: Rating - {review['rating']}, Review - {review['review']}")

        if ratings:
            average_rating = sum(ratings) / len(ratings)
            print(f"\nReviews for {media_title} ({media_type}):")
            for review in reviews:
                print(review)
            print(f"\nAverage Rating: {average_rating:.2f}")
        else:
            print(f"No reviews found for {media_title} ({media_type}).")


def get_valid_rating():
    while True:
        try:
            rating = int(input("Enter the rating (1-5): "))
            if 1 <= rating <= 5:
                return rating
            else:
                print("Invalid rating. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_valid_media_type():
    while True:
        try:
            media = str(input("Enter the media type (Movie, Book, TV Show): "))
            if media.lower() == "movie":
                return "Movie"
            elif media.lower() == "book":
                return "Book"
            elif media.lower() == "tv show":
                return "TV Show"
            else:
                print("Invalid media type. Please enter a valid media type (Movie, Book, TV Show)")
        except ValueError:
            print("Invalid input. Please enter a media type.")


def main():
    catalog = ReviewCatalog()

    while True:
        print("\nOptions:")
        print("1. Create user profile")
        print("2. Login")
        print("3. Quit")

        choice = input("Enter your choice (1, 2, 3): ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            catalog.create_user_profile(username, password)

        elif choice == "2":
            login_username = input("Enter your username to log in: ")
            login_password = input("Enter your password: ")
            catalog.login(login_username, login_password)

            while catalog.current_user:
                print("\nOptions:")
                print("1. Add media you've seen")
                print("2. Look at reviews from other users for a media")
                print("3. View your own reviews")
                print("4. Logout")

                inner_choice = input("Enter your choice (1, 2, 3, 4): ")

                if inner_choice == "1":
                    media_title = input("Enter the media title: ")
                    media_type = get_valid_media_type()
                    rating = get_valid_rating()
                    review = input("Enter an optional review: ")
                    catalog.current_user.add_to_list(media_title, media_type, rating, review)

                elif inner_choice == "2":
                    media_title = input("Enter the media title to get reviews: ")
                    media_type = input("Enter the media type to get reviews: ")
                    catalog.get_reviews(media_title, media_type)

                elif inner_choice == "3":
                    catalog.view_own_reviews()

                elif inner_choice == "4":
                    catalog.logout()
                    break

                else:
                    print("Invalid choice. Please enter a valid option.")
        

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
