import psycopg2 as pg
from config import *
import json


def main():
    try:
        connection = pg.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )

        cursor = connection.cursor()
    except pg.Error:
        return print('Error while connecting to PostgreSQL')

    export(FOOD_FILE, 'food_product', cursor)
    export(FOOD_I18N_FILE, 'food_producttranslation', cursor)
    export(CATEGORIES_FILE, 'food_category', cursor)
    export(CATEGORIES_I18N_FILE, 'food_categorytranslation', cursor)

    connection.commit()
    cursor.close()
    connection.close()

def prepair(el):
    if isinstance(el, str):
        return 'E\'{}\''.format(el.replace('\'', '\\\''))
    else:
        return str(el)


def export(filename, table_name, cursor):
    file = open(filename)
    data = json.loads(json.load(file))

    if len(data) == 0:
        return

    values = []

    for d in data:
        values.append('({})'.format(','.join(map(prepair, d.values()))))

    query = 'INSERT INTO {}({}) VALUES {}'.format(table_name, ','.join(data[0].keys()), ','.join(values))

    cursor.execute(query)

    file.close()


if __name__ == '__main__':
    main()
