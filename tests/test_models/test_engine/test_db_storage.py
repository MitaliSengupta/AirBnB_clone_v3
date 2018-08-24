#!/usr/bin/python3
'''
    Testing the file_storage module.
'''
import time
import unittest
import models
import sys
from models.engine.db_storage import DBStorage
from models import storage
from models.user import User
from models.state import State
from models import storage
from console import HBNBCommand
from os import getenv
from io import StringIO

db = getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db != 'db', "Testing DBstorage only")
class test_DBStorage(unittest.TestCase):
    '''
        Testing the DB_Storage class
    '''
    @classmethod
    def setUpClass(cls):
        '''
            Initializing classes
        '''
        cls.dbstorage = DBStorage()
        cls.output = StringIO()
        sys.stdout = cls.output

    @classmethod
    def tearDownClass(cls):
        '''
            delete variables
        '''
        del cls.dbstorage
        del cls.output

    def create(self):
        '''
            Create HBNBCommand()
        '''
        return HBNBCommand()

    def test_new(self):
        '''
            Test DB new
        '''
        new_obj = State(name="California")
        self.assertEqual(new_obj.name, "California")

    def test_dbstorage_user_attr(self):
        '''
            Testing User attributes
        '''
        new = User(email="melissa@hbtn.com", password="hello")
        self.assertTrue(new.email, "melissa@hbtn.com")

    def test_dbstorage_check_method(self):
        '''
            Check methods exists
        '''
        self.assertTrue(hasattr(self.dbstorage, "all"))
        self.assertTrue(hasattr(self.dbstorage, "__init__"))
        self.assertTrue(hasattr(self.dbstorage, "new"))
        self.assertTrue(hasattr(self.dbstorage, "save"))
        self.assertTrue(hasattr(self.dbstorage, "delete"))
        self.assertTrue(hasattr(self.dbstorage, "reload"))

    def test_dbstorage_all(self):
        '''
            Testing all function
        '''
        storage.reload()
        result = storage.all("")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 7)
        new = User(email="adriel@hbtn.com", password="abc")
        console = self.create()
        console.onecmd("create State name=California")
        result = storage.all("State")
        self.assertTrue(len(result) > 0)

    def test_dbstorage_new_save(self):
        '''
           Testing save method
        '''
        new_state = State(name="NewYork")
        storage.new(new_state)
        save_id = new_state.id
        result = storage.all("State")
        temp_list = []
        for k, v in result.items():
            temp_list.append(k.split('.')[1])
            obj = v
        self.assertTrue(save_id in temp_list)
        self.assertIsInstance(obj, State)

    def test_dbstorage_delete(self):
        '''
            Testing delete method
        '''
        new_user = User(email="haha@hehe.com", password="abc",
                        first_name="Adriel", last_name="Tolentino")
        storage.new(new_user)
        save_id = new_user.id
        key = "User.{}".format(save_id)
        self.assertIsInstance(new_user, User)
        storage.save()
        old_result = storage.all("User")
        del_user_obj = old_result[key]
        storage.delete(del_user_obj)
        new_result = storage.all("User")
        self.assertNotEqual(len(old_result), len(new_result))

    def test_model_storage(self):
        '''
            Test to check if storage is an instance for DBStorage
        '''
        self.assertTrue(isinstance(storage, DBStorage))

    def test_get_db_storage(self):
        """This test the get method in db_storage"""
        storage.reload()
        new_state = State(name="NewYork")
        storage.new(new_state)
        first_state_id = list(storage.all("State").values())[0].id
        self.assertEqual(type(storage.get("State", first_state_id)), State)

    def test_count_db_storage(self):
        """This test the get method in db_storage"""
        storage.reload()
        counter = storage.count("State")
        state = State(name="Colorado")
        state.save()
        counter_2 = storage.count("State")
        self.assertTrue(counter + 1, counter_2)
        result = storage.all("")
        count = storage.count(None)
        self.assertEqual(len(result), count)
        result = storage.all("State")
        count = storage.count("State")
        self.assertEqual(len(result), count)

    def test_get_db_storage(self):
        '''
        Tests the get method in db storage
        '''
        storage.reload()
        state = State(name="Cali")
        state_id = state.id
        state.save()
        state_obj = storage.get("State", state_id)
        self.assertEqual(state_obj, state)

    def test_count_db_storage_works(self):
        '''
        Tests if the count method in db storage is working
        '''
        storage.reload()
        all_dict = storage.all()
        all_count = len(all_dict)
        count = storage.count()
        self.assertEqual(all_count, count)

    def test_count_db_storage_no_class(self):
        '''
        Tests the count method in db storage when no class is passed
        '''
        storage.reload()
        first_count = storage.count()
        state = State(name="Colorado")
        state.save()
        second_count = storage.count()
        self.assertTrue(first_count + 1, second_count)

    def test_count_db_storage_class(self):
        '''
        Tests the count method in db storage when passing a class
        '''
        storage.reload()
        first_count = storage.count("State")
        state = State(name="Illinois")
        state.save()
        second_count = storage.count("State")
        self.assertTrue(first_count + 1, second_count)

    def test_db_get(self):
        """Test that get returns specific object, or none"""
        new_state = State(name="Maine")
        new_state.save()
        new_user = User(email="am@zon.com", password="password")
        new_user.save()
        self.assertIs(new_state, models.storage.get("State", new_state.id))
        self.assertIs(None, models.storage.get("State", "filler"))
        self.assertIs(new_user, models.storage.get("User", new_user.id))

    def test_db_count(self):
        """test that new adds an object to the database"""
        initial_count = models.storage.count()
        new_state = State(name="California")
        new_state.save()
        new_user = User(email="ali@baba.com", password="password")
        new_user.save()
        self.assertEqual(models.storage.count("State"), initial_count + 1)
        self.assertEqual(models.storage.count(), initial_count + 2)
