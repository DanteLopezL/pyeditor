import unittest
import sqlite3
import os
from unittest.mock import patch
import hashlib
import sys
from pathlib import Path

# Add the src directory to the Python path
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

    def test_init_db_creates_users_table(self):
        assert self.db is not None
        conn = sqlite3.connect(self.TEST_DB)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists, "Users table should exist")

        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        expected_columns = [
            (0, "id", "INTEGER", 0, None, 1),
            (1, "username", "TEXT", 1, None, 0),
            (2, "password_hash", "TEXT", 1, None, 0),
            (3, "created_at", "TIMESTAMP", 0, "CURRENT_TIMESTAMP", 0),
        ]

        for i, col in enumerate(columns):
            self.assertEqual(
                col[1], expected_columns[i][1], f"Column {i} name mismatch"
            )
            self.assertEqual(
                col[2], expected_columns[i][2], f"Column {i} type mismatch"
            )
            self.assertEqual(
                col[3],
                expected_columns[i][3],
                f"Column {i} not null constraint mismatch",
            )

        conn.close()

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

    @patch("sqlite3.connect")
    def test_database_connection_error(self, mock_connect):
        mock_connect.return_value = sqlite3.connect(":memory:")
        db = Database(self.TEST_DB)

        mock_connect.side_effect = sqlite3.Error("Connection failed")

        with self.assertRaises(sqlite3.Error):
            db.create_user("test", "password")

        with self.assertRaises(sqlite3.Error):
            db.authenticate_user("test", "password")

    @patch("sqlite3.connect")
    def test_database_initialization_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error("Connection failed")

        with self.assertRaises(sqlite3.Error):
            Database(self.TEST_DB)


if __name__ == "__main__":
    unittest.main()
