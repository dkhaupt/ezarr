import os
import subprocess


class UserGroupSetup:
    def __init__(self, media_dir='/', config_dir='/'):
        self.media_dir = media_dir
        self.config_dir = config_dir
        self._run(['sudo', 'groupadd', 'mediacenter', '-g', '13000'])

    def _run(self, args):
        subprocess.run(args, check=True)

    def _owner(self):
        return str(os.getuid()) + ':mediacenter'

    def _data_subdirs(self):
        return [self.media_dir + '/data/' + sub for sub in ('media', 'usenet', 'torrents')]

    def create_config_dir(self, service_name):
        config_path = self.config_dir + '/' + service_name + '-config'
        self._run(['sudo', 'mkdir', '-p', config_path])
        self._run(['sudo', 'chown', '-R', service_name + ':mediacenter', config_path])
        self._run(['sudo', 'chown', self._owner(), self.config_dir])

    def _servarr(self, username, uid, subfolder):
        self._run(['sudo', 'useradd', username, '-u', uid])
        for path in self._data_subdirs():
            self._run(['sudo', 'mkdir', '-pv', path + '/' + subfolder, '-m', '775'])
        for path in self._data_subdirs():
            self._run(['sudo', 'chown', '-R', username + ':mediacenter', path + '/' + subfolder])
        self._run(['sudo', 'chown', self._owner(), self.media_dir + '/data'])
        for path in self._data_subdirs():
            self._run(['sudo', 'chown', self._owner(), path])
        self.create_config_dir(username)
        self._run(['sudo', 'usermod', '-a', '-G', 'mediacenter', username])

    def sonarr(self):
        self._servarr('sonarr', '13001', 'tv')

    def radarr(self):
        self._servarr('radarr', '13002', 'movies')

    def lidarr(self):
        self._servarr('lidarr', '13003', 'music')

    def mylar3(self):
        self._servarr('mylar', '13005', 'comics')

    def audiobookshelf(self):
        self._servarr('audiobookshelf', '13013', 'audiobooks')

    def prowlarr(self):
        self._run(['sudo', 'useradd', 'prowlarr', '-u', '13006'])
        self.create_config_dir('prowlarr')
        self._run(['sudo', 'usermod', '-a', '-G', 'mediacenter', 'prowlarr'])

    def qbittorrent(self):
        self._run(['sudo', 'useradd', 'qbittorrent', '-u', '13007'])
        self._run(['sudo', 'usermod', '-a', '-G', 'mediacenter', 'qbittorrent'])

    def overseerr(self):
        self._run(['sudo', 'useradd', 'overseerr', '-u', '13009'])
        self.create_config_dir('overseerr')
        self._run(['sudo', 'usermod', '-a', '-G', 'mediacenter', 'overseerr'])

    def plex(self):
        self._run(['sudo', 'useradd', 'plex', '-u', '13010'])
        self.create_config_dir('plex')
        self._run(['sudo', 'usermod', '-a', '-G', 'mediacenter', 'plex'])

    def sabnzbd(self):
        self._run(['sudo', 'useradd', 'sabnzbd', '-u', '13011'])
        self.create_config_dir('sabnzbd')
        self._run(['sudo', 'usermod', '-a', '-G', 'mediacenter', 'sabnzbd'])

    def jellyseerr(self):
        self._run(['sudo', 'useradd', 'jellyseerr', '-u', '13012'])
        self.create_config_dir('jellyseerr')
        self._run(['sudo', 'usermod', '-a', '-G', 'mediacenter', 'jellyseerr'])
