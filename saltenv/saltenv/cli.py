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

__func_alias__ = {"list_": "list"}
LOCAL_VERSIONS = []
REMOTE_VERSIONS = {}


async def local_version_list(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    ret = {}
    versions_dir = Path(hub.OPT.saltenv.saltenv_dir) / "versions"
    if versions_dir.exists():
        ret = versions_dir.glob("salt-*")
        ret = {ver.stem.replace("salt-", ""): ver for ver in ret}
    return ret


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


async def download_version(hub, version, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    ret = False
    ctx = SimpleNamespace(acct={})
    if not hub.saltenv.cli.REMOTE_VERSIONS:
        hub.saltenv.cli.REMOTE_VERSIONS = await hub.saltenv.cli.remote_version_list()

    if version in hub.saltenv.cli.REMOTE_VERSIONS:
        file_list = await hub.exec.request.raw.get(
            ctx,
            url=f"{hub.OPT.saltenv.repo_url}/{hub.saltenv.cli.REMOTE_VERSIONS[version]}",
        )
        soup = BeautifulSoup(file_list["ret"], "html.parser")
        links = [
            node["href"]
            for node in soup.find_all("a")
            if node.get("href")
            and not node["href"].endswith("/")
            and node["href"] != "../"
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
                    hub.saltenv.cli.REMOTE_VERSIONS[version],
                    pkg_name,
                ]
            )

            pkg = {}
            if not outfile.exists():
                pkg = await hub.exec.request.raw.get(
                    ctx,
                    url=download_url,
                )

            if (outfile.exists() and not salt_bin_out.exists()) or (
                pkg and pkg["status"] == 200
            ):
                async with aiofiles.open(outfile, "wb") as ofile:
                    await ofile.write(pkg["ret"])
                filemimetype = mimetypes.guess_type(outfile)

                if (
                    filemimetype and filemimetype[0] == "application/zip"
                ) or outfile.suffix == ".zip":
                    print("Processing zip file...")
                    if zipfile.is_zipfile(outfile):
                        zip_source = zipfile.ZipFile(outfile)
                        zip_source.extractall(versions_dir)
                        if salt_bin_in.exists():
                            salt_bin_in.rename(salt_bin_out)
                elif filemimetype == ("application/x-tar", "gzip") or str(
                    outfile
                ).endswith(".tar.gz"):
                    print("Processing tarball...")
                    if tarfile.is_tarfile(outfile):
                        with tarfile.open(outfile) as tar_source:
                            tar_source.extractall(versions_dir)
                        if salt_bin_in.exists():
                            salt_bin_in.rename(salt_bin_out)
                else:
                    print(
                        f"ERROR: Unknown file type for download {outfile}: {filemimetype}"
                    )
                    return False
                ret = True
    return ret


async def list_(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    versions = await hub.saltenv.cli.local_version_list()
    print("Local versions available:")
    print("\n".join(sorted(versions.keys())))


async def list_remote(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    versions = await hub.saltenv.cli.remote_version_list()
    print("Remote versions available:")
    print("\n".join(sorted(versions.keys())))


async def install(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    hub.saltenv.cli.REMOTE_VERSIONS = await hub.saltenv.cli.remote_version_list()
    hub.saltenv.cli.LOCAL_VERSIONS = await hub.saltenv.cli.local_version_list()

    if hub.OPT.saltenv.salt_version in hub.saltenv.cli.LOCAL_VERSIONS:
        print(f"{hub.OPT.saltenv.salt_version} is already installed.")
    elif hub.OPT.saltenv.salt_version in hub.saltenv.cli.REMOTE_VERSIONS:
        await hub.saltenv.cli.download_version(hub.OPT.saltenv.salt_version)
    else:
        print(f"ERROR: {hub.OPT.saltenv.salt_version} is not available as a binary.")
