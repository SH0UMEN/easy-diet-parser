import MySQLdb as sql
from config import *
import json


def main():
    try:
        db = sql.connect(
            user=DB_USERNAME,
            passwd=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            db=DB_NAME
        )
    except sql.Error:
        return print('Error while connecting to PostgreSQL')

    export(CATEGORIES_FILE, CATEGORY_TABLE, db)
    export(CATEGORIES_I18N_FILE, CATEGORY_I18N_TABLE, db)
    export(FOOD_FILE, FOOD_TABLE, db)
    export(FOOD_I18N_FILE, FOOD_I18N_TABLE, db)

    db.commit()
    db.close()


def prepair(el):
    if isinstance(el, str):
        return '\'{}\''.format(el.replace('\'', '\\\''))
    else:
        return str(el)


def export(filename, table_name, db):
    file = open(filename)
    data = json.loads(json.load(file))

    if len(data) == 0:
        return

    values = []

    for d in data:
        values.append('({})'.format(','.join(map(prepair, d.values()))))

    query = 'INSERT INTO {}({}) VALUES {}'.format(table_name, ','.join(data[0].keys()), ','.join(values))

    db.query(query)

    file.close()


if __name__ == '__main__':
    main()
