def test_cli(mock_hub, hub):
    mock_hub.saltenv.init.cli = hub.saltenv.init.cli
    mock_hub.saltenv.init.cli()
    mock_hub.pop.config.load.assert_called_once_with(["saltenv"], "saltenv")
