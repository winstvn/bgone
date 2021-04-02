import typing
import requests


class api_key_list():
    def __init__(self, api_keys: list, account_url: str) -> None:
        self.account_url = account_url
        self.api_keys = self.__initialize_keys(api_keys)
        self.curr_key = self.__get_new_key()

    def __get_num_credits(self, key: str) -> typing.Union[int, None]:
        """returns the number of api credits left for the given key

        Args:
            key (str): the api key
            sessions(ClientSession): an aiohttp session

        Returns:
            int | None: number of api credits left or None if request failed
        """
        headers = {'X-Api-Key': key}
        response = requests.get(self.account_url, headers=headers)
        num_credits = None

        if response.status_code == requests.codes.ok:
            num_credits = response.json(
            )['data']['attributes']['api']['free_calls']

        return num_credits

    def __initialize_keys(self, api_keys: typing.List[str]) -> dict:
        """[summary]

        Args:
            api_keys (List[str]): [description]

        Returns:
            dict: [description]
        """
        num_credits = [self.__get_num_credits(api_key) for api_key in api_keys]
        keys = dict(zip(api_keys, num_credits))

        # remove any failed tasks or zero-credit keys
        for key, item in keys.items():
            if item is None or item == 0:
                keys.pop(key)

        return keys

    def __get_new_key(self) -> typing.Union[str, None]:
        """returns a new key if possible. Returns None if there are no more keys
        to use

        Returns:
            str | None: A new key or None if one cannot be found.
        """
        new_key = None
        if len(self.api_keys.keys()) != 0:
            new_key = list(self.api_keys.keys())[0]
        return new_key

    def get_total_credits(self) -> int:
        """returns the total number of credits left

        Returns:
            int: number of credits left
        """
        return sum(self.api_keys.values())

    def get_key(self) -> typing.Union[str, None]:
        """returns the current key

        Returns:
            typing.Union[str, None]: [description]
        """
        return self.curr_key

    def use_key(self) -> None:
        """ decreases the current key's credit by 1 and replaces it with a new
        key if credits for it run out
        """
        if self.get_total_credits() == 0:
            return
        
        self.api_keys[self.curr_key] -= 1

        if self.api_keys[self.curr_key] == 0:
            self.api_keys.pop(self.curr_key)
            self.curr_key = self.__get_new_key()
