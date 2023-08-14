import click
import httpx

from pprint import pformat

try:
    from .webhook_api import WebHookManager, WebhookManagerError, WebhookIsNotValid, WebhookDoesNotExist, \
        WRONG_WEBHOOK_TYPES
except ImportError:
    from webhook_api import WebHookManager, WebhookManagerError, WebhookIsNotValid, WebhookDoesNotExist, \
        WRONG_WEBHOOK_TYPES

import typing as t


@click.group()
@click.version_option(prog_name="Discord Scam Webhook Destroyer (Ruiner)", package_name="discord_webhook_scam",
                      version="0.0.1")
def main_group():
    pass


def handle_wrong_webhook_urls(e):
    click.secho(f"Error {type(e)}", fg='red')
    if type(e) is WebhookIsNotValid:
        click.secho("Please, enter right webhook url", fg='red')
    elif type(e) is WebhookDoesNotExist:
        click.secho("This webhook does not exists", fg='red')
    exit(-1)


def delete_webhook(webhook_url):
    webhook = WebHookManager(webhook_url)
    click.secho("Webhook found", fg='green')
    webhook.delete()
    click.secho("Webhook deleted", fg='green')


def info_webhook(webhook_url: str, raw: bool = True):
    if raw is False:
        click.secho("Only JSON print is supported yet")
        return
    webhook = WebHookManager(webhook_url)
    click.secho("Webhook found", fg='green')
    info = webhook.get_raw_json_info()
    click.echo(pformat(info))
    click.echo()


@main_group.command(name="menu", short_help="Just little general menu")
@click.option("--webhook_url", type=str, required=False)
def main_menu(webhook_url: str = None):
    if webhook_url is None:
        webhook_url = click.prompt("Enter webhook url", type=str)
    while True:
        click.secho("Choose an action:")
        click.secho("    d: Delete this webhook")
        click.secho("    i: Print raw info in json about webhook")
        click.secho("    q: Quit")
        ch_char = click.getchar()
        if ch_char == "d":
            delete_webhook(webhook_url)
            click.secho("You delete dirty webhook, so ...")
            break
        elif ch_char == "i":
            info_webhook(webhook_url)
        elif ch_char == "q":
            break
    click.secho("Bye :3", fg='green')


@main_group.command(name="delete", short_help="Simply deletes webhook")
@click.argument('webhook_url', required=True, type=str)
def delete_command(webhook_url):
    """Simply delete webhook"""
    delete_webhook(webhook_url)


@main_group.command(name="info", short_help="Info about webhook")
@click.argument('webhook_url', required=True, type=str)
@click.option('--raw', default=True, type=bool, help="Is data printed in JSON or not", is_flag=True)
def info_command(webhook_url, raw):
    info_webhook(webhook_url, raw)


def main():
    try:
        main_group()
    except Exception as exc:
        handle_wrong_webhook_urls(exc)
