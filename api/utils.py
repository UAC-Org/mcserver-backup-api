from typing import Optional


def generate_tar_archive(archive_path: str, *sources: str):
    import tarfile
    with tarfile.open(archive_path, "w") as archive:
        for source in sources:
            archive.add(source)
    return archive_path


def generate_zstd_archive(source_path: str, archive_path: str):
    import zstandard
    compressor = zstandard.ZstdCompressor()
    compressor.compressobj
    with open(source_path, "rb") as source, open(archive_path, "wb") as archive:
        compressor.copy_stream(source, archive)
    return archive_path


def generate_signature(file_path: str, default_key: Optional[str] = None):
    import gnupg  # type: ignore
    gpg = gnupg.GPG()
    args = {"data": file_path, "detach": True}
    if default_key:
        args["default_key"] = default_key
    gpg.sign(**args)  # type: ignore
    return file_path + ".sig"
