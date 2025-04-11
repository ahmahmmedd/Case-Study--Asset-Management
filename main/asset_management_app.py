from dao.asset_management_service_impl import AssetManagementServiceImpl
from myexception.exceptions import AssetNotFoundException
from myexception.exceptions import AssetNotMaintainException

class AssetManagementApp:
    def __init__(self):
        self.service = AssetManagementServiceImpl()

    def display_menu(self):
        print("\n========== Asset Management System ================")
        print("1. Add Asset")
        print("2. Update Asset")
        print("3. Delete Asset")
        print("4. Allocate Asset")
        print("5. Deallocate Asset")
        print("6. Perform Maintenance")
        print("7. Reserve Asset")
        print("8. Withdraw Reservation")
        print("9. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    name = input("Enter asset name: ")
                    asset_type = input("Enter asset type: ")
                    serial_number = input("Enter serial number: ")
                    purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
                    location = input("Enter location: ")
                    status = input("Enter status (in use / decommissioned / under maintenance): ")
                    owner_id = input("Enter owner ID: ")
                    self.service.add_asset(name, asset_type, serial_number, purchase_date, location, status, owner_id)

                elif choice == "2":
                    asset_id = int(input("Enter asset ID to update: "))
                    new_location = input("Enter new location: ")
                    new_status = input("Enter new status(available/ in use / decommissioned / under maintenance): ")
                    self.service.update_asset(asset_id, new_location, new_status)

                elif choice == "3":
                    asset_id = int(input("Enter asset ID to delete: "))
                    self.service.delete_asset(asset_id)

                elif choice == "4":
                    asset_id = int(input("Enter asset ID to allocate: "))
                    employee_id = int(input("Enter employee ID: "))
                    allocation_date = input("Enter allocation date (YYYY-MM-DD): ")
                    self.service.allocate_asset(asset_id, employee_id, allocation_date)

                elif choice == "5":
                    asset_id = int(input("Enter asset ID to deallocate: "))
                    self.service.deallocate_asset(asset_id)

                elif choice == "6":
                    asset_id = int(input("Enter asset ID for maintenance: "))
                    maintenance_date = input("Enter maintenance date (YYYY-MM-DD): ")
                    description = input("Enter maintenance description: ")
                    cost = float(input("Enter maintenance cost: "))
                    self.service.perform_maintenance(asset_id, maintenance_date, description, cost)

                elif choice == "7":
                    asset_id = int(input("Enter asset ID to reserve: "))
                    employee_id = int(input("Enter employee ID: "))
                    reservation_date = input("Enter reservation date (YYYY-MM-DD): ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    self.service.reserve_asset(asset_id, employee_id, reservation_date, start_date, end_date)

                elif choice == "8":
                    reservation_id = int(input("Enter reservation ID to withdraw: "))
                    self.service.withdraw_reservation(reservation_id)

                elif choice == "9":
                    print("Exiting the application...")
                    break

                else:
                    print("Invalid choice! Please try again.")

            except AssetNotFoundException as e:
                print(f"Error: {e}")

            except AssetNotMaintainException as e:
                print(f"Error: {e}")

            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app = AssetManagementApp()
    app.run()
