from requests.exceptions import HTTPError
from flask import render_template
from fastapi.logger import logger
from config import DEV_API_URL
import requests
import json


def get_request(resource: str, template: str):
    try:
        response = requests.get(f"{DEV_API_URL}/{resource}")
        response.raise_for_status()
        json_response = response.json()
        return render_template(template, **{resource: json_response})
    except HTTPError:
        logger.error("Error in Api")
        return render_template("error.html")

    except json.JSONDecodeError:
        logger.error("Error while parsing API response")
        return render_template("error.html")


def post_request(resource: str, template: str, json: dict):
    try:
        response = requests.post(f"{DEV_API_URL}/{resource}", json=json)
        response.raise_for_status()
        response_get = requests.get(f"{DEV_API_URL}/{resource}")
        json_response = response_get.json()
        return render_template(template, **{resource: json_response})
    except HTTPError:
        logger.error("Error in Api")
        return render_template("error.html")
    except json.JSONDecodeError:
        logger.error("Error while parsing API response")
        return render_template("error.html")


def delete_request(template: str, resource: str, parameter: str):
    try:
        response = requests.delete(f"{DEV_API_URL}/{resource}/{parameter}")
        response.raise_for_status()
        updated_task_response = requests.get(f"{DEV_API_URL}/{resource}")
        updated_tasks = updated_task_response.json()
        return render_template(template, **{resource: updated_tasks})
    except HTTPError:
        logger.error("Error in Api")
        return render_template("error.html")
    except json.JSONDecodeError:
        logger.error("Error while parsing API response")
        return render_template("error.html")
