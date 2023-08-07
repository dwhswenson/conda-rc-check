#!/usr/bin/env python

import argparse
import requests
import bs4
import dateutil.parser
import datetime
import packaging.version

def parse_file_row(tr):
    tds = tr.find_all('td')
    string_date = tds[4]['title']
    date = dateutil.parser.parse(string_date)
    a = list(tds[3].find_all('a'))[1]
    version = packaging.version.Version(a['href'].split('/')[3])
    conda_tag = tds[6].a.string.strip()
    return version, date, conda_tag

def get_page(package, num):
    req = requests.get(f"https://anaconda.org/{package}/files?page={num}")
    soup = bs4.BeautifulSoup(req.content, features="lxml")
    trs = soup.table.tbody.find_all('tr')
    releases = set(parse_file_row(tr) for tr in trs)
    return releases

def get_releases_since_days_ago(package, oldest_allowed):
    num = 1
    releases = set()
    prev = None
    new = None
    while new is None or prev != new:
        prev = new
        new = get_page(package, num)
        releases.update(new)
        oldest = min(new, key=lambda r: r[1])  # sort by date
        if oldest[1] < oldest_allowed:
            break
        num += 1

    return releases

def find_rcs(releases, oldest_allowed, tags):
    filtered = [r for r in releases if r[1] >= oldest_allowed]
    if tags is not None:
        filtered = [r for r in filtered if r[2] in tags]

    versions = set(r[0] for r in filtered)
    rcs = [v for v in versions if v.pre and 'rc' in v.pre]
    return rcs

def main(package, n_days=7, allowed_tags=None):
    oldest_allowed = datetime.datetime.now() - datetime.timedelta(days=n_days)
    releases = get_releases_since_days_ago(package, oldest_allowed)
    rcs = find_rcs(releases, oldest_allowed, allowed_tags)
    #print(rcs)
    return bool(rcs)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('channel', type=str)
    parser.add_argument('package', type=str)
    parser.add_argument('n_days', type=int)
    parser.add_argument('tags', type=str)
    opts = parser.parse_args()
    package = f"{opts.channel}/{opts.package}"
    tags = opts.tags.split()
    return package, opts.n_days, tags


if __name__ == "__main__":
    package, n_days, tags = parse_args()
    result = main(package, n_days, tags)
    print(f"::set-output name=hasrc::{result}")
