class AssetNotFoundException(Exception):
    def __init__(self, message="Asset not found"):
        self.message = message
        super().__init__(self.message)

class AssetNotMaintainException(Exception):
    def __init__(self, message="Asset is not properly maintained"):
        self.message = message
        super().__init__(self.message)