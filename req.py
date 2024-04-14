import requests

def get_views_from_Id(id):
    url = f'https://giphy.com/api/v1/proxy-gif/{id}/view-count/'
    # print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['viewCount'], response.status_code
        else:
            print(f'Request failed with status code {response.status_code} : {response.reason} ')
            return f'Request failed with status code {response.status_code} : {response.reason} ' , response.status_code

    except requests.RequestException as e:
        print(f'An error occured: {e}')
        return f'An error occured: {e}'
    