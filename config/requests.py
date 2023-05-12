import json
from rest_framework.exceptions import APIException
import requests
from config.logger import log_error


def _send_request(url: str, headers: dict, payload: dict):
    r = requests.get(url, headers=headers, data=payload)
    if r.status_code != 200:
        log_error(APIException(f'Request to {url} got status_code: {r.status_code}, payload: {payload}'))
    return json.loads(r.text)


def get_values(_dict, keys):
    return [_dict.get(key) for key in keys]


def get_matching_book_data(name: str):
    url = f"https://openlibrary.org/search.json?title={name}"
    res = _send_request(url=url, headers={}, payload={})
    if res['docs']:
        res = get_values(res['docs'][0], ['key', 'number_of_pages_median', 'subject'])
        return res
    return None, None, None


def get_work_data(work_id: str):
    cover_id, description = "", ""
    url = f"https://openlibrary.org{work_id}.json"
    res = _send_request(url=url, headers={}, payload={})

    if res.keys().__contains__('covers'):
        for _cover_id in res['covers']:
            if _cover_id != -1:
                cover_id = _cover_id
                break

    if res.keys().__contains__('description'):
        description = res['description']
        if isinstance(description, dict):
            description = description['value']

    return cover_id, description
