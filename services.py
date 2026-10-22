from werkzeug.security import generate_password_hash, check_password_hash
from abc import ABC, abstractmethod

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.__password_hash = None

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if not value or not value.strip():
            raise ValueError("Username cannot be empty.")

        self.__username = value.strip()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not value or "@" not in value:
            raise ValueError("Invalid email address.")

        self.__email = value.strip().lower()

    @property
    def password_hash(self):
        return self.__password_hash

    def set_password(self, password):
        if not password or not password.strip():
            raise ValueError("Password cannot be empty.")

        self.__password_hash = generate_password_hash(password)


class AuthService(ABC):
    @abstractmethod
    def execute(self, data):
        pass


class PasswordStrategy(ABC):
    @abstractmethod
    def verify(self, password, password_hash):
        pass


class WerkzeugPasswordStrategy(PasswordStrategy):
    def verify(self, password, password_hash):
        if not password_hash:
            return False

        return check_password_hash(password_hash, password)


class SignupService(AuthService):
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def execute(self, data):
        try:
            username = data.get("username", "")
            email = data.get("email", "")
            password = data.get("password", "")

            user = User(username, email)
            user.set_password(password)

            self.cursor.execute(
                "SELECT email FROM users WHERE email = %s",
                (user.email,)
            )

            if self.cursor.fetchone() is not None:
                return {
                    "success": False,
                    "message": "Email is already registered."
                }, 409

            self.cursor.execute("SELECT username FROM users WHERE username = %s", (user.username,))

            if self.cursor.fetchone() is not None:
                return {
                    "sucess": False,
                    "message": "Username is already used"
                }, 409

            self.cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (
                    user.username,
                    user.email,
                    user.password_hash
                )
            )

            self.connection.commit()

            return {
                "success": True,
                "message": "Account created successfully!",
                "username": user.username,
                "email": user.email
            }, 201

        except ValueError as error:
            return {
                "success": False,
                "message": str(error)
            }, 400


class LoginService(AuthService):
    def __init__(self, cursor, password_strategy):
        self.cursor = cursor
        self.password_strategy = password_strategy

    def execute(self, data):
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not email or not password:
            return {
                "success": False,
                "message": "Email and password are required."
            }, 400

        self.cursor.execute("SELECT username, email, password_hash FROM users WHERE email = %s",(email,))

        record = self.cursor.fetchone()

        if record is None:
            return {
                "success": False,
                "message": "Invalid email or password."
            }, 401

        username, stored_email, stored_hash = record

        if not self.password_strategy.verify(
            password,
            stored_hash
        ):
            return {
                "success": False,
                "message": "Invalid email or password."
            }, 401

        return {
            "success": True,
            "message": f"Welcome, {username}!",
            "username": username,
            "email": stored_email
        }, 200


class AuthServiceFactory:
    @staticmethod
    def create(service_type, cursor, connection=None):

        if service_type == "signup":
            return SignupService(cursor, connection)

        elif service_type == "login":
            return LoginService(cursor,WerkzeugPasswordStrategy())

        else:
            raise ValueError("Unsupported authentication service.")
