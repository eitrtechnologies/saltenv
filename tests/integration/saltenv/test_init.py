from unittest import mock


def test_cli(hub):
    with mock.patch("sys.argv", ["saltenv"]):
        hub.saltenv.init.cli()
