import requests
from dotenv import load_dotenv
import json
import os

load_dotenv()

url = os.getenv("API_URL")

token = os.getenv("BEARER_TOKEN")
debug = os.getenv("DEBUG")  # Set debug to True to enable debugging

archived_feedback = {} # Archive feedback per request, to prevent model from hallucinating average score

def get_menu():
    endpoint = url + "menu"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    if debug:
        print("URL:", endpoint)

    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        print("Error fetching menu:", e)
        return None


def place_order(item, quantity):
    endpoint = url + "orders"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "item": item,
        "quantity": quantity
    }

    # Make sure the first letter is capitalised
    data['item'] = data['item'].capitalize()

    if debug:
        print("URL:", endpoint)
        print("Payload:", data)

    try:
        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code in [400, 200]:
            return json.dumps(response.json())
        
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print("Error placing order:", e)
        return None


def get_feedback():
    endpoint = url + "feedback"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    if debug:
        print("URL:", endpoint)

    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()

        global archived_feedback
        archived_feedback = response.json()

        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        print("Error fetching feedback:", e)
        return None


def submit_feedback(comment, rating):
    endpoint = url + "feedback"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "comment": comment,
        "rating": rating
    }

    if debug:
        print("URL:", endpoint)
        print("Payload:", data)

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        print("Error submitting feedback:", e)
        return None


def get_inventory():
    endpoint = url + "inventory"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    if debug:
        print("URL:", endpoint)

    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        print("Error fetching inventory:", e)
        return None


def restock_item(item, quantity):
    endpoint = url + "restock"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "item": item,
        "quantity": quantity
    }

    if debug:
        print("URL:", endpoint)
        print("Payload:", data)

    try:
        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code in [400, 200]:
            return json.dumps(response.json())
        
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print("Error restocking item:", e)
        return None


def submit_report(feedback_summary, average_rating):

    endpoint = url + "report"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    ratings = [feedback['rating'] for feedback in archived_feedback['feedback']]
    if ratings:
        real_average_rating = sum(ratings) / len(ratings)
    else:
        real_average_rating = average_rating

    data = {
        "feedback_summary": feedback_summary,
        "average_rating": real_average_rating
    }

    if debug:
        print("URL:", endpoint)
        print("Payload:", data)

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        print("Error submitting report:", e)
        return None


tools = {get_menu, place_order, get_feedback, submit_feedback, get_inventory, restock_item, submit_report}
