# -*- coding: utf-8 -*-

# import sys
# print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
# print(sys.path)
from ..utilities import init_flask
from flask_sqlalchemy import SQLAlchemy
from ..models import InfographicsDataCache
import logging

app = init_flask()
db = SQLAlchemy(app)

def logger_info():
    output = ''
    logger = logging.getLogger()
    handler = logging.FileHandler('log.log', mode='w')
    logger.addHandler(handler)
    handlers = logger.handlers
    lvl    = logger.getEffectiveLevel()
    to_print = 'logger type:{}, level:{}, handlers:{}.'\
        .format(type(logger), logger.getEffectiveLevel(), logger.handlers)
    output = '{"' + output + '"}'
    logging.debug(to_print)


def insert_to_cache(news_flash_id, years_ago, data):
    line = InfographicsDataCache(news_flash_id=news_flash_id, years_ago=years_ago, data=data)
    db.session.add(line)
    db.session.commit()


def print_cache():
    items = db.session.query(InfographicsDataCache).all()
    for item in items:
        print(item)


def main():
    insert_to_cache(1779, 5, {'ziv': 17, 'Harpaz': 19})


if __name__ == "__main__":
    logger_info()
    main()

