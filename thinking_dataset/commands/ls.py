# @file thinking_dataset/commands/ls.py
# @description Command to list all files in the DataTonic dataset directory.
# @version 1.0.20
# @license MIT

import click
import thinking_dataset.config as conf
import thinking_dataset.config.config_keys as Keys
import thinking_dataset.dataset as Dataset

from thinking_dataset.utils.log import Log as log
from thinking_dataset.data.data_tonic import DataTonic
from thinking_dataset.utils.exceptions import exceptions

CK = Keys.ConfigKeys
D = Dataset.Dataset
DT = DataTonic


@click.command()
@exceptions
@log.level(log.CRITICAL)
def ls():
    try:
        conf.initialize()
        org = conf.get_env_value(CK.HF_ORG)
        user = conf.get_env_value(CK.HF_USER)
        read_token = conf.get_env_value(CK.HF_READ_TOKEN)
        write_token = conf.get_env_value(CK.HF_WRITE_TOKEN)

        dt = DT(read_token=read_token,
                write_token=write_token,
                org=org,
                user=user)

        d = D(dt)
        files = d.get_file_list()

        if not files:
            click.echo("No files found.")
            return

        click.echo("Files in the dataset:")
        for file in files:
            click.echo(f"- {file.name}")

    except Exception as e:
        raise e


if __name__ == '__main__':
    ls()
