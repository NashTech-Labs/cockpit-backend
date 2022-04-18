
def get_ssh_connection(connections_details):
    """return ssh connection payload"""
    try:
        SSH_CONNECTION={
                "parentIdentifier": "ROOT",
                "name": "{}".format(connections_details["name"]),
                "protocol": "ssh",
                "parameters": {
                    "port": "{}".format(connections_details["port"]),
                    "read-only": "",
                    "swap-red-blue": "",
                    "cursor": "",
                    "color-depth": "",
                    "clipboard-encoding": "",
                    "disable-copy": "",
                    "disable-paste": "",
                    "dest-port": "",
                    "recording-exclude-output": "",
                    "recording-exclude-mouse": "",
                    "recording-include-keys": "",
                    "create-recording-path": "",
                    "enable-sftp": "",
                    "sftp-port": "",
                    "sftp-server-alive-interval": "",
                    "enable-audio": "",
                    "color-scheme": "",
                    "font-size": "",
                    "scrollback": "",
                    "timezone": None,
                    "server-alive-interval": "",
                    "backspace": "",
                    "terminal-type": "",
                    "create-typescript-path": "",
                    "hostname": "{}".format(connections_details['hostname']),
                    "host-key": "",
                    "private-key": "{}".format(connections_details['private-key']),
                    "username": "{}".format(connections_details['username']),
                    "password": "{}".format(connections_details['password']),
                    "passphrase": "",
                    "font-name": "",
                    "command": "",
                    "locale": "",
                    "typescript-path": "",
                    "typescript-name": "",
                    "recording-path": "",
                    "recording-name": "",
                    "sftp-root-directory": ""
                },
                "attributes": {
                    "max-connections": "100",
                    "max-connections-per-user": "100",
                    "weight": "",
                    "failover-only": "",
                    "guacd-port": "",
                    "guacd-encryption": "",
                    "guacd-hostname": ""
                }
        }
        return SSH_CONNECTION
    except Exception as e:
        print("Error in SSH connection config \nError:{}".format(e))
        return None