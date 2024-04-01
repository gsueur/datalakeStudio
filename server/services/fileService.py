import requests
import urllib.parse
import os
import re
import mimetypes

def guessFileNameFromURL(url):
    filename = None
    if '.' in url.split('/')[-1]:
        filename = url.split('/')[-1]
    return filename


def downloadFile(url, destination_dir):
    url = urllib.parse.unquote(url)

    r = requests.get(url, allow_redirects=True)
    filename = guessFileNameFromURL(url)
    if r.status_code == 200:
        # let's try to guess the file format
        # when coming as an attachment, the filename is in the Content-Disposition header.
        if r.history:
            filename = guessFileNameFromURL(r.url)
        if not filename and 'Content-Disposition' in r.headers:
            if (d := r.headers['Content-Disposition']) != 'inline':
                names = re.findall("filename=(.+)", d)
                if len(names) == 1:
                    filename = names[0]
                else:
                    filename = 'download'
        if not filename and 'Content-Type' in r.headers:
            extension = mimetypes.guess_extension(r.headers['Content-Type'].split(';')[0])
            filename = 'download' + extension
            # detect geojson format in a json file
            if extension == '.json' and "FeatureCollection" in str(r.content[:27]):
                filename = 'download.geojson'
        if filename:
            filename = os.path.join(destination_dir, filename)
            open(filename, 'wb').write(r.content)
        return filename
    else:
        return None