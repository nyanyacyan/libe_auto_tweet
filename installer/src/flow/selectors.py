# login
EMAIL_INPUT = "input[placeholder='メールアドレス']"
PASSWORD_INPUT = "input[placeholder='パスワード"
LOGIN_BTN_X = "//button[span[normalize-space(.)='ログイン']]"
AFTER_LOGIN_PROOF = "a[href='/mypage/home'], a[href='/mypage/top']"

# tweet
OPEN_TWEET_BTN = "button.btn_tweetInput"   # 投稿モーダルを開くボタン

# 入力フィールド
POST_INPUT = (
    ".public-DraftEditor-content [contenteditable], "
    "[data-lexical-editor] [contenteditable], "
    "[role='textbox'], "
    "[contenteditable], "
    "textarea, "
    "input[type='text']"
)

# 送信ボタン
POST_SUBMIT = ".tweetBtnArea button:not([disabled]):not(.is-disabled)"

# 成功サイン（任意）
POST_SUCCESS = "[data-testid='post-item'], .toast-success, .alert-success"