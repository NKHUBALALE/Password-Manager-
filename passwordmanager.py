import re
import hashlib
import json
import os
import random
import string
from cryptography.fernet import Fernet
import base64
from datetime import datetime

class PasswordManager:
    def __init__(self):
        self.file = "storage.json"

        self.data = {
            "users": {}
        }

        self.current_user = None
        self.key = None

        self._load()

    def _load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    self.data = json.load(f)

                    if "users" not in self.data:
                        self.data["users"] = {}
            except:
                self.data = {"users": {}}

    def register_user(self, username, password):
        if username in self.data["users"]:
            return False, "User already exists."

        self.data["users"][username] = {
            "master_hash": self._hash_password(password),
            "vault": []
        }

        self._save()
        return True, "User registered successfully."
    
    def login(self, username, password):
        user = self.data["users"].get(username)

        if not user:
            return False, "User not found, please check your login details or register if you don't have an account."

        if self._hash_password(password) != user["master_hash"]:
            return False, "Incorrect password."

        self.current_user = username
        self.key = self._derive_key(password)

        return True, "Login successful."
    def _save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _derive_key(self, master_password: str) -> bytes:
        hash_digest = hashlib.sha256(master_password.encode()).digest()
        return base64.urlsafe_b64encode(hash_digest)

    def _encrypt(self, password: str, key: bytes) -> str:
        f = Fernet(key)
        return f.encrypt(password.encode()).decode()

    def _decrypt(self, encrypted_password: str, key: bytes) -> str:
        f = Fernet(key)
        return f.decrypt(encrypted_password.encode()).decode()

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


    def reset_lock(self):
        self.failed_attempts = 0
        self.locked = False

    

    def add_entry(self, site, username, password):
        if self.key is None or self.current_user is None:
            return False, "You must log in first."

        user_vault = self.data["users"][self.current_user]["vault"]

        for entry in user_vault:
            if entry["site"] == site and entry["username"] == username:
                # 🔥 UPDATE instead of reject
                entry["password"] = self._encrypt(password, self.key)
                entry["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                self._save()
                return True, "Password updated successfully."

        # ➕ Create new entry
        encrypted_password = self._encrypt(password, self.key)

        user_vault.append({
            "site": site,
            "username": username,
            "password": encrypted_password,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self._save()
        return True, "Password saved successfully."

    def entry_exists(self, site, username):
        if self.current_user is None:
            return False

        user_vault = self.data["users"][self.current_user]["vault"]

        for entry in user_vault:
            if entry["site"] == site and entry["username"] == username:
                return True

        return False
    def get_entries(self):
        if self.key is None or self.current_user is None:
            return []

        user_vault = self.data["users"][self.current_user]["vault"]

        result = []

        for item in user_vault:
            decrypted = self._decrypt(item["password"], self.key)

            result.append({
                    "site": item["site"],
                    "username": item["username"],
                    "password": decrypted,
                    "updated_at": item.get("updated_at")
                })

        return result