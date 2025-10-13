from pathlib import Path
import json, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from .base.logger import SimpleLogger
from .base.chrome import ChromeManager
from .base.selenium_element import GetElement, Wait


class AutoLoginFlow:
    def __init__(self):
        self.logger = SimpleLogger(__name__).get_logger()
        self.conf = self._load_config()
        self.ChromeManager = ChromeManager()
        self.chrome = self.ChromeManager.start_chrome()
        self.url = "https://libecity.com/signin"
        self.tweet_page = "https://libecity.com/tweet/my"
        self.get_element = GetElement(chrome=self.chrome)

    def _load_config(self):
        base_dir = Path(__file__).resolve().parents[2]  # installer/src/flow → installer
        config_path = base_dir / "config" / "config.json"
        with config_path.open(encoding="utf-8") as f:
            return json.load(f)        

    def open_site(self, url: str):
        self.logger.info(f"サイトを開きます: {url}")
        self.chrome.get(url)
        time.sleep(1)

    def close_browser(self):
        self.logger.info(f"ブラウザを閉じます")
        self.chrome.quit
        self.chrome = None
        
# ------------------------------------------------------------------------------
# login & tweet 
# ------------------------------------------------------------------------------

    def process(self):
        # 1. サイトを開く
        self.open_site(self.url)

        # 2. ID(メールアドレス)入力
        elem = self.get_element.clickClearInput(value='input[placeholder="メールアドレス"]', by="css")
        elem.send_keys(self.conf["EMAIL"])

        # 3. パスワード入力
        pw_elem = self.get_element.clickClearInput(value='input[placeholder="パスワード"]', by="css")
        pw_elem.send_keys(self.conf.get("PASSWORD", ""))

        # 4. ログインボタンをクリック
        self.get_element.click_element(value="button.btn.bg_yellow", by="css")
        time.sleep(1)

        # 5. つぶやきページを開く
        self.open_site(self.tweet_page)
        time.sleep(1)

        # 6. 投稿欄にメッセージ入力
        msg = self.get_element.resolve_message(Path(__file__).resolve().parents[2] / "config" / "config.json")
        self.get_element.find_element(
            value=".public-DraftEditor-content [contenteditable], [data-lexical-editor] [contenteditable], [role='textbox'], [contenteditable], textarea, input[type='text']",
            by="css"
        )        
        self.get_element.input_element(value="textarea.tweetInput", input_text=msg, by="css")
        time.sleep(1)

        # 7. 投稿ボタンをクリック
        self.get_element.click_element(value="button.tweetBtn", by="css")
        time.sleep(1)

        # 8. サイトを閉じる
        self.close_browser()  


