# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# import

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# **********************************************************************************
# class定義


    # ------------------------------------------------------------------------------
    # 関数定義


    # ------------------------------------------------------------------------------
    # 関数定義


    # ------------------------------------------------------------------------------

from pathlib import Path
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flow.base.libe_bot import LibeBot
from flow.base.logger import SimpleLogger

def create_driver():
    opts = Options()
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")
    return webdriver.Chrome(options=opts)

if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parents[2]   # プロジェクトルート
    cfg = json.loads((ROOT / "config" / "config.json").read_text(encoding="utf-8"))

    email = cfg["LIBE"]["ID"]
    password = cfg["LIBE"]["PASS"]
    sample_text = "テスト投稿（プレビュー）です"

    logger = SimpleLogger(__name__).get_logger()
    driver = create_driver()
    bot = LibeBot(driver, logger)

    try:
        bot.login(email, password)
        bot.post_tweet(sample_text)
        logger.info("ログイン & 投稿欄入力まで完了")
    finally:
        driver.quit()


# **********************************************************************************

