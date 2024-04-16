import pytest
from unittest.mock import patch
from io import StringIO

from F3 import UserProfile, ReviewCatalog


def test_create_user_profile():
    catalog = ReviewCatalog()
    assert len(catalog.users) == 0

    with patch("builtins.input", side_effect=["test_user", "test_password"]):
        catalog.create_user_profile("test_user", "test_password")

    assert len(catalog.users) == 1
    assert "test_user" in catalog.users
    assert catalog.users["test_user"].username == "test_user"
    assert catalog.users["test_user"].password == "test_password"


def test_create_user_profile_duplicate_username():
    catalog = ReviewCatalog()
    assert len(catalog.users) == 0

    catalog.users["existing_user"] = UserProfile("existing_user", "existing_password")

    with patch("builtins.input", side_effect=["existing_user", "test_password"]):
        catalog.create_user_profile("existing_user", "test_password")

    assert len(catalog.users) == 1  # User should not be added


def test_login_successful():
    catalog = ReviewCatalog()
    catalog.users["test_user"] = UserProfile("test_user", "test_password")

    with patch("builtins.input", side_effect=["test_user", "test_password"]):
        catalog.login("test_user", "test_password")

    assert catalog.current_user is not None
    assert catalog.current_user.username == "test_user"


def test_login_invalid_username():
    catalog = ReviewCatalog()
    catalog.users["test_user"] = UserProfile("test_user", "test_password")

    with patch("builtins.input", side_effect=["invalid_user", "test_password"]):
        catalog.login("invalid_user", "test_password")

    assert catalog.current_user is None


def test_login_invalid_password():
    catalog = ReviewCatalog()
    catalog.users["test_user"] = UserProfile("test_user", "test_password")

    with patch("builtins.input", side_effect=["test_user", "invalid_password"]):
        catalog.login("test_user", "invalid_password")

    assert catalog.current_user is None


def test_add_to_list():
    user = UserProfile("test_user", "test_password")
    user.add_to_list("Movie 1", "Movie", 4, "Enjoyed it!")

    assert ("Movie 1", "Movie") in user.media_list
    assert user.media_list[("Movie 1", "Movie")] == {"rating": 4, "review": "Enjoyed it!"}


def test_add_to_list_duplicate():
    user = UserProfile("test_user", "test_password")
    user.add_to_list("Movie 1", "Movie", 4, "Enjoyed it!")

    with patch("builtins.print") as mock_print:
        user.add_to_list("Movie 1", "Movie", 3, "Okay")

    mock_print.assert_called_once_with("You've already added Movie 1 (Movie) to your list.")
    assert user.media_list[("Movie 1", "Movie")] == {"rating": 4, "review": "Enjoyed it!"}


def test_get_reviews_with_reviews(capfd):
    catalog = ReviewCatalog()
    user1 = UserProfile("user1", "password1")
    user1.add_to_list("Movie 1", "Movie", 4, "Great!")
    catalog.users = {"user1": user1}

    with patch("builtins.input", side_effect=["Movie 1", "Movie"]):
        catalog.get_reviews("Movie 1", "Movie")

    captured_output = capfd.readouterr()
    assert "Reviews for Movie 1 (Movie):" in captured_output.out
    assert "user1: Rating - 4, Review - Great!" in captured_output.out


def test_get_reviews_no_reviews(capfd):
    catalog = ReviewCatalog()
    user1 = UserProfile("user1", "password1")
    catalog.users = {"user1": user1}

    with patch("builtins.input", side_effect=["Movie 1", "Movie"]):
        catalog.get_reviews("Movie 1", "Movie")

    captured_output = capfd.readouterr()
    assert "No reviews found for Movie 1 (Movie)." in captured_output.out


def test_get_written_reviews_with_reviews(capfd):
    catalog = ReviewCatalog()
    user1 = UserProfile("user1", "password1")
    user1.add_to_list("Movie 1", "Movie", 4, "Great!")
    catalog.users = {"user1": user1}

    with patch("builtins.input", side_effect=["Movie 1", "Movie"]):
        catalog.get_written_reviews("Movie 1", "Movie")

    captured_output = capfd.readouterr()
    assert "Written reviews for Movie 1 (Movie):" in captured_output.out
    assert "user1: Great!" in captured_output.out


def test_get_written_reviews_no_reviews(capfd):
    catalog = ReviewCatalog()
    user1 = UserProfile("user1", "password1")
    catalog.users = {"user1": user1}

    with patch("builtins.input", side_effect=["Movie 1", "Movie"]):
        catalog.get_written_reviews("Movie 1", "Movie")

    captured_output = capfd.readouterr()
    assert "No written reviews found for Movie 1 (Movie)." in captured_output.out

# Run tests using `pytest F3_Test.py` in the terminal
