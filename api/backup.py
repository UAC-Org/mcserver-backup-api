import os

import utils


def generate_backup_with_signature(source_path: str, archive_path: str):
    backup_archive = utils.generate_zstd_compressed_tar_archive(
        archive_path, source_path
    )
    signature = utils.generate_signature(backup_archive, backup_archive + ".sig")
    archive = utils.generate_tar_archive(
        archive_path + "-signed.tar", backup_archive, signature
    )
    os.remove(backup_archive)
    os.remove(signature)
    os.rename(archive, archive_path)
    return archive_path
