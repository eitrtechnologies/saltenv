import mock
from pathlib import Path

"""
async def list_(hub, **kwargs):
    '''
    This is the entrypoint for the async code in your project
    '''
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
"""


async def test_list1(mock_hub, hub):
    """
    SCENARIO #1:
    - No local versions
    - No current version
    """
    pass


async def test_list2(mock_hub, hub):
    """
    SCENARIO #2:
    - 2 local versions
    - No current version
    """
    pass


async def test_list3(mock_hub, hub):
    """
    SCENARIO #3:
    - 2 local versions
    - A current version
    """
    pass
