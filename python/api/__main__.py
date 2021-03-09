from configparser import ConfigParser
from importlib.resources import open_text

def main():
    cfg = ConfigParser()
    cfg.read_string(open_text("api", "config.txt").readlines())
    url = cfg.get("settings", "api_url")

    print('url:{}'.format(url))

if __name__ == "__main__":
    main()
