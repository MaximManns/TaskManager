from requests.exceptions import HTTPError
from flask import render_template, redirect
from fastapi.logger import logger
from config import DEV_API_URL
import requests
import json


def get_request(resource: str, template: str):
    try:
        response = requests.get(f"{DEV_API_URL}/{resource}")
        tasks = response.json()
        return render_template({template}, tasks=tasks)
    except HTTPError:
        logger.error("Error in Api")
        return render_template(tasks=[])
    except json.JSONDecodeError:
        logger.error("Error while parsing API response")
        return render_template(tasks=[])


def post_request(json: json):
    try:
        response = requests.post(f"{DEV_API_URL}/users/", json)
        return response.json()
    except HTTPError:
        logger.error("Error in Api")
        return render_template(tasks=[])
    except json.JSONDecodeError:
        logger.error("Error while parsing API response")
        return render_template(tasks=[])


def delete_request(resource: str, parameter: str):
    try:
        requests.delete(f"{DEV_API_URL}/{resource}/{parameter}")
        return redirect('/tasks')
    except HTTPError:
        logger.error("Error in Api")
        return render_template(users=[])
    except json.JSONDecodeError:
        logger.error("Error while parsing API response")
        return render_template(users=[])
