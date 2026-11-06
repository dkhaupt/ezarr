class ContainerConfig:
    def __init__(self,
                 media_dir,
                 config_dir,
                 timezone,
                 plex_claim='',
                 ):
        self.media_dir = media_dir
        self.config_dir = config_dir
        self.timezone = timezone
        self.plex_claim = plex_claim

        self.movie_dir = media_dir + '/media/movies'
        self.tv_dir = media_dir + '/media/tv'
        self.music_dir = media_dir + '/media/music'
        self.book_dir = media_dir + '/media/books'
        self.comic_dir = media_dir + '/media/comics'
        self.torrent_dir = media_dir + '/data/torrents'
        self.usenet_dir = media_dir + '/data/usenet'

    def plex(self):
        return (
            '  plex:\n'
            '    image: lscr.io/linuxserver/plex@sha256:7f9a1d574958fc2f177c14ca190d4b811a58c274477f5bae8fb44ee676fb96bf\n'
            '    container_name: plex\n'
            '    network_mode: host\n'
            '    environment:\n'
            '      - PUID=13010\n'
            '      - PGID=13000\n'
            '      - VERSION=docker\n'
            '      - PLEX_CLAIM=' + self.plex_claim + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/plex-config:/config\n'
            '      - ' + self.media_dir + '/data/media:/media\n'
            '    restart: unless-stopped\n\n'
        )

    def tautulli(self):
        return (
            '  tautulli:\n'
            '    image: lscr.io/linuxserver/tautulli@sha256:13f03ecfc61a7af89d492677389771ac29682a72153ce08a5cd4faffbc0197e8\n'
            '    container_name: tautulli\n'
            '    depends_on:\n'
            '      - plex\n'
            '    environment:\n'
            '      - PUID=${UID}\n'
            '      - PGID=13000\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/tautulli-config:/config\n'
            '    ports:\n'
            '      - "8181:8181"\n'
            '    restart: unless-stopped\n\n'
        )

    def jellyfin(self):
        return (
            '  jellyfin:\n'
            '    image: lscr.io/linuxserver/jellyfin:latest\n'
            '    container_name: jellyfin\n'
            '    environment:\n'
            '      - PUID=${UID}\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/jellyfin-config:/config\n'
            '      - ' + self.media_dir + '/data/media:/data\n'
            '    ports:\n'
            '      - "8096:8096"\n'
            '    restart: unless-stopped\n\n'
        )

    def sonarr(self):
        return (
            '  sonarr:\n'
            '    image: lscr.io/linuxserver/sonarr@sha256:c19aa4ecdf03d73e1d5c901da33744cb7eb4d921f89bafed1ca264601d7fa224\n'
            '    container_name: sonarr\n'
            '    environment:\n'
            '      - PUID=13001\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/sonarr-config:/config\n'
            '      - ' + self.media_dir + '/data:/data\n'
            '    ports:\n'
            '      - "8989:8989"\n'
            '    restart: unless-stopped\n\n'
        )

    def radarr(self):
        return (
            '  radarr:\n'
            '    image: lscr.io/linuxserver/radarr@sha256:119aaa4a4f7349bcd2a136c5373a0d7925b5479915c7dfe0c0ad352db2a6d438\n'
            '    container_name: radarr\n'
            '    environment:\n'
            '      - PUID=13002\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/radarr-config:/config\n'
            '      - ' + self.media_dir + '/data:/data\n'
            '    ports:\n'
            '      - "7878:7878"\n'
            '    restart: unless-stopped\n\n'
        )

    def lidarr(self):
        return (
            '  lidarr:\n'
            '    image: lscr.io/linuxserver/lidarr@sha256:c74c32408fdf6e7926ad62641fc1a5544206ee65c33f2188bb179edb30e28f5a\n'
            '    container_name: lidarr\n'
            '    environment:\n'
            '      - PUID=13003\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/lidarr-config:/config\n'
            '      - ' + self.media_dir + '/data:/data\n'
            '    ports:\n'
            '      - "8686:8686"\n'
            '    restart: unless-stopped\n\n'
        )

    def mylar3(self):
        return (
            '  mylar3:\n'
            '    image: lscr.io/linuxserver/mylar3:latest\n'
            '    container_name: mylar3\n'
            '    environment:\n'
            '      - PUID=13005\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/mylar-config:/config\n'
            '      - ' + self.media_dir + '/data:/data\n'
            '    ports:\n'
            '      - "8090:8090"\n'
            '    restart: unless-stopped\n\n'
        )

    def audiobookshelf(self):
        return (
            '  audiobookshelf:\n'
            '    image: ghcr.io/advplyr/audiobookshelf:latest\n'
            '    container_name: audiobookshelf\n'
            '    environment:\n'
            '      - AUDIOBOOKSHELF_UID=13013\n'
            '      - AUDIOBOOKSHELF_GID=13000\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/audiobookshelf-config:/config\n'
            '      - ' + self.media_dir + '/data/audiobooks:/audiobooks\n'
            '      - ' + self.media_dir + '/data/podcasts:/podcasts\n'
            '      - ' + self.media_dir + '/data/metadata:/metadata\n'
            '    ports:\n'
            '      - "13378:80"\n'
            '    restart: unless-stopped\n\n'
        )

    def prowlarr(self):
        return (
            '  prowlarr:\n'
            '    image: lscr.io/linuxserver/prowlarr@sha256:363769676eb4a58dc5f691fb95ff65b3ed6918654b90c15c676c988aa2921048\n'
            '    container_name: prowlarr\n'
            '    environment:\n'
            '      - PUID=13006\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/prowlarr-config:/config\n'
            '    ports:\n'
            '      - "9696:9696"\n'
            '    restart: unless-stopped\n\n'
        )

    def qbittorrent(self):
        return (
            '  qbittorrent:\n'
            '    image: lscr.io/linuxserver/qbittorrent@sha256:a00b6a597a3832a1814cde0ef60abc55c94644f3f80902c3432f6af6de8d4a96\n'
            '    container_name: qbittorrent\n'
            '    environment:\n'
            '      - PUID=13007\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '      - WEBUI_PORT=8080\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/qbittorrent-config:/config\n'
            '      - ' + self.torrent_dir + ':/data/torrents\n'
            '    network_mode: "service:gluetun"\n'
            '    restart: unless-stopped\n\n'
        )

    def overseerr(self):
        return (
            '  overseerr:\n'
            '    image: sctx/overseerr@sha256:6197516c9d7b58ccf113455e32aafb94df5d91995fe50e8c2cae6ba6c7c7b7de\n'
            '    container_name: overseerr\n'
            '    environment:\n'
            '      - PUID=13009\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/overseerr-config:/app/config\n'
            '    ports:\n'
            '      - "5055:5055"\n'
            '    restart: unless-stopped\n\n'
        )

    def jellyseerr(self):
        return (
            '  jellyseerr:\n'
            '    image: fallenbagel/jellyseerr:latest\n'
            '    container_name: jellyseerr\n'
            '    environment:\n'
            '      - PUID=13012\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/jellyseerr-config:/app/config\n'
            '    ports:\n'
            '      - "5056:5055"\n'
            '    restart: unless-stopped\n\n'
        )

    def sabnzbd(self):
        return (
            '  sabnzbd:\n'
            '    image: lscr.io/linuxserver/sabnzbd@sha256:13d4404f1242f819e0cc2e294def5858def251a3609eb59404dad303075a564a\n'
            '    container_name: sabnzbd\n'
            '    environment:\n'
            '      - PUID=13011\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '      - HAS_IPV6=false\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/sabnzbd-config:/config\n'
            '      - ' + self.usenet_dir + ':/downloads\n'
            '    network_mode: "service:gluetun"\n'
            '    restart: unless-stopped\n\n'
        )
