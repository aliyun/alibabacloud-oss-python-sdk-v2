import os
from typing import Optional, Callable
from ..types import Credentials, CredentialsProvider
from ..exceptions import CredentialsEmptyError


class AnonymousCredentialsProvider(CredentialsProvider):
    """Access OSS anonymously.
    """

    def __init__(self) -> None:
        self._credentials = Credentials("", "")

    def get_credentials(self) -> Credentials:
        return self._credentials


class StaticCredentialsProvider(CredentialsProvider):
    """Explicitly specify the AccessKey pair that you want to use to access OSS.
    """

    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        security_token: Optional[str] = None,
    ) -> None:
        """
        Args:
            access_key_id (str): access key id to access OSS.
            access_key_secret (str): access key secret to access OSS.
            security_token (Optional[str], optional): The sts session token.
        """
        self._credentials = Credentials(
            access_key_id, access_key_secret, security_token)

    def get_credentials(self) -> Credentials:
        return self._credentials

class EnvironmentVariableCredentialsProvider(CredentialsProvider):
    """Obtaining credentials from environment variables.
    OSS_ACCESS_KEY_ID
    OSS_ACCESS_KEY_SECRET
    OSS_SESSION_TOKEN (Optional)
    """

    def __init__(self) -> None:
        access_key_id = os.getenv("OSS_ACCESS_KEY_ID", '')
        access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET", '')

        if access_key_id == '' or access_key_secret == '':
            raise CredentialsEmptyError()

        self._credentials = Credentials(
            access_key_id, access_key_secret, os.getenv("OSS_SESSION_TOKEN", None))

    def get_credentials(self) -> Credentials:
        return self._credentials

class CredentialsProviderFunc(CredentialsProvider):
    """Provides a helper wrapping a function value to satisfy the CredentialsProvider interface.
    """

    def __init__(
        self,
        func: Callable,
    ) -> None:
        self._func = func

    def get_credentials(self) -> Credentials:
        return self._func()
