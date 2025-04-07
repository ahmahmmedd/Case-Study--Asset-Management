class Asset:
    def __init__(self, asset_id=None, name=None, asset_type=None, serial_number=None,
                 purchase_date=None, location=None, status=None, owner_id=None):
        self.__asset_id = asset_id
        self.__name = name
        self.__asset_type = asset_type
        self.__serial_number = serial_number
        self.__purchase_date = purchase_date
        self.__location = location
        self.__status = status
        self.__owner_id = owner_id

    # Getters
    @property
    def asset_id(self):
        return self.__asset_id

    @property
    def name(self):
        return self.__name

    @property
    def asset_type(self):
        return self.__asset_type

    @property
    def serial_number(self):
        return self.__serial_number

    @property
    def purchase_date(self):
        return self.__purchase_date

    @property
    def location(self):
        return self.__location

    @property
    def status(self):
        return self.__status

    @property
    def owner_id(self):
        return self.__owner_id

    # Setters
    @asset_id.setter
    def asset_id(self, value):
        self.__asset_id = value

    @name.setter
    def name(self, value):
        self.__name = value

    @asset_type.setter
    def asset_type(self, value):
        self.__asset_type = value

    @serial_number.setter
    def serial_number(self, value):
        self.__serial_number = value

    @purchase_date.setter
    def purchase_date(self, value):
        self.__purchase_date = value

    @location.setter
    def location(self, value):
        self.__location = value

    @status.setter
    def status(self, value):
        self.__status = value

    @owner_id.setter
    def owner_id(self, value):
        self.__owner_id = value