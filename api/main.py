import argparse
import os
import tempfile
from datetime import datetime, timedelta
from threading import Timer
from typing import NamedTuple, Optional

import backup
import flask

app = flask.Flask(__name__)


LastBackupInfo = NamedTuple("LastBackupInfo", time=datetime, archive=str)


@app.route("/get-backup")
def get_backup():
    now = datetime.now()
    last_backup: Optional[LastBackupInfo] = app.config.get("last_backup")  # type: ignore
    if last_backup and last_backup.time - now < timedelta(minutes=1):
        return flask.send_file(last_backup.archive)  # type: ignore
    filename = os.path.join(
        tempfile.gettempdir(),
        "mcserer-backup-" + now.strftime("%Y%m%d%H%M%S") + "%05d" % now.microsecond,
    )
    directory: str = app.config["directory"]
    archive = backup.generate_backup_with_signature(directory, filename)
    app.config["last_backup"] = LastBackupInfo(now, archive)
    _ = Timer(120, os.remove, (archive,)).start()
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
app.config["directory"] = args.directory
app.run(args.host, args.port)
