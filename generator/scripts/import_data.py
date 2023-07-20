from .generator.models import KeyModel, ValueModel


def import_data_to_models(data):
    for key_name, value_name in data.items():
        key_model, _ = KeyModel.objects.get_or_create(key=key_name)

        if isinstance(values, list):
            for value_name in values:
                ValueModel.objects.create(
                    key_name=key_model, value_name=value_name)
        elif isinstance(values, dict):
            for sub_key, sub_values in values.items():
                for values in sub_values:
                    ValueModel.objects.create(
                        key_name=key_model, value_name=value_name)
