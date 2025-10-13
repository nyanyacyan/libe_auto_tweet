from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException
from .logger import SimpleLogger
import time
from pathlib import Path
import json

class GetElement:
    def __init__(self, chrome: WebDriver, timeout: int = 15):
        self.logger = SimpleLogger(__name__).get_logger()
        self.chrome = chrome
        self.wait = Wait(driver=self.chrome, timeout=timeout)

    # ----------------------------------------------------------------------------------
    # 単体取得
    def get_element(self, value: str, by: str = "xpath"):
 
        by_dict = {
            "id": By.ID,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "tag": By.TAG_NAME,
            "link": By.LINK_TEXT,
            "name": By.NAME,
            "class": By.CLASS_NAME,
        }

        if by not in by_dict:
            raise ValueError(f"未定義の検索タイプです: {by}")

        return self.chrome.find_element(by_dict[by], value)
    
    # ----------------------------------------------------------------------------------
    # 複数取得
    def get_elements(self, value: str, by: str = "xpath"):
        self.logger.debug(f"複数の要素を取得開始: by: {by} value: {value}")

        by_dict = {
            "id": By.ID,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "tag": By.TAG_NAME,
            "link": By.LINK_TEXT,
            "name": By.NAME,
            "class": By.CLASS_NAME,
        }

        if by not in by_dict:
            raise ValueError(f"未定義の検索タイプです: {by}")

        return self.chrome.find_element(by_dict[by], value)

   # ----------------------------------------------------------------------------------
   # クリック
    def click_element(self, value: str, by: str = "xpath"):
        element = self.get_element(by=by, value=value)
        try:
            element.click()
            self.logger.debug(f"クリック完了しました: {value}")
        except ElementClickInterceptedException:
            self.logger.debug(f"popupなどでClickができません: {element}")
            self.chrome.execute_script("arguments[0].click();", element)
        except ElementNotInteractableException:
            self.logger.debug(f"要素はありますがクリックができません: {element}")
            self.chrome.execute_script("arguments[0].click();", element)
            self.logger.info(f"jsにてクリック実施: {element}")
        except NoSuchElementException:
            self.logger.error(f"[clickElement] 要素が見つかりませんでした: {value}")
            raise
        return element

    # ----------------------------------------------------------------------------------
    # 入力
    def input_element(self, value: str, input_text: str, by: str = "xpath", clear_first=True):
        element = self.get_element(value=value, by=by)
        try:
            if clear_first:
                element.clear()
                self.logger.debug(f"入力欄をクリアしました: {value}")
            element.send_keys(input_text)
            self.logger.debug(f"テキスト入力: {value}")
        except NoSuchElementException:
            self.logger.error(f"[inputElement] 要素が見つかりません: {value}")
            raise
        return element

    def clickClearInput(self, value: str, by: str = "xpath"):
        element = self.get_element(value=value, by=by)
        try:
            element.click()
        except Exception:
            self.chrome.execute_script("arguments[0].focus();", element)
        try:
            element.clear()
        except Exception:
            pass
        return element
    
    # ----------------------------------------------------------------------------------
    # 存在確認
    def find_element(self, value: str, by: str = "xpath"):
        try:
            self.get_element(value=value, by=by)
            self.logger.debug(f"要素が見つかりました: {value}")
            return True
        except NoSuchElementException:
            self.logger.debug(f"要素が見つかりません: {value}")
            return False

    # ----------------------------------------------------------------------------------
    # 入力操作 (クリック or JS でフォーカスを当て,実際に入力)
    def focus_and_type(self, value: str, input_text: str, by: str = "xpath"):
        try:
            element = self.get_element(value=value, by=by)
            self.logger.debug(f"要素が見つかりました: {value}")
            self.chrome.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            try:
                element.click()
            except Exception:
                self.chrome.execute_script("arguments[0].focus();", element)
            element.send_keys(input_text)
            self.logger.info(f"入力完了: {value}")
            return element
        except Exception as e:
            self.logger.error(f"入力に失敗しました: {e}")
            raise

    # ----------------------------------------------------------------------------------
    # 投稿メッセージ：ファイルから読み込む専用　MESSAGE_FILE が空・未指定・ファイルなしの場合は投稿をスキップ
    def resolve_message(self, conf_path: Path) -> str | None:
        self.logger.debug(f"[msg] 設定ファイルからメッセージを読み込み: {conf_path}")

        try:
            with conf_path.open(encoding="utf-8") as f:
                conf = json.load(f)
            auto = conf.get("AUTOPOST", {})
            msg_file = (auto.get("MESSAGE_FILE") or "").strip()

            if not msg_file:
                self.logger.warning("[msg] MESSAGE_FILE が設定されていません。投稿をスキップします。")
                return None

            p = Path(__file__).resolve().parents[2] / msg_file
            if not p.exists():
                self.logger.warning(f"[msg] ファイルが存在しません: {p}")
                return None

            text = p.read_text(encoding="utf-8").strip()
            if not text:
                self.logger.warning(f"[msg] MESSAGE_FILE が空です: {p.name}")
                return None

            self.logger.info(f"[msg] ファイルから読み込み完了: {p.name} ({len(text)} chars)")
            return text

        except Exception as e:
            self.logger.error(f"[msg] メッセージ読み込み中にエラー: {e}")
            return None

    # ----------------------------------------------------------------------------------
    # 未使用
class Wait:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout

    def presence(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def clickable(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def visible(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )
