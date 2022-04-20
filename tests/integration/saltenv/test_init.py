from io import StringIO
from unittest import mock

import pop.hub
import pytest


@mock.patch("sys.stderr", new_callable=StringIO)
def test_cli_with_no_arguments(mock_stderr):
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="saltenv")
    hub.pop.loop.create()
    with pytest.raises(SystemExit) as ex_:
        hub.pop.Loop.run_until_complete(hub.saltenv.init.cli())
    assert "error: argument _subparser_: invalid choice:" in mock_stderr.getvalue()
