"""katcrawl

katcrawl provides a command line interface to Kickass Torrents.

Usage:
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
"""


import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from sys import platform
import subprocess
import os
from docopt import docopt
from sys import platform


def download_torrent(link, name):

    file_name = "".join(name.split()) # Remove whitespace from name to serve as filename.
    source_code = requests.get(link)
    plain_text = source_code.text.encode('utf-8')
    soup = BeautifulSoup(plain_text, "lxml")

    magnet = soup.find('a', {'title': 'Magnet link'}) # Extract the magnet link.
    magnet_link = magnet.get('href')

    if platform == "linux" or platform == "linux2":
        subprocess.Popen(['xdg-open', magnet_link],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    elif platform == "darwin":
	            os.system('open '+magnet_link)

    elif platform == "win32":
        procs = []
        flag = 0
        client = ''
        cmd = 'WMIC PROCESS get Caption'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            procs.append(line.strip())

        clients = ['BitTorrent.exe',
                   'uTorrent.exe',
                   'deluge.exe',
                   'qbittorrent.exe']

        for c in clients:
            if c in procs:
                client = c
                break

        if client:
            cmd = 'wmic process where "name=\'{}\'" get ExecutablePath'.format(client)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            loc = proc.stdout.readlines()
            exe = loc[1].strip()
            subprocess.Popen([exe.decode(), magnet_link])
        else:
            print("Compatible torrent client not installed or running.")
            return
        
    print('Downloaded: '+name); # Let the user know which torrent was downloaded.


def check_kats():
    # Check kastatus.com an available mirror.
    kastatus='https://kastatus.com'

    kastatus_source = requests.get(kastatus)
    plain_text = kastatus_source.text.encode('utf-8')
    soup = BeautifulSoup(plain_text, "lxml")
    
    print('Finding an available mirror...') 
    for i in soup.findAll('a', {'class': 'domainLink'}): # Loop through mirrors checking availability. Return first available.
        url = i.get('href')
        print('Testing '+url+'...')
        try:
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                print('Success!')
                return url+'/'
            else:
                raise Exception()
        except:
            print('Failed!')

    print('No mirrors available')
    return False
 

def fetch_list(media_type, page, link, query=None): # Fetch page number <page> of media type <media_type> from <link> matching <query> (if provided).
    torrent_name = []
    torrent_size = []
    torrent_seeds = []
    torrent_leechers = []
    torrent_hrefs = []
    torrent_age = []
    count = 0

    if query != None: # Add the query string to the link.
        link += 'usearch/'
        words=query.split()
        for idx,val in enumerate(words):
            if idx == 0:
                link += val
            else:
                link += '%20' + val
        if media_type != '':
            link += '%20category%3A'+media_type
    else:
        link += media_type

    if page > 1:
        link += '/'+str(page)

    source_code = requests.get(link)
    plain_text = source_code.text.encode('utf-8')
    soup = BeautifulSoup(plain_text, "lxml")

    for i in soup.findAll('table', {'class': 'data'}):
        for j in i('a', {'class': 'cellMainLink'}):
            torrent_name.append(''.join(c for c in j.get_text() if 0 < ord(c) < 127)[:64]) # Add the torrent name removing non-ascii characters - max 64 chars.
            torrent_hrefs.append(j.get('href'))
            count += 1

        for j in i('td', {'class': 'nobr center'}): # All <td> tags with class = "nobr center".
            torrent_size.append(j.get_text())

        for j in i('td', {'class': 'center', 'title': True}): # All <td> tags with class = "center" and a title.
            torrent_age.append(j.get_text())

        for j in i('td', {'class': 'green center'}): # All <td> tags with class = "green center".
            torrent_seeds.append(j.get_text())

        for j in i('td', {'class': 'red lasttd center'}): # All <td> tags with class = "red lasttd center".
            torrent_leechers.append(j.get_text())

    return (count,
            list(zip(range(count), torrent_name, torrent_size, torrent_age, torrent_seeds, torrent_leechers)),
            torrent_hrefs)


def list_torrents(media_type, query=None):

    headers = ['No.', 'Name', 'Size', 'Age', 'Seeds', 'Leechers'] # Set up column headings for the printed list of torrents.
    page = 1 # Start at page 1. Page 0 indicates exit.

    # Check for an avilable mirror.
    try:
        link = check_kats()
    except:
        page = 0 # No mirrors available so exit.

    while page > 0:
        count, torrent_list, torrent_hrefs = fetch_list(media_type, page, link, query) # Get the list of torrents.
        # Print the list.
        print('\nTop '+media_type.upper()+' torrents - Page '+str(page)+'\n')
        print(tabulate(torrent_list, headers, tablefmt='psql', numalign="center"))
      
        if page > 1:
            req_torrents = input('Enter torrent numbers to download, "e" to exit, "n" for next page, or "p" for previous page: ')
        else:
            req_torrents = input('Enter torrent numbers to download, "e" to exit, or "n" for next page: ')

        if 'e' in req_torrents.lower(): # Exit.
            page = 0
        elif 'n' in req_torrents.lower(): # Next page.
            page += 1
        elif 'p' in req_torrents.lower(): # Previous page.
            page = max(1, page - 1)
        else: # Download torrents
            page = 0 # Exit after the torrents have been downloaded.
            if ',' in req_torrents:
                for x in req_torrents.split(','):
                    try: 
                        i = int(x)
                    except:
                        print(x+" is an invalid torrent number - ignored\n")
                        continue
                    if i >= 0 and i < count:
                        download_torrent('https://kat.cr' + torrent_hrefs[i],torrent_list[i][1])
                    else:
                        print(x+" is an invalid torrent number - ignored\n")
            else:
                try:
                    i = int(req_torrents)
                except:
                    print(req_torrents+" is an invalid torrent - ignored!\n")
                    continue
                if i >= 0 and i < count:
                    download_torrent('https://kat.cr' + torrent_hrefs[i],torrent_list[i][1])
                else:
                    print(req_torrents+" is an invalid torrent - ignored!\n")


def main():
    args = docopt(__doc__, version='katcrawl 1.0')

    media_type = '' # Set a default empty category.

    if args["--movies"] or args['--topmovies']:
        media_type='movies'
    elif args["--tv"] or args["--toptv"]:
        media_type='tv'
    elif args["--anime"] or args["--topanime"]:
        media_type='anime'
    elif args["--music"] or args["--topmusic"]:
        media_type='music'
    elif args["--lossless"] or args['--toplossless']:
        media_type='lossless'
    elif args["--books"] or args["--topbooks"]:
        media_type='books'
    elif args["--games"] or args['--topgames']:
        media_type='games'
    elif args["--applications"] or args["--topapplications"]:
        media_type='applications'
    elif args["--xxx"] or args["--topxxx"]:
        media_type='xxx'
    
    list_torrents(media_type, args['<search>'])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except ValueError:
        sys.exit()
