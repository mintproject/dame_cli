from pathlib import Path

import click


def find_file_directory(data_dir, _format=None):
    """
    Find the files by format on the data_dir
    :param data_dir: The local directory where the files are
    :type data_dir: Path
    :param _format:
    :type _format:
    """
    if _format is not None:
        _format = _format.replace(".", "")
        files = [f for f in data_dir.glob("*{}".format(_format))]
        if len(files) > 1:
            print_choices([f.resolve().expanduser() for f in files])
            file_index = click.prompt("Select the file",
                                      type=click.Choice(range(1, len(files) + 1)),
                                      show_choices=True,
                                      value_proc=parse
                                      )
            click.secho("Selected from your computer {}".format(files[file_index-1]))
            return str(files[file_index-1])
        elif len(files) == 1:
            click.secho("Selected from your computer {}".format(files[0]))
            return str(files[0])
        else:
            click.secho("There is not files with format {} on {}".format(_format, data_dir))
    return None

def print_choices(choices):
    for index, choice in enumerate(choices):
        click.echo("[{}] {}".format(index + 1, choice))


def parse(value):
    try:
        return int(value)
    except:
        return value
