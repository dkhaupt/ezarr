### These steps describe the necessary configuration to get the ezarr stack running after cloning the repo.

1. Add a file named `.env` at the root of this repo
1. In `.env`, specify `WIREGUARD_PRIVATE_KEY` and `WIREGUARD_ADDRESSES` and set values according to the instructions [here](https://github.com/qdm12/gluetun-wiki/blob/main/setup/providers/mullvad.md#wireguard-only).
   - This assumes the VPN provider of choice is Mullvad. If not, `docker-compose.yml` will need to be edited.
1. Follow the steps in "Important notes" in `README.md`
   - Use container names when connecting services to each other, rather than IP + port
   - When connecting services to qbittorrent, use `gluetun` since that's what the qbittorrent container is using for networking
1. `qbittorrent` setup
   - Add the following in "Run external program on torrent completion": `chmod -R 775 "%F"`
   - Default save path: `/data/torrents`
   - Set torrents to automatic management
   - Add the correct download path to each Category, i.e. `tv-sonarr` should be set to `/data/torrents/tv`
   - Set network interface to `tun0`


### Optional configuration

1. Set indexer priorities in the Sonarr and Radarr settings to ensure larger trackers are prioritized

