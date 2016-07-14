# katcrawl
A command line interface to Kickass Torrents.

A major rework of [Katastrophe](https://github.com/alyakhtar/Katastrophe).

### Dependencies

* [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
* [tabulate](https://pypi.python.org/pypi/tabulate)
* [docopt](https://github.com/docopt/docopt)
* [requests](https://pypi.python.org/pypi/requests)

### Requires
* Python 3
* Linux/Mac
  - A torrent client that can handle magnet links.
* Windows
  - One of [BitTorrent](http://www.bittorrent.com)/[μTorrent](http://utorrent.com)/[Deluge](http://deluge-torrent.org)/[qBittorrent](http://www.qbittorrent.org)

### Usage:
```sh
  katcrawl <search>
  katcrawl ( -m | -t | -a | -s | -l | -g | -p | -b | -x )
  katcrawl ( -M | -T | -A | -S | -L | -G | -P | -B | -X ) <search>
  katcrawl -h | --help
  katcrawl --version  

Options:
  <search>                 Search string
  -h, --help               Display this screen.
  --version                Display version.
  -m, --topmovies          List top Movie torrents
  -t, --toptv              List top TV torrents
  -a, --topanime           List top Anime torrents
  -s, --topmusic           List top Music torrents
  -l, --toplossless        List top Lossless Music torrents
  -g, --topgames           List top Game torrents
  -p, --topapplications    List top Application torrents
  -b, --topbooks           List top Book torrents
  -x, --topxxx             List top XXX torrents
  -M, --movies             Search by Movie category
  -T, --tv                 Search by TV category
  -A, --anime              Search by Anime category
  -S, --music              Search by Music category
  -L, --lossless           Search by Lossless Music category
  -G, --games              Search by Games category
  -P, --applications       Search by Applications category
  -B, --books              Search by Book category
  -X, --xxx                Search by XXX category
```
### Todo
* See if there is a way to check if Bittorrent client is installed on Windows (ie: doesn't have to be running).
* Add the ability to specify other categories.
* Migrate to [Reuben-Thorpe's](https://github.com/Reuben-Thorpe) API.

### Thanks
A big thanks to [Aly Akhtar](https://github.com/alyakhtar) for Katastrophe and the motivation to learn Python.

### License

MIT © [Kevin Grant](https://github.com/wedwabbit/katcrawl/blob/master/LICENSE.html)
