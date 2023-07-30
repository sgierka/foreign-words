import json
import os
import sys
import time
from generator.models import Meaning, Word
from django.db import transaction


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(
            f"Execution time of {func.__name__}: {execution_time:.6f} seconds")
        return result
    return wrapper


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


@measure_execution_time
def data_to_models(data):
    """Assumed data model in JSON:
        "abaja": [
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
    try:
        with transaction.atomic():
            Word.objects.all().delete()
            Meaning.objects.all().delete()

            words_to_create = []
            meanings_to_create = []

            for word, meaning in data.items():
                # if there's no 'Word' in database - create
                if not Word.objects.filter(word=word).exists():
                    word_obj = Word(word=word)
                    words_to_create.append(Word(word=word))

            # Save the Word objects first
            Word.objects.bulk_create(words_to_create)

            # Fetch all Word objects from the database
            words_in_db = Word.objects.all()

            for word, meaning in data.items():
                word_obj = words_in_db.get(word=word)

                if isinstance(meaning, list):
                    joined_meaning = ', '.join(meaning)
                    meanings_to_create.append(
                        Meaning(word=word_obj, meaning=joined_meaning))
                elif isinstance(meaning, dict):
                    for sub_key, sub_meaning in meaning.items():
                        joined_sub_meaning = ', '.join(sub_meaning)
                        meanings_to_create.append(
                            Meaning(word=word_obj, meaning=joined_sub_meaning))

            Meaning.objects.bulk_create(meanings_to_create)
        return len(meanings_to_create)

    except Exception as e:
        print(f"An error occured at data_to_models: {str(e)}")


def run():
    # path settings
    current_directory = os.path.dirname(__file__)
    print(current_directory)
    json_file_path = "../../static/data/"
    json_file_name = "words.json"
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
        print(
              f"An error occures: \nstr{(e)}")


if __name__ == "__main__":
    run()
