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

def run():
    # path settings
    current_directory = os.path.dirname(__file__)
    json_file_path = "../../static/data"
    json_file_name = "/words.json"
    file_path = os.path.join(current_directory, json_file_path+json_file_name)

    data = import_from_file(file_path)
    data_to_models(data)


if __name__ == "__main__":
    run()
