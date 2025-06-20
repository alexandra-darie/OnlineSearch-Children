import requests

def search_brave(query, api_key, count=5):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
       "X-Subscription-Token": api_key,
    }
    params = {
        "q": query,
        "count": count
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
