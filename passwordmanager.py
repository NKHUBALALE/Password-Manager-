import re
import hashlib


class PasswordManager:
    def __init__(self):
        self.password_history = []  # stores hashed passwords

    # ---------------------------
    # Hashing
    # ---------------------------
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # ---------------------------
    # Strength Calculation
    # ---------------------------
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

        return score  # 0–5

    def strength_label(self, score: int) -> str:
        if score <= 2:
            return "Weak"
        elif score == 3 or score == 4:
            return "Medium"
        return "Strong"

    # ---------------------------
    # Password Verification
    # ---------------------------
    def verify_password(self, attempt: str) -> bool:
        if not self.password_history:
            return False

        hashed_attempt = self._hash_password(attempt)
        return hashed_attempt == self.password_history[-1]

    # ---------------------------
    # Set Password
    # ---------------------------
    def set_password(self, new_password: str):
        score = self.calculate_strength(new_password)

        if score < 4:
            return False, "Password does not meet security requirements."

        hashed_password = self._hash_password(new_password)

        if hashed_password in self.password_history:
            return False, "Password has been used before."

        self.password_history.append(hashed_password)
        return True, "Password successfully updated."

    def get_password_count(self):
        return len(self.password_history)