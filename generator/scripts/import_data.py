import json
import os
import sys

from generator.models import Meaning, Word


def import_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            parsed_json = json.load(f)
        return parsed_json

    except FileNotFoundError:
        print(f"File not found at: {file_path}")
    except json.JSONDecodeError:
        print("Invalid JSON format in the file.")
    except Exception as e:
        print(f"An error occured: {str(e)}")


def data_to_models(data):
    """Assumed data model in JSON:
    v    "abaja": [
        "sukmana",
        "płaszcz",
        "okrycie",
        "burka"
    ],
    "abakus": {
        "1": [
            "(rzadziej) abak"
        ],
        "2": [
            "liczydło",
            "maszyna licząca",
            "arytmometr"
        ]
    },
    """
    meanings_count = 0

    try:
        for word, meaning in data.items():
            # if there's no 'Word' in database - create
            word_obj, created = Word.objects.get_or_create(word=word)

            if isinstance(meaning, list):
                joined_meaning = ', '.join(meaning)
                meaning_obj = Meaning.objects.get_or_create(
                    word=word_obj, meaning=joined_meaning)
                meanings_count += 1

            elif isinstance(meaning, dict):
                for sub_key, sub_meaning in meaning.items():
                    joined_sub_meaning = ', '.join(sub_meaning)
                    meaning_obj = Meaning.objects.get_or_create(
                        word=word_obj, meaning=joined_sub_meaning)
                    meanings_count += 1
        return meanings_count
    except Exception as e:
        print(f"An error occured at data_to_models: {str(e)}")


def run():
    # path settings
    current_directory = os.path.dirname(__file__)
    print(current_directory)
    json_file_path = "../../static/data/"
    json_file_name = "test_data.json"
    file_path = os.path.join(current_directory, json_file_path+json_file_name)

    data = import_from_file(file_path)

    try:
        total_words_in_file = len(data.keys())
        total_meanings_in_file = data_to_models(data)
        total_words_in_db = Word.objects.all().count()
        total_meanings_in_db = Meaning.objects.all().count()
    except Exception as e:
        print(f"An error occured while trying to prepare stats: {str(e)}")

    stats = f"\nWords in file:{total_words_in_file}\nWords in database: {total_words_in_db}\nMeanings in file: {total_meanings_in_file}\nMeanings in database: {total_meanings_in_db}"

    try:
        if (total_words_in_file == total_words_in_db) and (total_meanings_in_file == total_meanings_in_db):
            print("All items from the file have been added to the database.", stats)
            sys.exit()
    except Exception as e:
        print(stats,
              f"An error occures: \nstr{(e)}")


if __name__ == "__main__":
    run()
