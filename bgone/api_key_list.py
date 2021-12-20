import typing
import requests


class api_key_list():
    def __init__(self, api_keys: list, account_url: str) -> None:
        self._account_url = account_url
        self._api_keys = self.__initialize_keys(api_keys)
        self._curr_key = self.__get_new_key()

    def __get_num_credits(self, key: str) -> typing.Union[int, None]:
        """Returns the number of api credits left for the given key

        Args:
            key (str): the api key
            sessions(ClientSession): an aiohttp session

        Returns:
            int | None: number of api credits left or None if request failed
        """
        headers = {'X-Api-Key': key}
        response = requests.get(self._account_url, headers=headers)
        num_credits = None

        if response.status_code == requests.codes.ok:
            num_credits = response.json(
            )['data']['attributes']['api']['free_calls']

        return num_credits

    def __initialize_keys(self, api_keys: typing.List[str]) -> dict:
        """Initialize the key rotation 

        Args:
            api_keys (List[str]): List of API keys

        Returns:
            dict: [description]
        """
        keys = {}

        # keep sucessful keys (> 0 calls left or non-failed keys)
        for api_key in api_keys:
            num_credits = self.__get_num_credits(api_key)
            if num_credits is not None or num_credits > 0:
                keys[api_key] = num_credits

        return keys

    def __get_new_key(self) -> typing.Union[str, None]:
        """returns a new key if possible. Returns None if there are no more keys
        to use

        Returns:
            str | None: A new key or None if one cannot be found.
        """
        new_key = None
        if len(self._api_keys.keys()) != 0:
            new_key = list(self._api_keys.keys())[0]
        return new_key

    @property
    def total_credits(self) -> int:
        """returns the total number of credits left

        Returns:
            int: number of credits left
        """
        return sum(self._api_keys.values())

    @property
    def curr_key(self) -> typing.Union[str, None]:
        """Returns the current key in rotation. Returns None if there is no
        available key.
        """
        return self._curr_key

    def use_key(self) -> None:
        """Decreases the current key's credit by 1 and replaces it with a new
        key if credits for it run out.
        """
        if self.get_total_credits() == 0:
            return

        self._api_keys[self._curr_key] -= 1

        if self._api_keys[self._curr_key] == 0:
            self._api_keys.pop(self._curr_key)
            self._curr_key = self.__get_new_key()
