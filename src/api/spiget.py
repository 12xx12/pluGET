import re

from src.plugin.plugin import Plugin
from src.plugin.plugin_updatechecker import egg_cracking_jar, get_latest_plugin_version_spiget, compare_plugin_version
from src.utils.console_output import rich_print_error
from src.utils.utilities import api_do_request


def search_plugin_spiget(plugin_file: str, plugin_file_name: str, plugin_file_version: str) -> int:
    """
    Search the spiget api for the installed plugin and add it to the installed plugin list

    :param plugin_file: Full file name of plugin
    :param plugin_file_name: Name of plugin file
    :param plugin_file_version: Version of plugin file

    :returns: Plugin ID of Spigot Plugin
    """
    url = f"https://api.spiget.org/v2/search/resources/{plugin_file_name}?field=name&sort=-downloads"
    plugin_list = api_do_request(url)

    # Handle failed api request
    """
    {'error': 'Unexpected Exception', 'msg': 'Unexpected Exception. Please report this to 
    https://github.com/SpiGetOrg/api.spiget.org/issues'}
    """
    if "error" in plugin_list:
        rich_print_error(
            f"[not bold]Error: Spiget error occurred whilst searching for plugin '{plugin_file}': {plugin_list['msg']}"
        )
        return plugin_list['msg']
    else:
        plugin_file_version2 = plugin_file_version
        for i in range(4):
            if i == 1:
                plugin_file_version2 = re.sub(r'(\-\w*)', '', plugin_file_version)
            if i == 2:
                plugin_name_in_yml, plugin_version_in_yml = egg_cracking_jar(plugin_file)
                url = f"https://api.spiget.org/v2/search/resources/{plugin_name_in_yml}?field=name&sort=-downloads"
                try:
                    plugin_list = api_do_request(url)
                except ValueError:
                    continue
                # if no plugin name was found with egg_cracking_jar() skip this round
                if plugin_list is None:
                    continue

            # search with version which is in plugin.yml for the plugin
            if i == 3:
                plugin_file_version2 = plugin_version_in_yml

            for plugin in plugin_list:
                plugin_id = plugin["id"]
                url2 = f"https://api.spiget.org/v2/resources/{plugin_id}/versions?size=100&sort=-name"
                try:
                    plugin_versions = api_do_request(url2)
                except ValueError:
                    continue
                if plugin_versions is None:
                    continue
                for updates in plugin_versions:
                    update_version_name = updates["name"]
                    if plugin_file_version2 in update_version_name:
                        # spigot_update_id = updates["id"]
                        plugin_latest_version = get_latest_plugin_version_spiget(plugin_id)
                        plugin_is_outdated = compare_plugin_version(plugin_latest_version, update_version_name)
                        Plugin.add_to_plugin_list(
                            plugin_file,
                            plugin_file_name,
                            plugin_file_version,
                            plugin_latest_version,
                            plugin_is_outdated,
                            "spigot",
                            [plugin_id]
                        )
                        return plugin_id
        return None
