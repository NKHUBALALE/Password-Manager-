import re
import hashlib
import json
import os
import random
import string


class PasswordManager:
    def __init__(self):
        self.file = "storage.json"

        self.password_history = []
        self.failed_attempts = 0
        self.locked = False

        self._load()

    def _load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    data = json.load(f)
                    self.password_history = data.get("password_history", [])
            except:
                self.password_history = []

    def _save(self):
        with open(self.file, "w") as f:
            json.dump({
                "password_history": self.password_history
            }, f)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def calculate_strength(self, password: str) -> int:
        score = 0

        if len(password) >= 8:
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"\d", password):
            score += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1

        return score

    def strength_label(self, score: int) -> str:
        if score <= 2:
            return "Weak"
        elif score in (3, 4):
            return "Medium"
        return "Strong"

    def verify_password(self, attempt: str):
        if self.locked:
            return False, "Account is locked due to multiple failed attempts."

        if not self.password_history:
            return False, "No password has been set."

        hashed_attempt = self._hash_password(attempt)

        if hashed_attempt == self.password_history[-1]:
            self.failed_attempts = 0
            return True, "Password verified successfully."

        self.failed_attempts += 1

        if self.failed_attempts >= 3:
            self.locked = True
            return False, "Too many failed attempts. Account locked."

        return False, f"Incorrect password. Attempts left: {3 - self.failed_attempts}"

    def set_password(self, new_password: str):
        if self.locked:
            return False, "Account is locked. Cannot change password."

        score = self.calculate_strength(new_password)

        if score < 4:
            return False, "Password does not meet security requirements."

        hashed_password = self._hash_password(new_password)

        if hashed_password in self.password_history:
            return False, "Password has been used before."

        self.password_history.append(hashed_password)
        self._save()

        return True, "Password successfully updated."

    def generate_password(self, length: int = 10):

        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*(),.?\":{}|<>"

        password_chars = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special),
        ]

        all_chars = lowercase + uppercase + digits + special

        while len(password_chars) < length:
            password_chars.append(random.choice(all_chars))

        random.shuffle(password_chars)

        return "".join(password_chars)

    def get_password_count(self):
        return len(self.password_history)

    def reset_lock(self):
        self.failed_attempts = 0
        self.locked = False