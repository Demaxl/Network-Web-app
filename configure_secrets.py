import requests
import os
import environ
from base64 import b64encode
from nacl import encoding, public

env = environ.Env(
    REPOSITORY_OWNER=(str, 'demaxl'))

environ.Env.read_env('.env')

# GitHub repository and personal access token details
REPOSITORY_OWNER = env('REPOSITORY_OWNER')
REPOSITORY_NAME = env("RESPOSITORY_NAME")
TOKEN = env('GITHUB_ACCESS_TOKEN')
HEADERS = {"Authorization": f"token {TOKEN}"}
BASE_URL = "https://api.github.com"


def get_public_key():
    """Returns the public key credentials for the repository."""
    # endpoint to get public key
    url = f"{BASE_URL}/repos/{REPOSITORY_OWNER}/{REPOSITORY_NAME}/actions/secrets/public-key"

    response = requests.get(url, headers=HEADERS)

    return response.json()


def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(
        public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")



def add_secrets():
    # URL for adding repository secrets
    url = f"{BASE_URL}/repos/{REPOSITORY_OWNER}/{REPOSITORY_NAME}/actions/secrets/"
    public_key = get_public_key()

    # Read secrets from .env file
    with open('.env', 'r') as file:
        lines = file.readlines()
        secrets = [line.strip().split('=', 1) for line in lines if '=' in line and not line.startswith('#')]

    # Add each secret to the repository
    for secret in secrets:
        secret_name, secret_value = secret
        payload = {
            "encrypted_value": encrypt(public_key['key'], secret_value),
            "key_id": public_key["key_id"]
        }
        
        response = requests.put(url + secret_name, json=payload, headers=HEADERS)

        if response.status_code == 201:
            print(f"Secret '{secret_name}' added successfully.")
        else:
            print(
                f"Failed to add secret '{secret_name}'. Status code: {response.status_code}")

if __name__ == "__main__":
    add_secrets()
