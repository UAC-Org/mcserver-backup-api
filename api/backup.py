import os
from typing import Optional
import utils


def generate_backup(source_path: str, archive_path_and_name: str, default_key: Optional[str] = None):
    tar_archive = utils.generate_tar_archive(source_path, archive_path_and_name + ".tar")
    archive = utils.generate_zstd_archive(tar_archive, archive_path_and_name + ".tar.zst")
    os.remove(tar_archive)
    signature = utils.generate_signature(source_path, default_key)
    return archive, signature
