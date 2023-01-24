from dataclasses import dataclass
import jwt
import openbb_terminal.feature_flags as obbff
from openbb_terminal.rich_config import console


@dataclass
class User:
    TOKEN_TYPE: str = ""
    TOKEN: str = ""
    EMAIL: str = ""
    UUID: str = ""

    @classmethod
    def load_user_info(cls, session: dict):
        """Load user info from login info.

        Parameters
        ----------
        session : dict
            The login info.
        """
        User.TOKEN_TYPE = session.get("token_type", "")
        User.TOKEN = session.get("access_token", "")
        User.UUID = session.get("uuid", "")

        if User.TOKEN:
            decoded_info = jwt.decode(User.TOKEN, options={"verify_signature": False})
            User.EMAIL = decoded_info.get("sub", "")

            if obbff.USE_FLAIR == ":openbb":
                username = User.EMAIL[: User.EMAIL.find("@")]
                setattr(obbff, "USE_FLAIR", "[" + username + "] 🦋")

    @classmethod
    def whoami(cls):
        console.print(f"[info]email:[/info] {User.EMAIL}")
        console.print(f"[info]uuid:[/info] {User.UUID}\n")
