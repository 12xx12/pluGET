class Plugin:
    """
    Create plugin class to store installed plugins inside it
    """

    def __init__(
            self,
            plugin_file_name: str,
            plugin_name: str,
            plugin_file_version: str,
            plugin_latest_version: str,
            plugin_is_outdated: bool,
            plugin_repository: str,
            plugin_repository_data: list
    ) -> None:
        self.plugin_file_name = plugin_file_name
        self.plugin_name = plugin_name
        self.plugin_file_version = plugin_file_version
        self.plugin_latest_version = plugin_latest_version
        self.plugin_is_outdated = plugin_is_outdated
        self.plugin_repository = plugin_repository
        self.plugin_repository_data = plugin_repository_data

    @staticmethod
    def create_plugin_list() -> list:
        """
        Creates a global array list to store plugins
        """
        global INSTALLEDPLUGINLIST
        INSTALLEDPLUGINLIST = []
        return INSTALLEDPLUGINLIST

    @staticmethod
    def add_to_plugin_list(
            plugin_file_name: str,
            plugin_name: str,
            plugin_file_version: str,
            plugin_latest_version: str,
            plugin_is_outdated: bool,
            plugin_repository: str,
            plugin_repository_data: list
    ) -> None:
        """
        Adds a plugin to global installed plugin lists
        """
        INSTALLEDPLUGINLIST.append(Plugin(
            plugin_file_name,
            plugin_name,
            plugin_file_version,
            plugin_latest_version,
            plugin_is_outdated,
            plugin_repository,
            plugin_repository_data
        ))
        return None
