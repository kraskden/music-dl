import argparse

from app import App
from downloader.downloader import Downloader
from plugin import get_plugins_names

if __name__ == "__main__":
    downloaders = get_plugins_names('downloader', Downloader)

    parser = argparse.ArgumentParser("music-dl", description="Download music from streaming services")
    parser.add_argument("target", help="Target directory")
    parser.add_argument("-i", dest="source", help="Source url")
    parser.add_argument("-d", default="hitmo", dest="downloader", help="Which downloader to use", choices=downloaders)
    parser.add_argument("-a", default=False, dest="download_all", help="Download all", action='store_true')

    args = parser.parse_args()
    app = App(args.target, args.downloader)

    if args.source is not None:
        app.source_download(args.source, args.download_all)
    else:
        app.interactive_download()