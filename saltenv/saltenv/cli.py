from pathlib import Path
from textwrap import dedent

import aiofiles

__func_alias__ = {"list_": "list"}


async def list_(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.saltenv.ops.fill_local_version_list()
    current_version = await hub.saltenv.ops.get_current_version()
    version_list = []
    for ver in sorted(hub.saltenv.ops.LOCAL_VERSIONS.keys(), reverse=True):
        prefix = "  "
        suffix = ""
        if ver == current_version[0]:
            prefix = "* "
            suffix = f" (set by {current_version[1]})"
        version_list.append(prefix + ver + suffix)
    print("\n".join(version_list))


async def list_remote(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.saltenv.ops.fill_remote_version_list()
    print("\n".join(sorted(hub.saltenv.ops.REMOTE_VERSIONS.keys(), reverse=True)))


async def install(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.saltenv.ops.fill_remote_version_list()
    await hub.saltenv.ops.fill_local_version_list()

    if hub.OPT.saltenv.salt_version in hub.saltenv.ops.LOCAL_VERSIONS:
        print(f"{hub.OPT.saltenv.salt_version} is already installed.")
    elif hub.OPT.saltenv.salt_version in hub.saltenv.ops.REMOTE_VERSIONS:
        await hub.saltenv.ops.download_version(hub.OPT.saltenv.salt_version)
    else:
        print(f"ERROR: {hub.OPT.saltenv.salt_version} is not available as a binary.")


async def uninstall(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.saltenv.ops.fill_remote_version_list()
    await hub.saltenv.ops.fill_local_version_list()

    if hub.OPT.saltenv.salt_version in hub.saltenv.ops.LOCAL_VERSIONS:
        await hub.saltenv.ops.remove_version(hub.OPT.saltenv.salt_version)
    else:
        print(f"{hub.OPT.saltenv.salt_version} is already uninstalled.")


async def use(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.saltenv.ops.use_version(hub.OPT.saltenv.salt_version)


async def pin(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.saltenv.ops.pin_current_version()


async def version(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    current_version = await hub.saltenv.ops.get_current_version()
    if current_version[0]:
        print(f"{current_version[0]} (set by {current_version[1]})")
    else:
        print("ERROR: No version of Salt is set!")


async def init(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    salt_bin = Path(hub.OPT.saltenv.saltenv_dir) / "bin" / "salt"
    salt_bin.parent.mkdir(parents=True, exist_ok=True)
    minion_config = Path(hub.OPT.saltenv.saltenv_dir) / "etc" / "salt" / "minion"
    minion_config.parent.mkdir(parents=True, exist_ok=True)

    wrapper = dedent(
        f"""
        #!/usr/bin/env python3

        import os
        import subprocess
        import sys
        from pathlib import Path

        if __name__ == "__main__":
            saltenv_dir = Path("{hub.OPT.saltenv.saltenv_dir}")
            override_version_file = Path(os.getcwd()) / ".salt-version"
            main_version_file = saltenv_dir / "version"

            current_version = ""

            if override_version_file.exists():
                with open(override_version_file, "r") as cfile:
                    current_version = cfile.read()
                    current_version = current_version.replace("\\n", "").strip()

            if not current_version and main_version_file.exists():
                with open(main_version_file, "r") as vfile:
                    current_version = vfile.read()
                    current_version = current_version.replace("\\n", "").strip()

            current_bin = saltenv_dir / "versions" / ("salt-" + current_version)

            if current_version and current_bin.exists():
                del sys.argv[0]
                opt = ""
                extra_args = []
                if sys.argv and sys.argv[0] in [
                    "master",
                    "minion",
                    "call",
                    "ssh",
                    "syndic",
                    "cloud",
                    "api",
                    "pip",
                ]:
                    opt = sys.argv.pop(0)
                    if opt != "pip":
                        extra_args = [
                            "-c",
                            str(saltenv_dir / "etc" / "salt"),
                        ]
                cmd = (
                    [
                        str(current_bin),
                        opt,
                    ]
                    + extra_args
                    + sys.argv
                )
                subprocess.call(cmd)
            elif current_version:
                print("ERROR: Version " + current_version + " of Salt is not installed!")
            else:
                print("ERROR: No version of Salt specified!")
        """
    )
    wrapper = wrapper[1:]

    minion = dedent(
        f"""
        root_dir: {hub.OPT.saltenv.saltenv_dir}
        file_client: local
        master_type: disable
        pub_ret: false
        mine_enabled: false
        enable_fqdns_grains: false
        top_file_merging_strategy: same

        file_roots:
          base:
            - ./salt

        pillar_roots:
          base:
            - ./pillar
        """
    )

    async with aiofiles.open(salt_bin, "w") as ofile:
        await ofile.write(wrapper)
    salt_bin.chmod(0o755)

    if not minion_config.exists() or hub.OPT.saltenv.force:
        async with aiofiles.open(minion_config, "w") as cfile:
            await cfile.write(minion)

    print(
        "Add the saltenv bin directory to your PATH:\n\n"
        f"    echo 'export PATH=\"{salt_bin.parent}:$PATH\"' >> ~/.bashrc\n"
        "OR:\n"
        f"    echo 'export PATH=\"{salt_bin.parent}:$PATH\"' >> ~/.zshrc\n"
    )
