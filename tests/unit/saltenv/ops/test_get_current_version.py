import mock
from pathlib import Path, PosixPath
import os


"""
async def get_current_version(hub, **kwargs):
    '''
    Read the current active version from ./.salt-version and the main version
    file at ${SALTENV_DIR}/version. The former overrides the latter.
    '''
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
"""


async def test_get_current_version1(mock_hub, hub):
    """
    SCENARIO #1
    - override_version_file DOES NOT EXIST
    - main_version_file DOES NOT EXIST
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.get_current_version = hub.saltenv.ops.get_current_version

    # Set the saltenv_dir as a nonexistent directory
    mock_hub.OPT.saltenv.saltenv_dir = "nonexistent_testing_dir"

    # Patch os.getcwd() to be a nonexistent directory
    with mock.patch("os.getcwd") as mocked_override_file:
        mocked_override_file.return_value = Path("nonexistent_testing_dir") / ".salt-version"
        expected = ("", "")
        actual = await mock_hub.saltenv.ops.get_current_version()
        actual == expected


async def test_get_current_version2(mock_hub, hub, tmp_path):
    """
    SCENARIO #2
    - override_version_file DOES
    - main_version_file DOES NOT EXIST
    """
    pass


async def test_get_current_version3(mock_hub, hub, tmp_path):
    """
    SCENARIO #3
    - override_version_file DOES NOT EXIST
    - main_version_file DOES EXIST
    """
    pass


async def test_get_current_version4(mock_hub, hub, tmp_path):
    """
    SCENARIO #4
    - override_version_file DOES EXIST
    - main_version_file DOES EXIST
    """
    pass
