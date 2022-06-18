from food_desc_parser import FoodDescParser
from group_desc_parser import GroupDescParser
from nutrient_definition_parser import NutrientDefinitionParser
from nutrient_data_parser import NutrientDataParser
import translators as ts
from os.path import exists
from config import *
import json


def main():
    food_parser = FoodDescParser()
    food_parser.parse(FOOD_DESCRIPTION_FILE_PATH)
    foods = food_parser.filter_fields(['id', 'category_id', 'title'])

    categories = GroupDescParser().parse(GROUP_DESCRIPTION_FILE_PATH)
    nutrients = NutrientDefinitionParser().parse(NUTRIENT_DEFINITION_FILE_PATH)
    nutrients_foods = NutrientDataParser().parse(NUTRIENT_DATA_FILE_PATH)

    print('Data transformation...')

    for link in nutrients_foods.values():
        food = foods[link['food_id']]
        nutrient = nutrients[link['nutrient_id']]
        tag = nutrient['tagname']

        if tag == 'CHOCDF':
            nutrient_res_name = 'carbohydrate'
        elif tag == 'PROCNT':
            nutrient_res_name = 'protein'
        elif tag == 'FAT':
            nutrient_res_name = 'fat'
        elif tag == 'ENERC_KCAL':
            nutrient_res_name = 'kcal'
        else:
            continue

        value = link['value']

        food[nutrient_res_name] = value

    print('Data transformation is completed')

    if not exists(FOOD_I18N_FILE):
        write_json(translate_titles(foods, 'product_id'), FOOD_I18N_FILE)

    if not exists(CATEGORIES_I18N_FILE):
        write_json(translate_titles(categories, 'category_id'), CATEGORIES_I18N_FILE)

    if not exists(FOOD_FILE):
        for key in foods:
            foods[key].pop('title', None)

        write_json(list(foods.values()), FOOD_FILE)

    if not exists(CATEGORIES_FILE):
        for key in categories:
            categories[key].pop('title', None)

        write_json(list(categories.values()), CATEGORIES_FILE)


def translate_titles(items, relation_field_name):
    titles = []
    items_arr = []

    for item in items.values():
        titles.append(item['title'])
        items_arr.append(item)

    titles_translation = translate(titles)
    items_i18n = []

    languages = TRANSLATION_LANGUAGES
    languages.append('en')

    for i in range(len(titles)):
        for lang in languages:
            items_i18n.append({relation_field_name: items_arr[i]['id'], 'language': lang, 'title': titles_translation[lang][i]})

    return items_i18n


def translate(strings):
    strings_len = len(strings)

    print('Translating {} strings'.format(strings_len))

    translations = {'en': strings}
    batches = split_to_batches(strings, 650)

    for lang in TRANSLATION_LANGUAGES:
        translations[lang] = []

        for batch in batches:
            translations[lang].extend(ts.yandex(batch, from_language='en', to_language=lang).split('\n'))

            print('\r{}%'.format(round(len(translations[lang])/strings_len * 100, 3)), end='', flush=True)

    return translations


def split_to_batches(array, max_text_length):
    batches = []
    batch = ''

    for i in range(len(array)):
        if len(batch) + len(array[i]) > max_text_length - 1:
            batches.append(batch.strip())
            batch = ''

        batch += array[i] + '\n'

        if i == len(array) - 1:
            batches.append(batch.strip())

    return batches


def write_json(json_data, filename):
    with open(filename, 'w+') as file:
        json.dump(json.dumps(json_data), file)


if __name__ == '__main__':
    main()
