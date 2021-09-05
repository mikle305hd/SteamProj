from datetime import date


class SteamEvent:
    def __init__(self, first_date, last_date):
        self.__first_date = first_date
        self.__last_date = last_date

class CsgoEvent(SteamEvent):
    pass

class CsgoMajor(CsgoEvent):
    pass