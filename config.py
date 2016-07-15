import os


DEBUG = os.environ['DEBUG']
PROPAGATE_EXCEPTIONS = os.environ['PROPAGATE_EXCEPTIONS']
SECRET_KEY = os.environ['SECRET_KEY']
GLB_TOKEN = os.environ['GLB_TOKEN']
ITEMS_PER_PAGE = 20

statuses = {
    1: 'Mercado aberto',
    2: 'Mercado fechado',
    3: 'Mercado em atualização',
}
