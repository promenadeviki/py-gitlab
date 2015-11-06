import json
import os


class ConfigParser(object):
    def read(self, path):
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            raise OSError('{} does not exist'.format(path))
        with open(path, 'rb') as f:
            try:
                self._config = json.loads(f.read())
            except ValueError, e:
                raise e

    def get(self, key):
        try:
            return self._config[key]
        except ValueError, e:
            raise e


config = ConfigParser()
config.read('~/.gitlab')

GITLAB_USERNAME = config.get('username')
GITLAB_PASSWORD = config.get('password')


def get_ldap_username(user):
    """Return the Active Directory username from the GitLab account."""
    try:
        return user['identities'][0]['extern_uid'].split(',')[0][3:]
    except IndexError:
        return None
