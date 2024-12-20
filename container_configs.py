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
            '    image: lscr.io/linuxserver/plex:latest\n'
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
            '    image: lscr.io/linuxserver/tautulli:latest\n'
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
            '    image: lscr.io/linuxserver/sonarr:latest\n'
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
            '    image: lscr.io/linuxserver/radarr:latest\n'
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
            '    image: lscr.io/linuxserver/lidarr:latest\n'
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

    def readarr(self):
        return (
            '  readarr:\n'
            '    image: lscr.io/linuxserver/readarr:develop\n'
            '    container_name: readarr\n'
            '    environment:\n'
            '      - PUID=13004\n'
            '      - PGID=13000\n'
            '      - UMASK=002\n'
            '      - TZ=' + self.timezone + '\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/readarr-config:/config\n'
            '      - ' + self.media_dir + '/data:/data\n'
            '    ports:\n'
            '      - "8787:8787"\n'
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
            '      - AUDIOBOOKSHELF_UID=13009\n'
            '      - AUDIOBOOKSHELF_GID=13000\n'
            '    volumes:\n'
            '      - ' + self.config_dir + '/audiobookshelf:/config\n'
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
            '    image: lscr.io/linuxserver/prowlarr:develop\n'
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
            '    image: lscr.io/linuxserver/qbittorrent:latest\n'
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
            '    ports:\n'
            '      - "8080:8080" # qbittorrent\n'
            '      - "6881:6881" # qbittorrent\n'
            '      - "6881:6881/udp" # qbittorrent\n'
            '      - "8484:8484" # sabnzbd\n'
            '    network_mode:"service:gluetun"'
            '    restart: unless-stopped\n\n'
        )

    def overseerr(self):
        return (
            '  overseerr:\n'
            '    image: sctx/overseerr:latest\n'
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
            '    image: lscr.io/linuxserver/sabnzbd:latest\n'
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
