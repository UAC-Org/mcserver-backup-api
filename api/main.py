from datetime import datetime
import argparse
import os
import tempfile
import flask
import backup
import utils


app = flask.Flask(__name__)
backup_directory: str = ""


@app.route("/generate")
def generate():
    now = datetime.now()
    filename = os.path.join(
        tempfile.gettempdir(),
        "mcserer-backup-" + now.strftime("%Y%m%d%H%M%S") + str(now.microsecond)
    )
    backup_archive, signature = backup.generate_backup(
        backup_directory, filename
    )
    archive = filename + "-signed.tar"
    utils.generate_tar_archive(archive, backup_archive, signature)
    return flask.send_file(archive)  # type: ignore


parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", "--host",
    help="The host of API. (default: 0.0.0.0)",
    type=str,
    required=False, default="0.0.0.0"
)
parser.add_argument(
    "-p", "--port",
    help="The port of HTTP API. (default: 45850)",
    type=int,
    required=False, default=45850,
)
parser.add_argument(
    "-d", "--directory",
    help="The directory to backup.",
    type=str,
    required=True,
)
args = parser.parse_args()
if not os.path.exists(args.directory):
    exit(print("Invalid directory was specified."))
backup_directory = args.directory
app.run(args.host, args.port)
