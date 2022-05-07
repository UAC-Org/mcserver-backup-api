import os
import utils


def generate_backup(source_path: str, archive_path_and_name: str):
    tar_archive = utils.generate_tar_archive(archive_path_and_name + ".tar", source_path)
    archive = utils.generate_zstd_archive(tar_archive, archive_path_and_name + ".tar.zst")
    os.remove(tar_archive)
    signature = utils.generate_signature(archive, archive + ".sig")
    return archive, signature
