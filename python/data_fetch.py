import urllib
import urllib.error
import urllib.request
import logging


logger = logging.getLogger(__name__)


def fetch(url, fallback_file):
    """
    Please use only the python standard library for fetching the data from the server.
    In case the server responds with a non 2xx status code,
    your fetch function should return the content of the fallback_file.
    """
    try:
        response = urllib.request.urlopen(url, timeout=30)
        response_code = response.getcode()
    except (urllib.error.URLError, urllib.error.HTTPError, Exception) as ex:
        logger.warning(f"Could not fetch data from {url}. Switching to fallback file.")
        with open(fallback_file, encoding="utf-8") as f:
            data = f.read()
        print(ex)
    else:
        if response_code < 200 or response_code >= 300:
            pass
        data = response.read().decode("utf-8")
    return data
