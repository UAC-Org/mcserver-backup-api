import argparse
import os
import tempfile
from datetime import datetime, timedelta
from threading import Timer
from typing import Optional, Tuple

import backup
import flask

app = flask.Flask(__name__)
backup_directory: str = ""
last_backup: Optional[Tuple[datetime, str]] = None


@app.route("/get-backup")
def generate():
    global last_backup
    now = datetime.now()
    if last_backup and last_backup[0] - now < timedelta(minutes=1):
        return flask.send_file(last_backup[1])  # type: ignore
    filename = os.path.join(
        tempfile.gettempdir(),
        "mcserer-backup-" + now.strftime("%Y%m%d%H%M%S") + str(now.microsecond),
    )
    archive = backup.generate_backup(backup_directory, filename)
    last_backup = (now, archive)
    _ = Timer(120, os.remove, archive).start()
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
args = parser.parse_args()
if not os.path.exists(args.directory):
    exit(print("Invalid directory was specified."))
backup_directory = args.directory
app.run(args.host, args.port)
