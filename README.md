# katcrawl
A command line interface to Kickass Torrents.

A major rework of [Katastrophe](https://github.com/alyakhtar/Katastrophe).

### Dependencies

* [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
* [docopt](https://github.com/docopt/docopt)
* [requests](https://pypi.python.org/pypi/requests)
* [psutil](https://pypi.python.org/pypi/psutil/4.3.0)
* [kickass](https://github.com/Reuben-Thorpe/kickass)

### Requires
* Python 3
* Linux/Mac/Windows
  - A torrent client that can handle magnet links.

### Usage:
```katcrawl

katcrawl provides a command line interface to Kickass Torrents.

Usage:
  katcrawl <search>
  katcrawl ( -m | -t | -a | -s | -g | -p | -b | -x | -z <category> )
  katcrawl ( -M | -T | -A | -S | -G | -P | -B | -X | -Z <category> ) <search>
  katcrawl -h | --help
  katcrawl --version

Options:
  <search>                 Search string
  <category>               Custom category
  -h, --help               Display this screen.
  --version                Display version.
  -m, --topmovies          List top Movie torrents
  -t, --toptv              List top TV torrents
  -a, --topanime           List top Anime torrents
  -s, --topmusic           List top Music torrents
  -g, --topgames           List top Game torrents
  -p, --topapplications    List top Application torrents
  -b, --topbooks           List top Book torrents
  -x, --topxxx             List top XXX torrents
  -z, --topzzz             List top custom category
  -M, --movies             Search by Movie category
  -T, --tv                 Search by TV category
  -A, --anime              Search by Anime category
  -S, --music              Search by Music category
  -G, --games              Search by Games category
  -P, --applications       Search by Applications category
  -B, --books              Search by Book category
  -X, --xxx                Search by XXX category
  -Z, --zzz                Search by custom category
```

### Todo
* ~~See if there is a way to check if Bittorrent client is installed on Windows (ie: doesn't have to be running).~~
  * Now opens the torrent magnet link with the default handler on Windows.
* ~~Add the ability to specify other categories.~~
  * Done (version 2.0).
* ~~Migrate to [Reuben-Thorpe's](https://github.com/Reuben-Thorpe) API.~~
  * Done (version 2.0).
* Add ability to sort results ~~(probably after migration to API)~~.
* Show a more human readable torrent date. Maybe age?

### Thanks
A big thanks to [Aly Akhtar](https://github.com/alyakhtar) for Katastrophe and the motivation to learn Python.

### License

MIT © [Kevin Grant](https://github.com/wedwabbit/katcrawl/blob/master/LICENSE.html)
