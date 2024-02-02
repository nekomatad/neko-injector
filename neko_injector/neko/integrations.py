from neko_configparser import ConfigParserInterface


neko_config = ConfigParserInterface.parse_config()


__all__ = ['ConfigParserInterface', 'neko_config']
