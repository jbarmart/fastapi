from dynaconf import Dynaconf




settings = Dynaconf(
     settings_file="app/settings.toml",
    environments=True,
    #default_env="testing",
    env="development",
    fresh_vars=['VALUE'],
 )

# https://www.dynaconf.com/configuration/#default_ensv