from argparse import ArgumentParser, Namespace, ArgumentError
from pathlib import Path
from zipfile import ZipFile
from os import walk


def zip_it(args: Namespace) -> None:
    path = Path(args.path)
    zip_file_path = path.parent / f"{path.stem}.zip"
    if path.is_file():
        with ZipFile(zip_file_path, "w") as zip_file:
            zip_file.write(path, path.name)
        return

    with ZipFile(zip_file_path, "w") as zip_file:
        for root, dirs, files in walk(path):
            archive_path = Path(root).relative_to(path)
            for file in files:
                zip_file.write(Path(root) / file, archive_path / file)


def unzip_it(args: Namespace) -> None:
    pass


def path_type(path_like: str) -> Path:
    path = Path(path_like)
    if path.exists():
        return path
    else:
        raise ArgumentError(None, f"{path_like} is not valid path")


def zip_type(path_like: str) -> Path:
    path = Path(path_like)
    if path.exists() and path.is_file() and path.suffix == '.zip':
        return path
    else:
        raise ArgumentError(None, f"{path_like} is not valid zip file path")


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    subparsers = arg_parser.add_subparsers(help='Methods')

    start_parser = subparsers.add_parser('zip', help='Zip directory or file')
    start_parser.add_argument('path', type=path_type, help='Path to file or directory to zip')
    start_parser.set_defaults(func=zip_it)

    stop_parser = subparsers.add_parser('unzip', help='Unzip file')
    stop_parser.add_argument('path', type=str, help='Path to zip file to unzip')
    stop_parser.set_defaults(func=unzip_it)

    args = arg_parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        print("Use zipper.py -h")
