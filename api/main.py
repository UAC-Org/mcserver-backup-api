import argparse
import os
import tempfile
from datetime import datetime, timedelta
from threading import Timer
from typing import NamedTuple, Optional

import backup
import flask
from . import token as tc

app = flask.Flask(__name__)


LastBackupInfo = NamedTuple("LastBackupInfo", time=datetime, archive=str)


@app.route("/get-backup")
def get_backup():
    now = datetime.now()
    last_backup: Optional[LastBackupInfo] = app.config.get("last_backup")  # type: ignore
    if last_backup and last_backup.time - now < timedelta(minutes=1):
        return flask.send_file(last_backup.archive)  # type: ignore
    prefix: str = app.config["prefix"]
    archive = os.path.join(
        tempfile.gettempdir(),
        prefix + now.strftime("%Y%m%d%H%M%S") + "%05d" % now.microsecond + ".tar.zst",
    )
    directory: str = app.config["directory"]
    backup.generate_backup_with_signature(directory, archive)
    app.config["last_backup"] = LastBackupInfo(now, archive)
    _ = Timer(120, os.remove, (archive,)).start()
    return flask.send_file(archive)  # type: ignore


# push backup with token validation
@app.route("/request-backup")
def push():
    token = flask.request.args.get("token")
    if not token:
        return "No token provided."
    if not tc.get_token(token):
        return "Invalid token."
    tc.update_token(token)
    now = datetime.now()
    last_backup: Optional[LastBackupInfo] = app.config.get("last_backup")  # type: ignore
    if last_backup and last_backup.time - now < timedelta(minutes=1):
        return flask.send_file(last_backup.archive)  # type: ignore
    filename = os.path.join(
        tempfile.gettempdir(),
        "mcserer-backup-" + now.strftime("%Y%m%d%H%M%S") + "%05d" % now.microsecond,
    )
    directory: str = app.config["directory"]
    archive = backup.generate_backup(directory, filename)
    app.config["last_backup"] = LastBackupInfo(now, archive)
    return flask.send_file(archive)  # type: ignore


parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--host",
    help="The host of API. (default: 0.0.0.0)",
    type=str,
    required=False,
    default="0.0.0.0",
)
parser.add_argument(
    "-p",
    "--port",
    help="The port of HTTP API. (default: 45850)",
    type=int,
    required=False,
    default=45850,
)
parser.add_argument(
    "-d",
    "--directory",
    help="The directory to backup.",
    type=str,
    required=True,
)
parser.add_argument(
    "-x",
    "--prefix",
    help="The prefix of backup files.",
    type=str,
    required=False,
    default=""
)
args = parser.parse_args()
if not os.path.exists(args.directory):
    exit(print("Invalid directory was specified."))
app.config["directory"] = args.directory
app.config["prefix"] = args.prefix
app.run(args.host, args.port)
