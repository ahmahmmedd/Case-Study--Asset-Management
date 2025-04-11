import mysql.connector
from util.DBConnection import DBConnection
from myexception.exceptions import AssetNotFoundException
from myexception.exceptions import AssetNotMaintainException
from datetime import date, timedelta

class AssetManagementServiceImpl:
    def __init__(self):
        self.db = DBConnection()

    def add_asset(self, name, asset_type, serial_number, purchase_date, location, status, owner_id):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = ("insert into assets (name, type, serial_number, purchase_date, location, status, owner_id) values (%s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(query, (name, asset_type, serial_number,
                                   purchase_date, location, status, owner_id))
            conn.commit()
            asset_id = cursor.lastrowid
            print(f"asset added successfully! asset id: {asset_id}")
            return cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"database error: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def update_asset(self, asset_id, new_location, new_status):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = "update assets set location = %s, status = %s where asset_id = %s"
            cursor.execute(query, (new_location, new_status, asset_id))
            if cursor.rowcount == 0:
                raise AssetNotFoundException("asset id not found.")
            conn.commit()
            print("asset updated successfully!")
            return True
        except mysql.connector.Error as e:
            print(f"database error: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def delete_asset(self, asset_id):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = "delete from assets where asset_id = %s"
            cursor.execute(query, (asset_id,))
            if cursor.rowcount == 0:
                raise AssetNotFoundException("asset id not found.")
            conn.commit()
            print("asset deleted successfully!")
            return True
        except mysql.connector.Error as e:
            print(f"database error: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def allocate_asset(self, asset_id, employee_id, allocation_date):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                select status, purchase_date 
                from assets 
                where asset_id = %s
            """, (asset_id,))
            asset = cursor.fetchone()

            if not asset:
                raise AssetNotFoundException(f"asset id {asset_id} not found.")

            if asset['status'].lower() != 'available':
                print(f"cannot allocate asset - current status: {asset['status']}")
                return False

            purchase_date = asset['purchase_date']
            two_years_ago = date.today() - timedelta(days=365 * 2)

            if purchase_date < two_years_ago:
                cursor.execute("""
                    select 1 from maintenance_records 
                    where asset_id = %s 
                    and maintenance_date >= %s
                    limit 1
                """, (asset_id, two_years_ago))

                if not cursor.fetchone():
                    raise AssetNotMaintainException(
                        f"asset {asset_id} hasn't been maintained in the last 2 years")

            cursor.execute("""
                update assets 
                set status = 'allocated', owner_id = %s 
                where asset_id = %s
            """, (employee_id, asset_id))

            cursor.execute("""
                insert into asset_allocations 
                (asset_id, employee_id, allocation_date) 
                values (%s, %s, %s)
            """, (asset_id, employee_id, allocation_date))

            conn.commit()
            print(f"asset {asset_id} allocated successfully to employee {employee_id}!")
            return True

        except mysql.connector.Error as e:
            print(f"database error: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def deallocate_asset(self, asset_id):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            check_query = "select asset_id from assets where asset_id = %s"
            cursor.execute(check_query, (asset_id,))
            if not cursor.fetchone():
                raise AssetNotFoundException("asset id not found.")
            query = "update assets set status = 'available', owner_id = null where asset_id = %s"
            cursor.execute(query, (asset_id,))
            conn.commit()
            print("asset deallocated successfully!")
            return True
        except mysql.connector.Error as e:
            print(f"database error: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def perform_maintenance(self, asset_id, maintenance_date, description, cost):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                select status from assets 
                where asset_id = %s
            """, (asset_id,))
            row = cursor.fetchone()

            if not row:
                raise AssetNotFoundException("asset id not found.")

            status = row[0].lower()

            if status == "under maintenance":
                raise AssetNotMaintainException("asset is already under maintenance.")

            if status == "reserved":
                raise AssetNotMaintainException("cannot perform maintenance on reserved asset.")

            cursor.execute("""
                update assets 
                set status = 'under maintenance' 
                where asset_id = %s
            """, (asset_id,))

            cursor.execute("""
                insert into maintenance_records 
                (asset_id, maintenance_date, description, cost) 
                values (%s, %s, %s, %s)
            """, (asset_id, maintenance_date, description, cost))

            conn.commit()
            print("maintenance recorded successfully!")
            return True

        except mysql.connector.Error as e:
            print(f"database error: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def reserve_asset(self, asset_id, employee_id, reservation_date, start_date, end_date):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            check_query = "select status from assets where asset_id = %s"
            cursor.execute(check_query, (asset_id,))
            row = cursor.fetchone()
            if not row:
                raise AssetNotFoundException("asset id not found.")
            if row[0].lower() != 'available':
                print(f"cannot reserve asset - current status: {row[0]}")
                return False
            update_query = "update assets set status = 'reserved' where asset_id = %s"
            cursor.execute(update_query, (asset_id,))
            reservation_query = """insert into reservations 
                                (asset_id, employee_id, reservation_date, start_date, end_date, status) 
                                values (%s, %s, %s, %s, %s, 'reserved')"""
            cursor.execute(reservation_query, (asset_id, employee_id, reservation_date, start_date, end_date))
            conn.commit()
            reservation_id = cursor.lastrowid
            print(f"asset reserved successfully! reservation id: {reservation_id}")
            return True
        except mysql.connector.Error as e:
            print(f"database error: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def withdraw_reservation(self, reservation_id):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            get_query = """select r.asset_id, a.status 
                          from reservations r
                          join assets a on r.asset_id = a.asset_id
                          where r.reservation_id = %s"""
            cursor.execute(get_query, (reservation_id,))
            reservation = cursor.fetchone()
            if not reservation:
                raise AssetNotFoundException("reservation id not found.")
            asset_id, current_status = reservation
            if current_status.lower() != 'reserved':
                print(f"cannot withdraw reservation - asset is not reserved (current status: {current_status})")
                return False
            update_asset_query = "update assets set status = 'available' where asset_id = %s"
            cursor.execute(update_asset_query, (asset_id,))
            update_reservation_query = "update reservations set status = 'withdrawn' where reservation_id = %s"
            cursor.execute(update_reservation_query, (reservation_id,))
            conn.commit()
            print("reservation withdrawn successfully! asset is now available.")
            return True
        except mysql.connector.Error as e:
            print(f"database error: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()