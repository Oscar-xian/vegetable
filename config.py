HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'vegetable_provider'
SQLALCHEMY_DATABASE_URI= (f'mysql+mysqldb://{USERNAME}:{PASSWORD}@{HOSTNAME}:'
                                         f'{PORT}/{DATABASE}?charset=utf8mb4')