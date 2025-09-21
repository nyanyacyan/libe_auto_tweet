from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from .. import selectors as S
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#-----------------------------------------------------
def find_element(driver: WebDriver, by: By, value: str, cond: str = "presence", timeout: int = 15, logger=print):
    cond_map = {
        "presence":  EC.presence_of_element_located,
        "visible":   EC.visibility_of_element_located,
        "clickable": EC.element_to_be_clickable,
    }
    log = logger or (lambda msg: None)
   
    log(f"[find] 探します {by}={value}, cond={cond}, timeout={timeout}s")
    try:
        el = WebDriverWait(driver, timeout).until(cond_map[cond]((by, value)))
        log(f"[find] 見つかりました: {by}={value}")
        return el
    except TimeoutException:
        log(f"[find] 見つかりませんでした: {by}={value}")
        return None

#-----------------------------------------------------
def clear_element(driver: WebDriver, by: By, value: str, timeout: int = 20, logger=print):
    el = find_element(driver, by, value, cond="visible", timeout=timeout, logger=logger)
 
    log = logger or (lambda msg: None) 
    if not el:
        log(f"[clear] クリア NG: {by}={value}")
        return None
    el.clear()
    log(f"[clear] クリア OK: {by}={value}")
    return el

#-----------------------------------------------------
def input_element(driver: WebDriver, by: By, value: str, text: str, clear_first: bool = True,
                  timeout: int = 20, logger=print) -> bool:
    el = clear_element(driver, by, value, timeout, logger) if clear_first \
         else find_element(driver, by, value, cond="visible", timeout=timeout, logger=logger)
 
    log = logger or (lambda msg: None) 
    if not el:
        log(f"[input] 入力欄が見つからず中止: {by}={value}")
        return False
    el.send_keys(text)
    log(f"[input] 入力 OK")
    return True

#-----------------------------------------------------
def click_element(driver: WebDriver, by: By, value: str, timeout: int = 15, logger=print) -> bool:
    el = find_element(driver, by, value, cond="clickable", timeout=timeout, logger=logger)
 
    log = logger or (lambda msg: None) 
    if not el:
        log(f"[click] クリック NG: {by}={value}")
        return False
    el.click()
    log(f"[click] クリック OK: {by}={value}")
    return True
    
def _scroll_into_view(driver, el):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center',inline:'center'});", el)
    except Exception:
        pass

def type_into_post_field(driver, text: str, logger):
    el = find_element(driver, By.CSS_SELECTOR, S.POST_INPUT, cond="presence", timeout=8, logger=logger)

    log = logger or (lambda msg: None) 
    if not el:
        # 最後の手段：アクティブ要素に送る
        try:
            active = driver.switch_to.active_element
            ActionChains(driver).click(active).send_keys(text).perform()
            log("[post] アクティブ要素へ入力（フォールバック）")
            return True
        except Exception:
            log("[post] 入力先が見つからず失敗")
            return False

    # 自分でフォーカスして入力
    _scroll_into_view(driver, el)

    # まず JS で focus（クリック不要）
    try:
        driver.execute_script("arguments[0].focus();", el)
    except Exception:
        pass

    # クリア（contenteditable と input の両対応）
    try:
        try:
            el.clear()
        except Exception:

    # A) まず send_keys を試す
            ActionChains(driver).click(el)\
                .key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)\
                .send_keys(Keys.DELETE).perform()
        el.send_keys(text)
        log("[post] 直接 send_keys で入力")
        return True
    except Exception:
        pass

    # B) JS で代入＋イベント発火（React/Vue向け）
    driver.execute_script("""
        const el = arguments[0], val = arguments[1];
        if (el.isContentEditable || el.getAttribute('contenteditable') !== null) {
            el.focus();
            el.innerHTML = '';
            el.dispatchEvent(new InputEvent('input', {bubbles:true}));
            el.textContent = val;
            el.dispatchEvent(new InputEvent('input', {bubbles:true}));
        } else {
            el.focus();
            if ('value' in el) {
                const proto = el.tagName === 'TEXTAREA'
                  ? HTMLTextAreaElement.prototype
                  : HTMLInputElement.prototype;
                const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
                setter ? setter.call(el, val) : (el.value = val);
                el.dispatchEvent(new Event('input', {bubbles:true}));
                el.dispatchEvent(new Event('change', {bubbles:true}));
            }
        }
    """, el, text)
    logger("[post] JS 代入 inputイベントで入力")
    return True

def count_elements(driver, by: By, value: str) -> int:
    try:
        return len(driver.find_elements(by, value))
    except Exception:
        return 0