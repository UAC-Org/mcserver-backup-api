import os
import utils


def generate_backup(source_path: str, archive_path_and_name: str):
    tar_archive = utils.generate_tar_archive(
        archive_path_and_name + ".tar", source_path
    )
    backup_archive = utils.generate_zstd_archive(
        tar_archive, archive_path_and_name + ".tar.zst"
    )
    os.remove(tar_archive)
    signature = utils.generate_signature(backup_archive, backup_archive + ".sig")
    archive = archive_path_and_name + "-signed.tar"
    utils.generate_tar_archive(archive, backup_archive, signature)
    os.remove(backup_archive)
    os.remove(signature)
    return archive
