import os


basedir = os.path.abspath(os.path.dirname(__file__))
media_dir = os.path.join(basedir, 'media')



HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'vegetable_provider'
SQLALCHEMY_DATABASE_URI= (f'mysql+mysqldb://{USERNAME}:{PASSWORD}@{HOSTNAME}:'
                                         f'{PORT}/{DATABASE}?charset=utf8mb4')

MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = '3160324355@qq.com'
MAIL_PASSWORD = 'wwdkhwlqgyeudfed'
MAIL_DEFAULT_SENDER = '3160324355@qq.com'

SECRET_KEY = 'qwerwqw123'

