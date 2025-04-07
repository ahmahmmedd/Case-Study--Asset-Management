class MaintenanceRecord:
    def __init__(self, maintenance_id=None, asset_id=None, maintenance_date=None,
                 description=None, cost=None):
        self.__maintenance_id = maintenance_id
        self.__asset_id = asset_id
        self.__maintenance_date = maintenance_date
        self.__description = description
        self.__cost = cost

    # Getters
    @property
    def maintenance_id(self):
        return self.__maintenance_id

    @property
    def asset_id(self):
        return self.__asset_id

    @property
    def maintenance_date(self):
        return self.__maintenance_date

    @property
    def description(self):
        return self.__description

    @property
    def cost(self):
        return self.__cost

    # Setters
    @maintenance_id.setter
    def maintenance_id(self, value):
        self.__maintenance_id = value

    @asset_id.setter
    def asset_id(self, value):
        self.__asset_id = value

    @maintenance_date.setter
    def maintenance_date(self, value):
        self.__maintenance_date = value

    @description.setter
    def description(self, value):
        self.__description = value

    @cost.setter
    def cost(self, value):
        self.__cost = value