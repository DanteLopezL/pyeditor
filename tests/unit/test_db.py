import unittest
import sqlite3
import os
from unittest.mock import patch
import hashlib
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from db.db import Database


class TestDB(unittest.TestCase):
    TEST_DB = "test_file_editor.db"
    db: Database | None = None

    def setUp(self):
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)
        self.db = Database(self.TEST_DB)

    def tearDown(self):
        if self.db is not None:
            self.db = None
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    def test_hash_password_returns_consistent_hashes(self):
        assert self.db is not None
        password = "test_password"
        hash1 = self.db.hash_password(password)
        hash2 = self.db.hash_password(password)
        self.assertEqual(
            hash1, hash2, "Hashing the same password should produce the same hash"
        )

        expected_hash = hashlib.sha256(password.encode()).hexdigest()
        self.assertEqual(hash1, expected_hash, "Hash should be SHA-256")

    def test_create_user_success(self):
        assert self.db is not None
        result = self.db.create_user("test_user", "test_password")
        self.assertTrue(result, "User creation should succeed")

        conn = sqlite3.connect(self.TEST_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username=?", ("test_user",))
        user = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(user, "User should exist in database")

    def test_create_user_duplicate_username(self):
        assert self.db is not None
        self.db.create_user("test_user", "test_password")
        result = self.db.create_user("test_user", "different_password")
        self.assertFalse(result, "Duplicate username should be rejected")

    def test_authenticate_user_success(self):
        assert self.db is not None
        username = "test_user"
        password = "test_password"
        self.db.create_user(username, password)

        result = self.db.authenticate_user(username, password)
        self.assertTrue(
            result, "Authentication should succeed with correct credentials"
        )

    def test_authenticate_user_wrong_password(self):
        assert self.db is not None
        username = "test_user"
        self.db.create_user(username, "correct_password")

        result = self.db.authenticate_user(username, "wrong_password")
        self.assertFalse(result, "Authentication should fail with wrong password")

    def test_authenticate_user_nonexistent_user(self):
        assert self.db is not None
        result = self.db.authenticate_user("nonexistent", "password")
        self.assertFalse(result, "Authentication should fail for non-existent user")


if __name__ == "__main__":
    unittest.main()
