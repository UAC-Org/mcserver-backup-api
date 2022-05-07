def generate_tar_archive(archive_path: str, *sources: str):
    import os
    import tarfile

    with tarfile.open(archive_path, "w") as archive:
        for source in sources:
            archive.add(source, arcname=os.path.split(source)[1])
    return archive_path


def generate_zstd_archive(source_path: str, archive_path: str):
    import zstandard

    compressor = zstandard.ZstdCompressor()
    with open(source_path, "rb") as source, open(archive_path, "wb") as archive:
        compressor.copy_stream(source, archive)
    return archive_path


def generate_signature(file_path: str, signature_path: str):
    import gnupg  # type: ignore

    gpg = gnupg.GPG()
    with open(file_path, "rb") as file:
        gpg.sign_file(file, detach=True, output=signature_path)  # type: ignore
    return signature_path
