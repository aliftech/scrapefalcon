import click
import json
import requests
from rich import print as rprint
from decouple import config


@click.command()
@click.option(
    "-auth",
    "--a",
    "auth",
    type=click.Choice(["login", "register"]),
    required=True,
    help="Use to login or register a new user."
)
@click.option(
    "-username",
    "--u",
    "username",
    type=click.STRING,
    required=True,
    help="Set username value for login or registration."
)
@click.option(
    "-password",
    "--p",
    "password",
    type=click.STRING,
    required=True,
    help="Use to set password for login or registration."
)
@click.option(
    "-email",
    "--e",
    "email",
    type=click.STRING,
    help="Set email value for registration (required for register)."
)
def scrape(auth, username, password, email):
    try:
        if auth == 'register':
            if not email:
                raise click.UsageError("Email is required for registration.")

            headers = {"Content-Type": "application/json"}
            payload = {
                'username': username,
                'email': email,
                'password': password
            }
            payload_json = json.dumps(payload)

            # Assuming 'register' is a function that sends a POST request
            response = requests.post(
                f"{config('app.BaseURL')}signup", headers=headers, data=payload_json)

            rprint(
                f"[bold white]Response: {response.status_code} - {response.text}[/bold white]")
        else:
            # Add logic for 'login' if necessary
            headers = {"Content-Type": "application/json"}
            payload = {
                'username': username,
                'password': password
            }
            payload_json = json.dumps(payload)

            response = requests.post(
                f"{config('app.BaseURL')}signin", headers=headers, data=payload_json)

            rprint(
                f"[bold white]Response: {response.status_code} - {response.text}[/bold white]")

            rprint(
                "[bold yellow]Login functionality is not implemented yet.[/bold yellow]")

    except json.JSONDecodeError as e:
        rprint(f"[bold red]JSON Decode Error: {str(e)}[/bold red]")
    except requests.RequestException as e:
        rprint(f"[bold red]Request Error: {str(e)}[/bold red]")
    except Exception as e:
        rprint(f"[bold red]An error occurred: {str(e)}[/bold red]")


if __name__ == "__main__":
    scrape()
