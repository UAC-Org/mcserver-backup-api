def generate_tar_archive(archive_path: str, *sources: str):
    import os
    import tarfile

    with tarfile.open(archive_path, "w") as archive:
        for source in sources:
            archive.add(source, arcname=os.path.split(source)[1])
    return archive_path


def generate_zstd_compressed_tar_archive(archive_path: str, *sources: str):
    import os
    import tarfile
    import zstandard
    import tempfile

    compressor = zstandard.ZstdCompressor()
    _, tar_archive = tempfile.mkstemp()
    with tarfile.open(tar_archive, "w") as archive:
        for source in sources:
            archive.add(source, arcname=os.path.split(source)[1])
    with open(tar_archive, "rb") as tar, open(archive_path, "wb") as zstd:
        compressor.copy_stream(tar, zstd)
    os.remove(tar_archive)
    return archive_path


def generate_signature(file_path: str, signature_path: str):
    import gnupg  # type: ignore

    gpg = gnupg.GPG()
    with open(file_path, "rb") as file:
        gpg.sign_file(file, detach=True, output=signature_path)  # type: ignore
    return signature_path
