import unittest
from dao.asset_management_service_impl import AssetManagementServiceImpl
from myexception.exceptions import AssetNotFoundException, AssetNotMaintainException
import mysql.connector
from datetime import date, timedelta

class TestAssetManagementSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = AssetManagementServiceImpl()
        cls.test_asset_id = None
        cls.test_employee_id = 1
        cls.test_reservation_id = None

    def test_1_add_asset_success(self):
        name = "Test Asset"
        asset_type = "Test Equipment"
        serial_number = "TEST12"
        purchase_date = date.today().strftime('%Y-%m-%d')
        location = "Test Location"
        status = "available"
        owner_id = None

        asset_id = self.service.add_asset(
            name, asset_type, serial_number,
            purchase_date, location, status, owner_id
        )

        self.assertIsNotNone(asset_id)
        TestAssetManagementSystem.test_asset_id = asset_id

        conn = None
        cursor = None
        try:
            conn = self.service.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("select * from assets where asset_id = %s", (asset_id,))
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[1], name)
            self.assertEqual(result[6].lower(), "available")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def test_2_reserve_asset_success(self):
        if not hasattr(TestAssetManagementSystem, 'test_asset_id'):
            self.skipTest("No asset available for reservation test")

        employee_id = self.test_employee_id
        reservation_date = date.today().strftime('%Y-%m-%d')
        start_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')

        result = self.service.reserve_asset(
            TestAssetManagementSystem.test_asset_id,
            employee_id,
            reservation_date,
            start_date,
            end_date
        )

        self.assertTrue(result)

        conn = None
        cursor = None
        try:
            conn = self.service.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("select status from assets where asset_id = %s", (TestAssetManagementSystem.test_asset_id,))
            asset_status = cursor.fetchone()[0]
            self.assertEqual(asset_status.lower(), "reserved")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def test_3_perform_maintenance_on_reserved_asset(self):
        asset_id = self.service.add_asset(
            "Test Asset", "Equipment", "TEST1",
            "2023-01-01", "Location", "available", None
        )
        self.assertIsNotNone(asset_id)

        conn = None
        cursor = None
        try:
            conn = self.service.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("select 1 from assets where asset_id = %s", (asset_id,))
            self.assertTrue(cursor.fetchone())
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        reserve_result = self.service.reserve_asset(
            asset_id,
            self.test_employee_id,
            date.today().strftime('%Y-%m-%d'),
            (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
        )
        self.assertTrue(reserve_result)

        with self.assertRaises(AssetNotMaintainException):
            self.service.perform_maintenance(
                asset_id,
                date.today().strftime('%Y-%m-%d'),
                "Test maintenance",
                100.00
            )

        self.service.delete_asset(asset_id)

    def test_4_asset_not_found_exception(self):
        invalid_asset_id = 9999

        with self.assertRaises(AssetNotFoundException):
            self.service.update_asset(invalid_asset_id, "New Location", "available")

        with self.assertRaises(AssetNotFoundException):
            self.service.delete_asset(invalid_asset_id)

        with self.assertRaises(AssetNotFoundException):
            self.service.perform_maintenance(invalid_asset_id, "2023-01-01", "Test", 100.00)

    def test_5_asset_not_maintained_exception(self):
        old_date = (date.today() - timedelta(days=365 * 3)).strftime('%Y-%m-%d')
        asset_id = self.service.add_asset(
            "Old Unmaintained Asset",
            "Equipment",
            "OLD13",
            old_date,
            "Storage",
            "available",
            None
        )

        self.assertIsNotNone(asset_id)

        with self.assertRaises(AssetNotMaintainException):
            self.service.allocate_asset(
                asset_id,
                self.test_employee_id,
                date.today().strftime('%Y-%m-%d')
            )

        self.service.delete_asset(asset_id)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'test_asset_id') and cls.test_asset_id:
            conn = None
            cursor = None
            try:
                conn = cls.service.db.get_connection()
                cursor = conn.cursor()
                cursor.execute("delete from reservations where asset_id = %s", (cls.test_asset_id,))
                cursor.execute("delete from assets where asset_id = %s", (cls.test_asset_id,))
                conn.commit()
            except Exception as e:
                if conn: conn.rollback()
            finally:
                if cursor: cursor.close()
                if conn: conn.close()

if __name__ == '__main__':
    unittest.main()