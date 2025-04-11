class Reservation:
    def __init__(self, reservation_id=None, asset_id=None, employee_id=None,
                 reservation_date=None, start_date=None, end_date=None, status=None):
        self.__reservation_id = reservation_id
        self.__asset_id = asset_id
        self.__employee_id = employee_id
        self.__reservation_date = reservation_date
        self.__start_date = start_date
        self.__end_date = end_date
        self.__status = status

    @property
    def reservation_id(self):
        return self.__reservation_id

    @property
    def asset_id(self):
        return self.__asset_id

    @property
    def employee_id(self):
        return self.__employee_id

    @property
    def reservation_date(self):
        return self.__reservation_date

    @property
    def start_date(self):
        return self.__start_date

    @property
    def end_date(self):
        return self.__end_date

    @property
    def status(self):
        return self.__status

    @reservation_id.setter
    def reservation_id(self, value):
        self.__reservation_id = value

    @asset_id.setter
    def asset_id(self, value):
        self.__asset_id = value

    @employee_id.setter
    def employee_id(self, value):
        self.__employee_id = value

    @reservation_date.setter
    def reservation_date(self, value):
        self.__reservation_date = value

    @start_date.setter
    def start_date(self, value):
        self.__start_date = value

    @end_date.setter
    def end_date(self, value):
        self.__end_date = value

    @status.setter
    def status(self, value):
        self.__status = value