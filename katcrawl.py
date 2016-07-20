"""katcrawl

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
"""

from bs4 import BeautifulSoup
from docopt import docopt
import requests
import psutil
import timeago

from kickass import api
from kickass import CATEGORY, FIELD, ORDER

import sys
import subprocess
import os
from math import log
from datetime import datetime


def pretty_size(n, pow=0, b=1024, u='B', pre=[''] + [p for p in'KMGTPEZY']):
    pow, n = min(int(log(max(n * b**pow, 1), b)), len(pre) - 1), n * b**pow
    return "%%.%if %%s%%s" % abs(pow % (-pow - 1)) % (n / b**float(pow),
                                                      pre[pow], u)


def soupify_source(link):
    """
    Parameters: valid url
    Returns: BeautifulSoup object
    Desc: Connects to a url, downloads the page source, utf-8 encodes it,
          passing it to BeautifulSoup, returning the result.
    """
    print('Connecting to ' + link)
    # Define a user-agent to get past bot checks.
    headers = {'user-agent': 'Mozilla/5.0'}
    try:
        page_source = requests.get(link, headers=headers)  # Get page source.
        print('Success!')
        # UTF-8 encode source and pass to BS.
        return BeautifulSoup(page_source.text.encode('utf-8'), "lxml")
    except ConnectionError:
        print('Erorr connecting to ' + link + '!')
        return None
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise


def download_torrent(link):
    """
    Parameters: a valid url to a web page containing a magnet link.
    Returns: N/A.
    Desc: Extracts the magnet link from the supplie url and then opens
          it using the systems default magnet link handler (usually a
          bittorrent client).
    """
    soup = soupify_source(link)

    # Extract the magnet link.
    magnet = soup.find('a', {'title': 'Magnet link'})
    magnet_link = magnet.get('href')

    # Open the magnet link useing default torrent client.
    if sys.platform == "win32":  # subprocess.call not supported on Win32.
        os.startfile(magnet_link)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, magnet_link])


def check_kats():
    """
    Parameters: N/A.
    Returns: Either an accessable Kickass Torrents mirror or None.
    Desc: Connects to the Kickass Torrents status page, extracts
          available mirrors, and then returns the first that is
          accessable.
    """
    # Check kastatus.com an available mirror.
    kastatus = 'https://kastatus.com'
    soup = soupify_source(kastatus)

    print('Finding an available mirror...')
    # Loop through mirrors checking availability. Return first available.
    for i in soup.findAll('a', {'class': 'domainLink'}):
        url = i.get('href')
        print('Testing ' + url + '...')
        try:
            r = requests.get(url)  # Set a timeout for the mirror.
            if r.status_code == requests.codes.ok:
                print('Success!')
                return url + '/'
            else:
                raise
        except:
            print('Failed!')
            return None
    else:
        print('No mirrors available')
        return None


def list_torrents(media_type, query):
    """
    Parameters: Media type and a query.
    Returns: N/A.
    Desc: Main function that lists torrents matching supplied media type
          and query. User can select from list of torrents, page forward and
          back, or exit.
    """
    torrent_hrefs = []  # List containing urls to torrents.

    # Check for an avilable mirror.
    link = check_kats()
    if not link:
        exit()  # No mirrors available so exit.

    # Generate API object with link returned by check_kats.
    kat = api(link)

    if media_type:
        kat.category(media_type)

    torrent_search = kat.search(query)

    page = 1  # Start at page 1. Page 0 indicates exit.
    while page > 0:

         # Print a heading replacing doubles spaces with single.
        print(' '.join(('Top '
                        + media_type.upper()
                        + ' torrents - Page '
                        + str(page)).split()))
        print('|{0: ^5}|{1: <65}|{2: >9}|{3: ^21}|{4: >10}|{5: >10}|'
              .format('No.', 'Name', 'Size', 'Date', 'Seeds', 'Leechers'))
        print('|{0:-<125}|'.format('-'))

        count = 0
        for torrent in torrent_search.page(page):
            torrent_date = datetime.strptime(torrent["pubDate"],
                                             '%A %d %b %Y %H:%M:%S %z')
            now = datetime.now()
            print('|{0: ^5}|{1: <65}|{2: >9}|{3: ^21}|{4: >10}|{5: >10}|'
                  .format(count, torrent["title"][:60],
                          pretty_size(torrent["size"]),
                          timeago.format(
                              torrent_date.replace(tzinfo=None), now),
                          torrent["seeds"],
                          torrent["leechs"]))
            torrent_hrefs.append(torrent["link"])
            count += 1

        # Footer
        print('|{0:-<125}|'.format('-'))

        if page > 1:
            req_torrents = input('Enter torrent numbers to download, '
                                 '"e" to exit, "n" for next page, or '
                                 '"p" for previous page: ')
        else:
            req_torrents = input('Enter torrent numbers to download, '
                                 '"e" to exit, or "n" for next page: ')

        if 'e' in req_torrents.lower():  # Exit.
            page = 0
        elif 'n' in req_torrents.lower():  # Next page.
            page += 1
        elif 'p' in req_torrents.lower():  # Previous page.
            page = max(1, page - 1)
        else:  # Download torrents
            page = 0  # Exit after the torrents have been downloaded.
            if ',' in req_torrents:
                for x in req_torrents.split(','):
                    try:
                        i = int(x)
                    except:
                        print(x + " is an invalid torrent number - ignored!")
                        continue
                    if i >= 0 and i < count:
                        download_torrent(torrent_hrefs[i])
                    else:
                        print(x + " is an invalid torrent number - ignored!")
            else:
                try:
                    i = int(req_torrents)
                except:
                    print(req_torrents
                          + " is an invalid torrent number - ignored!")
                    continue
                if i >= 0 and i < count:
                    download_torrent(torrent_hrefs[i])
                else:
                    print(req_torrents
                          + " is an invalid torrent number - ignored!")


def main():
    args = docopt(__doc__, version='katcrawl 2.0')

    media_type = None  # Default media type is all (no setting).

    if args["--movies"] or args['--topmovies']:
        media_type = CATEGORY.MOVIES
    elif args["--tv"] or args["--toptv"]:
        media_type = CATEGORY.TV
    elif args["--anime"] or args["--topanime"]:
        media_type = CATEGORY.ANIME
    elif args["--music"] or args["--topmusic"]:
        media_type = CATEGORY.MUSIC
    elif args["--books"] or args["--topbooks"]:
        media_type = CATEGORY.BOOKS
    elif args["--games"] or args['--topgames']:
        media_type = CATEGORY.GAMES
    elif args["--applications"] or args["--topapplications"]:
        media_type = CATEGORY.APPLICATIONS
    elif args["--xxx"] or args["--topxxx"]:
        media_type = CATEGORY.XXX
    elif args["--zzz"] or args["--topzzz"]:
        # User entered custom category.
        media_type = args["<category>"].lower()

    list_torrents(media_type, str(args['<search>'] or ''))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except ValueError:
        sys.exit()
