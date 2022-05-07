from typing import Optional
import argparse
import os
import tempfile
import flask
import backup
import utils


app = flask.Flask(__name__)
backup_directory: str = ""
default_key: Optional[str] = None


@app.route("/generate")
def generate():
    _, file = tempfile.mkstemp()
    backup_archive, signature = backup.generate_backup(backup_directory, file, default_key)
    archive = utils.generate_tar_archive(file + "-signed.tar.zst", backup_archive, signature)
    return app.send_static_file(archive)


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
parser.add_argument(
    "-k", "--key",
    help="The key used to sign archive.",
    type=str,
    required=False, default=None
)
args = parser.parse_args()
if not os.path.exists(args.directory):
    exit(print("Invalid directory was specified."))
backup_directory = args.directory
app.run(args.host, args.port)
