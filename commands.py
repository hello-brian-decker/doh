
# Paths
meta_dir = "/usr/local/etc/meta.json"

# Commands
application_list = "apt list | awk -F/ '{print $1}'"
application_versions = "awk -F\"[{}]\" '/Test Machine/{print $2}'"
users = "cat /etc/passwd | awk - F: '{ print $1}'"


# Ignored Lists
ignored_users = ['root', 'daemon', 'bin', 'sys', 'sync', 'games', 'man',
                 'lp', 'mail', 'news', 'uucp', 'proxy', 'www-data',
                 'backup', 'list', 'irc', 'gnats', 'nobody', '_apt']
ignored_applications = []

# Error Messages
docker_not_running = "Docker Engine Not Running"
