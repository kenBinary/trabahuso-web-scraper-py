import utils.scraping_util as scraper
from selenium.webdriver.common.by import By
import time
from kalibrr.data_cleaning import normalizeData

def scrape():
    url = "https://www.kalibrr.com/home/te/software-developer"
    browser = scraper.browserDriver(url)

    jobCardSelector = "#__next > div > main > div.k-px-4.md\\:k-px-10.k-flex.k-flex-col > div:nth-child(1) > div > div";
    loadMoreButtonSelector = "main > div.k-px-4.md\\:k-px-10.k-flex.k-flex-col > div.k-font-dm-sans.k-w-full.k-flex.k-justify-center.k-mb-10 > button";
    jobTitleCompanySelector = "#__next > div > main > div.k-px-4.md\\:k-px-10.k-flex.k-flex-col > div:nth-child(1) > div > div:nth-child(1) > div.k-flex.k-p-4.k-gap-4.k-justify-between > div"
    jobDescriptionSelector = "#__next > div > main > div.k-px-4.md\\:k-px-10.k-flex.k-flex-col > div:nth-child(1) > div > div:nth-child(1) > div.k-relative > div.blur.k-flex.k-flex-col.k-gap-3.k-px-4.k-pb-4"
    jobLevel = "#__next > div > main > div.k-px-4.md\\:k-px-10.k-flex.k-flex-col > div:nth-child(1) > div > div:nth-child(1) > div.k-relative > div.k-mb-0.blur.k-flex.k-justify-between.k-items-center.k-py-2.k-px-4.k-min-h-10.k-h-auto.k-rounded-b-lg.css-9mbh4l > span.k-flex.k-items-center.k-justify-center.k-h-full.k-rounded-xl.k-bg-gray-300.k-px-2.k-py-1"


    for x in range(5):
        scraper.clickButton(browser,loadMoreButtonSelector)

    time.sleep(5)
    # elements = scraper.getElements(browser,By.TAG_NAME,"h2")
    elements = scraper.getElements(browser,By.CSS_SELECTOR,jobCardSelector)
    rawData = []
    for x in elements:
        rawData.append(x.text.splitlines())
    print(rawData)


    browser.quit()