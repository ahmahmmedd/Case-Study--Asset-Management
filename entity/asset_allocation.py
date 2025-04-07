class AssetAllocation:
    def __init__(self, allocation_id=None, asset_id=None, employee_id=None,
                 allocation_date=None, return_date=None):
        self.__allocation_id = allocation_id
        self.__asset_id = asset_id
        self.__employee_id = employee_id
        self.__allocation_date = allocation_date
        self.__return_date = return_date

    # Getters
    @property
    def allocation_id(self):
        return self.__allocation_id

    @property
    def asset_id(self):
        return self.__asset_id

    @property
    def employee_id(self):
        return self.__employee_id

    @property
    def allocation_date(self):
        return self.__allocation_date

    @property
    def return_date(self):
        return self.__return_date

    # Setters
    @allocation_id.setter
    def allocation_id(self, value):
        self.__allocation_id = value

    @asset_id.setter
    def asset_id(self, value):
        self.__asset_id = value

    @employee_id.setter
    def employee_id(self, value):
        self.__employee_id = value

    @allocation_date.setter
    def allocation_date(self, value):
        self.__allocation_date = value

    @return_date.setter
    def return_date(self, value):
        self.__return_date = value