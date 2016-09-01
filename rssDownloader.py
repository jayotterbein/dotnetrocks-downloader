import feedparser;
from datetime import datetime, timedelta, timezone;
from time import mktime;
from os import path, makedirs, listdir, utime;
from urllib.request import urlretrieve;
from urllib.parse import urlparse;

# .NET Rocks publishes at midnight eastern time

url = 'http://www.pwop.com/feed.aspx?show=dotnetrocks&filetype=master'
outputDir = '/Media/DotNetRocks'

if not path.exists(outputDir):
    makedirs(outputDir)

files = [f for f in listdir(outputDir) if path.isfile(path.join(outputDir, f))]

oldestDesired = datetime.now() - timedelta(days=30)
parsedFeed = feedparser.parse(url)
for item in parsedFeed.entries:    
    published = datetime.fromtimestamp(mktime(item.published_parsed))
    if published >= oldestDesired:
        for e in item.enclosures:
            filename = path.basename(urlparse(e.url).path)
            fullpath = path.join(outputDir, filename)
            if filename not in files:
                print('Downloading ' + filename)
                urlretrieve(e.url, fullpath)
            publishedTs = published.replace(tzinfo=timezone.utc).timestamp()
            utime(fullpath, (publishedTs, publishedTs))
