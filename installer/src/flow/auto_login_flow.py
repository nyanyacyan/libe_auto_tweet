from pathlib import Path
import json, sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from .base.logger import SimpleLogger
from .base.selenium_ops import find_element, input_element, click_element, type_into_post_field
from . import selectors as S

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]                     # installer/
CONFIG_PATH = ROOT / "config" / "config.json"

def load_config(path: Path):
    if not path.exists():
        print(f"[ERROR] config が見つかりません: {path}"); sys.exit(1)
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("BASE_URL", "https://libecity.com")
    data.setdefault("HEADLESS", False)
    data.setdefault("TIMEOUT_SEC", 30)
    if not data.get("EMAIL") or not data.get("PASSWORD"):
        print("[ERROR] EMAIL / PASSWORD が未設定です"); sys.exit(1)
    return data

def create_driver(headless=True, window_size="1280,900"):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")  # config で指定
    opts.add_argument("--disable-gpu")
    opts.add_argument(f"--window-size={window_size}")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=opts)

def get_message(cfg: dict) -> str:
    ap = cfg.get("AUTOPOST", {})
    msg = (ap.get("MESSAGE") or "").strip()
    if not msg and ap.get("MESSAGE_FILE"):
        p = Path(ap["MESSAGE_FILE"])
        if not p.exists():
            print(f"[ERROR] MESSAGE_FILE が見つかりません: {p}")
            sys.exit(5)
        msg = p.read_text(encoding="utf-8").strip()
    return msg


##################################################################
if __name__ == "__main__":
    cfg = load_config(CONFIG_PATH)
    d = create_driver(headless=cfg["HEADLESS"])

    log = SimpleLogger("post_flow").get_logger()

#-----------------------------------------------------------------
# login　&  tweet Flow
#-----------------------------------------------------------------
    try:
        base = cfg["BASE_URL"].rstrip("/")

        # 投稿本文（config から）
        message = get_message(cfg)
        if not message:
            log.error("[post] 投稿本文が空です。config.json を確認してください")
            sys.exit(5)

        # 1) サインイン
        d.get(f"{base}/signin")

        # 2) ログイン　入力 → クリック
        ok = input_element(d, By.CSS_SELECTOR, S.EMAIL_INPUT,   cfg["EMAIL"],    clear_first=True, timeout=cfg["TIMEOUT_SEC"])
        ok = ok and input_element(d, By.CSS_SELECTOR, S.PASSWORD_INPUT, cfg["PASSWORD"], clear_first=True, timeout=cfg["TIMEOUT_SEC"])
        ok = ok and click_element(d, By.XPATH, S.LOGIN_BTN_X, timeout=cfg["TIMEOUT_SEC"])
     
        if not ok:
            log.error("[login] 入力/クリックに失敗"); 
            sys.exit(2)

        # 3) ログイン判定： “30秒” 待つ（自然遷移を待つ）
        proof = find_element(d, By.CSS_SELECTOR, S.AFTER_LOGIN_PROOF, cond="presence", timeout=30)
        if not proof:
            log.error("[login] ログイン失敗 成功サインが見つからない");
            sys.exit(3)
        log.info("[login] ログイン成功！")

       # 4) 投稿ページへ遷移
        d.get(f"{base}/tweet/all")

        # 投稿モーダルを開く
        ok = click_element(d, By.CSS_SELECTOR, S.OPEN_TWEET_BTN, timeout=cfg["TIMEOUT_SEC"], logger=log.info)
        if not ok:
            log.error("[post] 投稿ボタンが見つからない/クリックできない")
            sys.exit(4)

        time.sleep(20)

        # 入力（フォールバック込み）
        ok = type_into_post_field(d, message, logger=log.info)
        if not ok:
            log.error("[post] テキスト入力に失敗"); sys.exit(4)

        # 5) 送信クリック
        ok = click_element(d, By.CSS_SELECTOR, S.POST_SUBMIT, timeout=cfg["TIMEOUT_SEC"], logger=log.info)
        if not ok:
            log.error("[post] 送信ボタンが見つからない/クリックできない")
            sys.exit(4)

#         # 5) 送信（DRY_RUN で分岐）
#        DRY_RUN = bool(cfg.get("AUTOPOST", {}).get("DRY_RUN", False))
#        if DRY_RUN:
#            log.info("[post] DRY_RUN true: 送信はしません")
#        else:
#            ok = click_submit_strong(d, log.info, timeout=10)
#            if not ok:
#                sys.exit(4)


        # 6) 投稿確認
        find_element(d, By.CSS_SELECTOR, S.POST_SUCCESS, cond="presence", timeout=15, logger=log.info)
        log.info("[post] 投稿完了！")
        sys.exit(0)

    finally:
        d.quit()
