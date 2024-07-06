import indeed.indeed_scraper as indeed
import sys
from dotenv import load_dotenv


def main():

    if len(sys.argv) < 2:
        print('supply environment type of either "dev" or "prod"')
        return

    load_dotenv(".env")

    if sys.argv[1] == "prod":
        load_dotenv(".env.production")
    else:
        load_dotenv(".env.development")

    indeed.scrape_indeed()


if __name__ == "__main__":
    main()
