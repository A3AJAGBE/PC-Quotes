import os
import dbinfo

basedir = os.path.abspath(os.path.dirname(__file__))

dblink = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(
    dbinfo.user, dbinfo.password, dbinfo.host, dbinfo.database)


class Config(object):
    DEBUG = False
    # Database setup
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or dblink
    SQLALCHEMY_TRACK_MODIFICATIONS = False

