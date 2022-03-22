import mimetypes
import os
import re
import sys
import tarfile
import zipfile
from pathlib import Path
from types import SimpleNamespace

import aiofiles
from bs4 import BeautifulSoup

LOCAL_VERSIONS = {}
REMOTE_VERSIONS = {}


async def local_version_list(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    ret = {}
    versions_dir = Path(hub.OPT.saltenv.saltenv_dir) / "versions"
    if versions_dir.exists():
        ret = versions_dir.glob("salt-*")
        ret = {ver.name.replace("salt-", ""): ver for ver in ret}
    return ret


async def fill_local_version_list(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    hub.saltenv.ops.LOCAL_VERSIONS = await hub.saltenv.ops.local_version_list()


async def remote_version_list(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    ret = {}
    ctx = SimpleNamespace(acct={})
    repo_list = await hub.exec.request.raw.get(
        ctx,
        url=hub.OPT.saltenv.repo_url,
    )
    if repo_list.get("ret"):
        soup = BeautifulSoup(repo_list["ret"], "html.parser")
        ret = {
            re.sub(r"-\d+$", "", node["href"][:-1]): node["href"][:-1]
            for node in soup.find_all("a")
            if node.get("href") and node["href"].endswith("/") and node["href"] != "../"
        }
    return ret


async def fill_remote_version_list(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    hub.saltenv.ops.REMOTE_VERSIONS = await hub.saltenv.ops.remote_version_list()


async def download_version(hub, version, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    ret = False
    ctx = SimpleNamespace(acct={})
    if not hub.saltenv.ops.REMOTE_VERSIONS:
        await hub.saltenv.ops.fill_remote_version_list()

    if version in hub.saltenv.ops.REMOTE_VERSIONS:
        file_list = await hub.exec.request.raw.get(
            ctx,
            url=f"{hub.OPT.saltenv.repo_url}/{hub.saltenv.ops.REMOTE_VERSIONS[version]}",
        )
        soup = BeautifulSoup(file_list["ret"], "html.parser")
        links = [
            node["href"]
            for node in soup.find_all("a")
            if node.get("href") and not node["href"].endswith("/") and node["href"] != "../"
        ]

        arch = os.uname().machine
        if arch == "x86_64":
            arch = "amd64"

        pkg_name = ""
        # TODO: verify download with SHA/GPG
        for link in links:
            if arch in link and sys.platform in link:
                pkg_name = link

        if pkg_name:
            outfile = Path(hub.OPT.saltenv.saltenv_dir) / "downloads" / pkg_name
            outfile.parent.mkdir(parents=True, exist_ok=True)
            versions_dir = Path(hub.OPT.saltenv.saltenv_dir) / "versions"
            versions_dir.mkdir(parents=True, exist_ok=True)
            salt_bin_in = versions_dir / "salt"
            salt_bin_out = versions_dir / f"salt-{version}"

            download_url = "/".join(
                [
                    hub.OPT.saltenv.repo_url,
                    hub.saltenv.ops.REMOTE_VERSIONS[version],
                    pkg_name,
                ]
            )

            pkg = {}
            if not outfile.exists():
                pkg = await hub.exec.request.raw.get(
                    ctx,
                    url=download_url,
                )
                async with aiofiles.open(outfile, "wb") as ofile:
                    await ofile.write(pkg["ret"])

            if (outfile.exists() and not salt_bin_out.exists()) or (pkg and pkg["status"] == 200):
                filemimetype = mimetypes.guess_type(str(outfile))

                if (
                    filemimetype and filemimetype[0] == "application/zip"
                ) or outfile.suffix == ".zip":
                    print("Processing zip file...")
                    if zipfile.is_zipfile(outfile):
                        zip_source = zipfile.ZipFile(outfile)
                        zip_source.extractall(versions_dir)
                        if salt_bin_in.exists():
                            salt_bin_in.rename(salt_bin_out)
                        ret = salt_bin_out.exists()
                    else:
                        print(f"ERROR: Unable to extract {outfile}")
                elif filemimetype == ("application/x-tar", "gzip") or str(outfile).endswith(
                    ".tar.gz"
                ):
                    print("Processing tarball...")
                    if tarfile.is_tarfile(outfile):
                        with tarfile.open(outfile) as tar_source:
                            tar_source.extractall(versions_dir)
                        if salt_bin_in.exists():
                            salt_bin_in.rename(salt_bin_out)
                        ret = salt_bin_out.exists()
                    else:
                        print(f"ERROR: Unable to extract {outfile}")
                else:
                    print(f"ERROR: Unknown file type for download {outfile}: {filemimetype}")
    return ret


async def get_current_version(hub, **kwargs):
    """
    Read the current active version from ./.salt-version and the main version
    file at ${SALTENV_DIR}/version. The former overrides the latter.
    """
    ret = ("", "")
    override_version_file = Path(os.getcwd()) / ".salt-version"
    main_version_file = Path(hub.OPT.saltenv.saltenv_dir) / "version"

    if override_version_file.exists():
        async with aiofiles.open(override_version_file, "r") as cfile:
            current_version = await cfile.read()
            current_version = current_version.replace("\n", "").strip()
        ret = (current_version, str(override_version_file))

    if not ret[0] and main_version_file.exists():
        async with aiofiles.open(main_version_file, "r") as vfile:
            current_version = await vfile.read()
            current_version = current_version.replace("\n", "").strip()
        ret = (current_version, str(main_version_file))

    return ret


async def pin_current_version(hub, **kwargs):
    """
    Get the current active version and write it to ./.salt-version
    """
    ret = False
    current_version = await hub.saltenv.ops.get_current_version()
    override_version_file = Path(os.getcwd()) / ".salt-version"

    if current_version[0]:
        async with aiofiles.open(override_version_file, "w") as ofile:
            await ofile.write(current_version[0])
        ret = True

    return ret


async def remove_version(hub, version, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    salt_bin = hub.saltenv.ops.LOCAL_VERSIONS.get(version)
    if salt_bin:
        salt_bin.unlink()

    return True


async def use_version(hub, version, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    if not hub.saltenv.ops.LOCAL_VERSIONS:
        await hub.saltenv.ops.fill_local_version_list()

    if version in hub.saltenv.ops.LOCAL_VERSIONS:
        version_file = Path(hub.OPT.saltenv.saltenv_dir) / "version"
        version_file.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(version_file, "w") as vfile:
            await vfile.write(version)
    else:
        print(f"{version} is not installed. Run 'saltenv install {version}' first.")

    return True
