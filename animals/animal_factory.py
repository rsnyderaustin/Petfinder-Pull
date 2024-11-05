from .animal import Animal


def _expand_dict(key, dict_) -> dict:
    data = {}
    for k, v in dict_.items():
        new_key = f"{key}{k}"
        data[new_key] = v
    return data


def _reformat_dict(dict_) -> dict:
    new_dict = {}
    for k, v in dict_.items():
        if isinstance(v, dict):
            expanded_dict = _expand_dict(k, v)
            new_dict.update(expanded_dict)
        else:
            new_dict[k] = v

    return new_dict


def create_animal(**params):
    data = _reformat_dict(params)
    new_animal = Animal(
        animal_id=data['animal_id'],
        org_id=data['organization_id'],
        status=data['status'],
        **{k: v for k, v in data.items() if k not in ['animal_id', 'organization_id', 'status']}
    )
    return new_animal
