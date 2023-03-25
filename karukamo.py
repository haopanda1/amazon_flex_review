from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from utils.chromeDriver_init import ChromeLauncher
import pandas as pd
from typing import List
from loguru import logger


class karukamo_scrapper:
    def __init__(self, chrome_driver_dir: str, headless: bool):
        self.chrome = ChromeLauncher(chrome_driver_dir=chrome_driver_dir, headless=headless).start_chrome_driver()
        self.short_wait = WebDriverWait(self.chrome, 10)
        self.url = 'https://karukamo.info/amazonflex-kutikomi/'

    def run(self, result_dir: str):
        logger.info('Starting Karu Kamo Records Extraction Process...')
        self._get_comment()
        review_list = self._get_comment()
        date_list = self._get_comment_date()
        df_result = self._consolidate_extraction(review_list, date_list)
        df_result.to_csv(result_dir, encoding='utf-16', index=False)
        logger.success('Records Extraction Process Complete.')

    def _get_comment(self) -> List[str]:
        self.chrome.get(self.url)
        reviews = self.short_wait.until(
            expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,'glsr-review'))
        )
        reviews = [x.text.replace('\n', ' ') for x in reviews]
        return reviews

    def _get_comment_date(self) -> List[str]:
        dates = self.short_wait.until(
            expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,'glsr-review-date'))
        )
        dates = [x.text.strip().replace('年','-').replace('月', '-').replace('日', '') for x in dates]
        return dates

    def _consolidate_extraction(self, reviews: List[str], dates: List[str]) -> pd.DataFrame:
        df = pd.DataFrame({'date':dates, 'review':reviews})
        return df

if __name__ == '__main__':
    chrome_dir = r"C:\Users\orf-haoj\Desktop\chromedriver.exe"
    headless = True
    output_dir = r'C:\Users\orf-haoj\Desktop\karukamo.csv'
    karukamo_scrapper(chrome_driver_dir=chrome_dir, headless=headless).run(output_dir)



