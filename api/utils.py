from typing import Union


def _try_remove(path: Union[str, bytes]):
    import os

    try:
        os.remove(path)
        return True
    except FileNotFoundError:
        return False


def generate_tar_archive(archive_path: str, *sources: str):
    import os
    import tarfile

    try:
        with tarfile.open(archive_path, "w") as archive:
            for source in sources:
                archive.add(source, arcname=os.path.split(source)[1])
    except:
        _try_remove(archive_path)
    return archive_path


def generate_zstd_compressed_tar_archive(archive_path: str, *sources: str):
    import os
    import tarfile
    import tempfile

    import zstandard

    compressor = zstandard.ZstdCompressor()
    _, tar_archive = tempfile.mkstemp()
    try:
        with tarfile.open(tar_archive, "w") as archive:
            for source in sources:
                archive.add(source, arcname=os.path.split(source)[1])
        with open(tar_archive, "rb") as tar, open(archive_path, "wb") as zstd:
            compressor.copy_stream(tar, zstd)
    except Exception:
        _try_remove(archive_path)
        raise
    finally:
        _try_remove(tar_archive)
    return archive_path


def generate_signature(file_path: str, signature_path: str):
    import gnupg  # type: ignore

    gpg = gnupg.GPG()
    with open(file_path, "rb") as file:
        gpg.sign_file(file, detach=True, output=signature_path)  # type: ignore
    return signature_path
