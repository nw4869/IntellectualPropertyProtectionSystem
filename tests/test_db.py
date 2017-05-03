import unittest
from sqlalchemy.orm.session import make_transient

from app import create_app
from app.models import *


class DBTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_simple_CURD(self):
        # add user
        user = User()
        user.username = 'nw'
        user.password = '4869'
        user.email = 'nw4869@gmail.com'
        user.name = 'nightwind'
        user.role = 1

        db.session.add(user)
        db.session.commit()

        # query to verify user
        result = User.query.filter_by(username='nw').first()
        self.assertEqual(user, result)

        # update user
        user.name = '张三'
        db.session.add(user)
        db.session.commit()
        # query to verify user
        result = User.query.filter_by(name='张三').first()
        print(result.name)
        self.assertEqual(user, result)

        # delete
        db.session.delete(user)
        db.session.commit()
        # verify
        result = User.query.filter_by(username='nw').first()
        self.assertIsNone(result)

    def test_file(self):
        # create user
        user = User()
        user.username = 'nw'
        user.password = '4869'
        user.email = 'nw4869@gmail.com'
        user.name = 'nightwind'
        user.role = 1

        db.session.add(user)
        db.session.commit()

        # create file
        file = File()
        file.hash = '0xeaeaa0f9773a5e7a1286ff54e39a6d19f5bdf819e24fa74f269a0addcce12d83'
        file.filename = 'nightwind'
        file.txhash = 'todo'
        file.owner_user = user

        make_transient(file)
        db.session.add(file)
        db.session.commit()

        # query file
        result = File.query.filter_by(hash=file.hash).first()
        self.assertEqual(file, result)

        # assert user back ref
        self.assertEqual(result, user.files[0])
        print(result.time, type(result.time))

        # remove user 检查级联删除user后，file的存在
        db.session.delete(user)
        db.session.commit()

        # verify file whether exist
        result = File.query.filter_by(hash=file.hash).first()
        self.assertIsNone(result)

        # 检查级联删除file后，user的存在
        make_transient(file)
        make_transient(user)
        db.session.add(file)
        db.session.commit()

        db.session.delete(file)
        db.session.commit()

        result = File.query.filter_by(hash=file.hash).first()
        self.assertIsNone(result)

        result = User.query.filter_by(username=user.username).first()
        self.assertEqual(user, result)


