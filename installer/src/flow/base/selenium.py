import sys
from pathlib import Path
HERE = Path(__file__).resolve()
INSTALLER = HERE.parents[3]            # .../LibeAutoTweet/installer
SRC_DIR = INSTALLER / "src"
sys.path.append(str(SRC_DIR))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
from flow.base.logger import SimpleLogger
import time
import json

logger = SimpleLogger(__name__).get_logger()

def create_driver():
    opts = Options()
    # opts.add_argument("--headless=new")  # 必要ならON
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")
    driver = webdriver.Chrome(options=opts)
    logger.debug("Chrome driver created")
    return driver


# ================================
# クリック処理：外部クラス (同一ファイル内)
# ================================
class ClickElement:
    """クリック処理をまとめた薄いラッパー。通常クリックと安全クリックを提供。"""
    def __init__(self, driver, log=None, timeout=12):
        self.d = driver
        self.log = log
        self.wait = WebDriverWait(driver, timeout)

    def click(self, by, value):
        """通常クリック。クリック可能になるまで待機。"""
        el = self.wait.until(EC.element_to_be_clickable((by, value)))
        el.click()
        if self.log: self.log.debug(f"[click] {by}={value}")

    def safe_click(self, by, value):
        """通常→scrollIntoView→JS click の順でトライ。成功なら True。"""
        el = self.wait.until(EC.presence_of_element_located((by, value)))
        try:
            self.wait.until(EC.element_to_be_clickable((by, value)))
            el.click()
            if self.log: self.log.debug(f"[safe_click] normal {by}={value}")
            return True
        except (ElementClickInterceptedException, ElementNotInteractableException, Exception):
            try:
                self.d.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                self.d.execute_script("arguments[0].click();", el)
                if self.log: self.log.debug(f"[safe_click] js {by}={value}")
                return True
            except Exception:
                if self.log: self.log.debug(f"[safe_click] failed {by}={value}")
                return False


class LibeClient:
    def __init__(self, driver, log=None, timeout=12):
        self.driver = driver
        # 元の `logger or logger` バグを修正：未指定ならデフォルトロガーを生成
        self.logger = log if log is not None else SimpleLogger(__name__).get_logger()
        self.wait = WebDriverWait(driver, timeout)
        # ← 外部クラス風 ClickElement を使用
        self.clicker = ClickElement(driver, self.logger, timeout)

    def login(self, email: str, password: str):
        d = self.driver
        d.get("https://libecity.com/signin?redirect=/mypage/top")
        d.implicitly_wait(5)

        d.find_element(By.CSS_SELECTOR, 'input[placeholder="メールアドレス"]').send_keys(email)
        d.find_element(By.CSS_SELECTOR, 'input[placeholder="パスワード"]').send_keys(password)

        # 外部クラスでクリック
        self.clicker.click(By.XPATH, '//button[span[text()="ログイン"]]')
        time.sleep(2)
        if self.logger: self.logger.info("Login submitted")

    def post_tweet(self, message: str):
        d = self.driver
        if self.logger: self.logger.debug("tweet")

        d.get('https://libecity.com/tweet/all')

        # 外部クラスで安全クリック（JSフォールバック含む）
        self.clicker.safe_click(By.CSS_SELECTOR, "button.btn_tweetInput")
        time.sleep(2)

        d.switch_to.active_element.send_keys(message)
        if self.logger: self.logger.info(f"Post preview: {message[:40]}...")
        time.sleep(10)


def close_driver(driver):
    driver.quit()
    logger.debug("Chrome driver closed")


# ------------------------
# 単体動作確認用のメイン 
# ------------------------
if __name__ == "__main__":
    # cfg 読み込み
    cfg_path = INSTALLER / "config" / "config.json"
    if not cfg_path.exists():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {cfg_path}")

    text = cfg_path.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError(f"設定ファイルが空です: {cfg_path}")

    logger.debug(f"Using config path: {cfg_path}")

    try:
        cfg = json.loads(text)
    except json.JSONDecodeError as e:
        preview = text[:100].replace("\n", "\\n")
        raise ValueError(f"config.json が不正なJSONです（位置: {e.pos} 付近）。先頭プレビュー: {preview}") from e

    email = cfg["LIBE"]["ID"]
    password = cfg["LIBE"]["PASS"]
    sample_text = "テスト投稿（プレビュー）です"

    driver = create_driver()
    bot = LibeClient(driver, logger)

    try:
        bot.login(email, password)
        bot.post_tweet(sample_text)
        logger.info("Flow finished (preview)")
    finally:
        close_driver(driver)
