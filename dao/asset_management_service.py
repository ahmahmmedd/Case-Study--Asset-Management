from abc import ABC, abstractmethod

class AssetManagementService(ABC):

    @abstractmethod
    def add_asset(self, name, asset_type, serial_number, purchase_date, location, status, owner_id):
        pass

    @abstractmethod
    def update_asset(self, asset_id, name=None, location=None, status=None):
        pass

    @abstractmethod
    def delete_asset(self, asset_id):
        pass

    @abstractmethod
    def allocate_asset(self, asset_id, employee_id, allocation_date,return_date):
        pass

    @abstractmethod
    def deallocate_asset(self, asset_id):
        pass

    @abstractmethod
    def perform_maintenance(self, asset_id, maintenance_date, description, cost):
        pass

    @abstractmethod
    def reserve_asset(self, asset_id, employee_id, reservation_date, start_date, end_date, status):
        pass

    @abstractmethod
    def withdraw_reservation(self, reservation_id):
        pass
