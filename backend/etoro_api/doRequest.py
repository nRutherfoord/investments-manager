import os
import uuid

import requests


def doRequest(url, params=None):
    try:
        api_key = os.environ.get("ETORO_PUBLIC_KEY")
        user_key = os.environ.get("ETORO_PRIVATE_KEY")

        if not api_key or not user_key:
            raise RuntimeError("eToro API keys are not configured")

        headers = {
            "x-api-key": api_key,
            "x-user-key": user_key,
            "x-request-id": str(uuid.uuid4()),
        }

        response = requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        return response
    except Exception as e:
        print(e)
        raise
