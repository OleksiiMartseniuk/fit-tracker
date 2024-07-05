import asyncio

import click

from src.account.dto import UserAddDTO
from src.account.services.user import UserService
from src.di import injector


@click.group()
def cli():
    pass


@click.command()
@click.argument("username", type=click.STRING)
@click.argument("password", type=click.STRING)
@click.argument("email", type=click.STRING, required=False)
def createsuperuser(username: str, password: str, email: str = None):
    user_service = injector.get(UserService)
    user_add_dto = UserAddDTO(username=username, password=password, email=email)

    try:
        asyncio.run(user_service.create_superuser(data=user_add_dto))
    except Exception as e:
        click.echo(f"Error creating superuser {username}: {e}")
        return None

    click.echo(f"Created superuser {username}")


cli.add_command(createsuperuser)

if __name__ == "__main__":
    cli()
