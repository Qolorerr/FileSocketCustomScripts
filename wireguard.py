import ctypes
import subprocess
from argparse import ArgumentParser, Namespace

from config import WIREGUARD_LOCATION, WIREGUARD_CONF_FILE


def start(args: Namespace) -> None:
    conf_file = args.conf_file if args.conf_file is not None else WIREGUARD_CONF_FILE
    exe_location = WIREGUARD_LOCATION / "wireguard.exe"
    conf_file_location = WIREGUARD_LOCATION / f"Data/Configurations/{conf_file}.conf.dpapi"
    command = f'"{exe_location}" /installtunnelservice "{conf_file_location}"'
    out, err = subprocess.Popen(command,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE).communicate()
    if err is not None:
        print(err)
    else:
        print("Wireguard started")


def stop(args: Namespace) -> None:
    conf_file = args.conf_file if args.conf_file is not None else WIREGUARD_CONF_FILE
    exe_location = WIREGUARD_LOCATION / "wireguard.exe"
    command = f'"{exe_location}" /uninstalltunnelservice {conf_file}'
    out, err = subprocess.Popen(command,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE).communicate()
    if err is not None:
        print(err)
    else:
        print("Wireguard stopped")


def _is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    if not _is_admin():
        print("Admin rights required")

    arg_parser = ArgumentParser()
    subparsers = arg_parser.add_subparsers(help='Methods')

    start_parser = subparsers.add_parser('start', help='Start wireguard')
    start_parser.add_argument('-conf_file', type=str, help='Specify conf file')
    start_parser.set_defaults(func=start)

    stop_parser = subparsers.add_parser('stop', help='Stop wireguard')
    stop_parser.add_argument('-conf_file', type=str, help='Specify conf file')
    stop_parser.set_defaults(func=stop)

    args = arg_parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        print("Use wireguard.py -h")
