from pathlib import Path
from unittest.mock import patch


async def test_unit_remove_version_exists(mock_hub, hub, tmp_path):
    """
    SCENARIO #1:
    - The version exists within LOCAL_VERSIONS
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remove_version = hub.saltenv.ops.remove_version

    # Add two versions to LOCAL_VERSIONS
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {
        "3001": Path(tmp_path / "salt-3001"),
        "3004": Path(tmp_path / "salt-3004"),
    }

    with patch("pathlib.PosixPath.unlink", return_value=None) as mock_unlink:
        # Call remove_version with a version that is present in LOCAL_VERSIONS
        ret = await mock_hub.saltenv.ops.remove_version("3004")
        assert ret == True

        # Ensure every mocked function was called the appropriate number of times
        mock_unlink.assert_called_once()


async def test_unit_remove_version_does_not_exist(mock_hub, hub, tmp_path):
    """
    SCENARIO #2:
    - The version does not exist within LOCAL_VERSIONS
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remove_version = hub.saltenv.ops.remove_version

    # Add two versions to LOCAL_VERSIONS
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {
        "3001": Path(tmp_path / "salt-3001"),
        "3004": Path(tmp_path / "salt-3004"),
    }

    with patch("pathlib.PosixPath.unlink", return_value=None) as mock_unlink:
        # Call remove_version with a version that is present in LOCAL_VERSIONS
        ret = await mock_hub.saltenv.ops.remove_version("3003")
        assert ret == True

        # Ensure every mocked function was called the appropriate number of times
        mock_unlink.assert_not_called()


async def test_unit_remove_version_empty_local_versions(mock_hub, hub):
    """
    SCENARIO #3:
    - LOCAL_VERSIONS is empty
    """
    # Link the function to the mock_hub
    mock_hub.saltenv.ops.remove_version = hub.saltenv.ops.remove_version

    # Set LOCAL_VERSIONS to contain no versions
    mock_hub.saltenv.ops.LOCAL_VERSIONS = {}

    with patch("pathlib.PosixPath.unlink", return_value=None) as mock_unlink:
        # Call remove_version with a version that is present in LOCAL_VERSIONS
        ret = await mock_hub.saltenv.ops.remove_version("3003")
        assert ret == True

        # Ensure every mocked function was called the appropriate number of times
        mock_unlink.assert_not_called()
