
def fetch_number_of_pages(json):
    return json['pagination']['total_pages']


def fetch_animals_data(json):
    return json['animals']
