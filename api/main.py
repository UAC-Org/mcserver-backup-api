import argparse
import os
import tempfile
from datetime import datetime
from threading import Timer
from typing import Dict, NamedTuple

import backup
import flask
import tokens

app = flask.Flask(__name__)


RequestInfo = NamedTuple("RequestInfo", times=int, archive=str)


@app.route("/get-backup")
def get_backup():
    token = flask.request.args.get("token")
    if not token:
        return "No token provided."
    if not tokens.exist(token):
        return "Invalid token."
    requests: Dict[str, RequestInfo] = app.config["client_requests"]
    if not tokens.timeout(token):
        request = requests.get(token)
        if request:
            if request.times < 5:
                requests[token] = RequestInfo(request.times + 1, request.archive)
                return flask.send_file(request.archive)  # type: ignore
    tokens.update_token(token)
    now = datetime.now()
    prefix: str = app.config["prefix"]
    archive = os.path.join(
        tempfile.gettempdir(),
        prefix + now.strftime("%Y%m%d%H%M%S") + "%05d" % now.microsecond + ".tar",
    )
    directory: str = app.config["directory"]
    backup.generate_backup_with_signature(directory, archive)
    requests[token] = RequestInfo(1, archive)
    _ = Timer(300, os.remove, (archive,)).start()
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
    default="",
)
args = parser.parse_args()
if not os.path.exists(args.directory):
    exit(print("Invalid directory was specified."))
app.config["directory"] = args.directory
app.config["prefix"] = args.prefix
app.config["client_requests"] = {}
app.run(args.host, args.port)
