from generator.models import KeyModel, ValueModel
import json
import os


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

    try:
        for key_name, value_name in data.items():
            key_model, _ = KeyModel.objects.get_or_create(key=key_name)

            if isinstance(value_name, list):
                for value in value_name:
                    ValueModel.objects.create(
                        key_name=key_model, value_name=value)
            elif isinstance(value_name, dict):
                for sub_key, sub_values in value_name.items():
                    for value in sub_values:
                        ValueModel.objects.create(
                            key_name=key_model, value_name=value)
    except Exception as e:
        print(f"An error occured at data_to_models: {str(e)}")


def elements_count(data):
    total_keys_in_file = len(data.keys())
    total_values_in_file = len(data.values())

    total_keys_in_db = KeyModel.objects.all().count()
    total_values_in_db = ValueModel.objects.all().count()

    try:
        if (total_keys_in_file == total_keys_in_db) and (total_values_in_file == total_values_in_db):
            sys.exit("All items from the file have been added to the database.")
    except Exception as e:
        print(
            f"Not all items in the file were added correctly.\n{total_keys_in_file}/{total_keys_in_db}\n{total_values_in_file}/{total_values_in_db}")


def run():
    # path settings
    current_directory = os.path.dirname(__file__)
    json_file_path = "../../static/data/"
    json_file_name = "words.json"
    file_path = os.path.join(current_directory, json_file_path+json_file_name)

    data = import_from_file(file_path)
    data_to_models(data)
    elements_count(data)


if __name__ == "__main__":
    run()
