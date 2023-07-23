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
    count_meanings = 0

    try:
        for word, meaning in data.items():
            word_obj, created = Word.objects.get_or_create(word=word)
            if isinstance(meaning, list):
                meaning_obj = Meaning.objects.get_or_create(
                    word=word_obj, meaning=meaning)
                count_meanings += 1
            elif isinstance(meaning, dict):
                for sub_key, sub_meaning in meaning.items():
                    meaning_obj = Meaning.objects.get_or_create(
                        word=word_obj, meaning=sub_meaning)
                    count_meanings += 1
        return count_meanings
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

    total_words_in_file = len(data.keys())
    total_meanings_in_file = data_to_models(data)
    total_words_in_db = Word.objects.all().count()
    total_meanings_in_db = Meaning.objects.all().count()

    stats = f"\nWords in file:{total_words_in_file}\nWords in database: {total_words_in_db}\nMeanings in file: {total_meanings_in_file}\nMeanings in database: {total_meanings_in_db}"

    try:
        if (total_words_in_file == total_words_in_db) and (total_meanings_in_file == total_meanings_in_db):
            print("All items from the file have been added to the database.", stats)
            sys.exit()
    except Exception as e:
        print(
            f"Not all items in the file were added correctly.", stats)

    # print(f"Counting amounts...\n{total_words_in_file}/{total_words_in_db}\n{total_meanings_in_file}/{total_meanings_in_db}")
    # try:
    #     if (total_words_in_file == total_words_in_db) and (total_meanings_in_file == total_meanings_in_db):
    #         print(f"All items from the file have been added to the database.\n{total_words_in_file}/{total_words_in_db}\n{total_meanings_in_file}/{total_meanings_in_db}")
    #         sys.exit("looooool")
    # except Exception as e:
    #     print(
    #         f"Not all items in the file were added correctly.\n{total_words_in_file}/{total_words_in_db}\n{total_meanings_in_file}/{total_meanings_in_db}")
if __name__ == "__main__":
    run()
