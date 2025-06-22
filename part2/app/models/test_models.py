# test_models.py

import time
import io
import contextlib

from app.models.base_model import BaseModel
from app.models.user       import User
from app.models.place      import Place
from app.models.review     import Review
from app.models.amenity    import Amenity

def test_base_model():
    a = BaseModel()
    b = BaseModel()
    assert a.id != b.id
    old = a.updated_at
    time.sleep(0.01)
    a.save()
    assert a.updated_at > old

def test_user_valid_and_invalid():
    User._used_emails.clear()
    u1 = User("Alice", "Smith", "alice@example.com")
    assert u1.first_name == "Alice"
    assert not u1.is_admin

    # First name too long
    try:
        User("X"*51, "Smith", "x@example.com")
        assert False
    except ValueError as e:
        assert "50 characters" in str(e)

    # Last name too long
    try:
        User("Bob", "Y"*51, "y@example.com")
        assert False
    except ValueError as e:
        assert "50 characters" in str(e)

    # Missing email
    try:
        User("Bob", "Jones", "")
        assert False
    except ValueError as e:
        assert "Email is required" in str(e)

    # Bad format
    try:
        User("Bob", "Jones", "no-at-symbol")
        assert False
    except ValueError as e:
        assert "Invalid email format" in str(e)

    # Duplicate email
    u2 = User("Carol", "Lee", "carol@example.com")
    try:
        User("Carol", "Lee", "carol@example.com")
        assert False
    except ValueError as e:
        assert "must be unique" in str(e)

def test_place_and_relationships():
    owner = User("Owner", "One", "owner1@example.com")
    p = Place("Cozy Loft", "Nice place", 120.0, 40.0, -75.0, owner)
    assert p.owner is owner

    # Invalid owner type
    try:
        Place("Title", "Desc", 50, 0, 0, "not a user")
        assert False
    except TypeError as e:
        assert "User instance" in str(e)

    # Amenity relationship
    a = Amenity("Wi-Fi")
    p.add_amenity(a)
    assert p.amenities == [a]

    # Review relationship
    r = Review("Great stay!", 5, p, owner)
    p.add_review(r)
    assert p.reviews == [r]

def test_review_validations():
    owner = User("R", "U", "r@example.com")
    p = Place("Place", "", 10.0, 0.0, 0.0, owner)

    # Invalid rating
    try:
        Review("Bad", 6, p, owner)
        assert False
    except ValueError as e:
        assert "between 1 and 5" in str(e)

    # Invalid place/user types
    try:
        Review("Text", 3, "not a place", owner)
        assert False
    except TypeError as e:
        assert "Place instance" in str(e)
    try:
        Review("Text", 3, p, "not a user")
        assert False
    except TypeError as e:
        assert "User instance" in str(e)

def test_amenity_length():
    ok = Amenity("Parking")
    assert ok.name == "Parking"

    # Name too long
    try:
        Amenity("X" * 51)
        assert False
    except ValueError as e:
        assert "50 characters" in str(e)

def test_display_methods():
    owner = User("Owner", "One", "owner.display@test.com")
    place = Place("Test", "Desc", 10.0, 0.0, 0.0, owner)

    # Test empty amenities
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        place.display_amenities()
    assert buf.getvalue().strip() == "There are no amenities for this place."

    # Test populated amenities
    amen = Amenity("Pool")
    place.add_amenity(amen)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        place.display_amenities()
    expected_amen = "Amenities:\n - Pool"
    assert buf.getvalue().strip() == expected_amen

    # Test empty reviews
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        place.display_reviews()
    assert buf.getvalue().strip() == "There are no reviews for this place."

    # Test populated reviews
    rev = Review("Loved it!", 5, place, owner)
    place.add_review(rev)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        place.display_reviews()
    expected_rev = "Owner: Loved it!"
    assert buf.getvalue().strip() == expected_rev

if __name__ == "__main__":
    for test in [
        test_base_model,
        test_user_valid_and_invalid,
        test_place_and_relationships,
        test_review_validations,
        test_amenity_length,
        test_display_methods,
    ]:
        test()
