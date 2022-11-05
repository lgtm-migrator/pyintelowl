import click
import click_creds
from rich import print as rprint

from ..cli._utils import ClickContext


@click.group("config")
def config():
    """
    Set or view config variables
    """
    pass


@config.command("get")
@click_creds.pass_netrcstore_obj
def config_get(netrc: click_creds.NetrcStore):
    """
    Pretty Print config variables
    """
    rprint(netrc.host_with_mapping)


@config.command("set")
@click.option(
    "-k",
    "--api-key",
    required=False,
    help="API key to authenticate against a IntelOwl instance",
)
@click.option(
    "-u",
    "--instance-url",
    required=False,
    default="http://localhost:80",
    show_default=True,
    help="IntelOwl's instance URL",
)
@click.option(
    "-c",
    "--certificate",
    required=False,
    type=click.Path(exists=True),
    help="Path to SSL client certificate file (.pem)",
)
@click.option(
    "-v",
    "--verify",
    required=False,
    default=True,
    show_default=True,
    type=click.BOOL,
    help="Boolean determining whether certificate validation is enforced",
)
@click.option(
    "-p",
    "--http-proxy",
    required=False,
    default="",
    help="HTTP proxy URL",
)
@click.option(
    "-ps",
    "--https-proxy",
    required=False,
    default="",
    help="HTTPS proxy URL",
)
@click.pass_context
def config_set(
    ctx: ClickContext,
    api_key,
    instance_url,
    certificate,
    verify,
    http_proxy,
    https_proxy,
):
    """
    Set/Edit config variables
    """
    netrc: click_creds.NetrcStore = click_creds.get_netrc_object_from_ctx(ctx)
    new_host = netrc.host.copy()
    if api_key:
        new_host["password"] = api_key
    if instance_url:
        new_host["account"] = instance_url
    if certificate:
        new_host["login"] = certificate
    if verify is False:
        new_host["login"] = False
    if http_proxy:
        new_host["http_proxy"] = http_proxy
    if https_proxy:
        new_host["https_proxy"] = https_proxy
    # finally save
    netrc.save(new_host)
    ctx.obj.logger.info(f"Successfully saved config variables! {new_host}")
