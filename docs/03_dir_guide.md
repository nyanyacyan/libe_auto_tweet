# ディレクトリ構成

## 【目的】

このドキュメントは、本プロジェクトのディレクトリ構成を共有し、ファイルの配置ルールを統一するためのものです。

---

## 【ディレクトリ構成】
```plaintext
tokyu_sns_image_tool
├── docs
│   ├── 00_setup_guide.md
│   ├── 01_security_key_guide.md
│   ├── 02_naming_guide.md
│   ├── 03_dir_guide.md
│   ├── 04_coding_guide.md
│   ├── 05_branch_guide.md
│   ├── 06_commit_guide.md
│   ├── 07_pr_guide.md
│   ├── 08. comment_guide.md
│   ├── 09_selenium.md
│   └── 10_const_guide.md
├── installer
│   ├── bin
│   │   ├── bat
│   │   └── requirements.txt
│   ├── config
│   │   └── config.json
│   ├── data
│   │   ├── pickle
│   │   ├── input
│   │   │   ├── fonts
│   │   │   │   └── MPLUSRounded1c-ExtraBold.ttf
│   │   │   └── template
│   │   │       ├── A.png
│   │   │       ├── B.png
│   │   │       ├── C.png
│   │   │       ├── D.png
│   │   │       └── LAST.png
│   │   └── output
│   │       └── logs
│   ├── src
│   │   ├── flow
│   │   │   ├── base
│   │   │   │   ├── chrome.py
│   │   │   │   ├── image_editor.py
│   │   │   │   ├── path.py
│   │   │   │   ├── utils.py
│   │   │   │   ├── ai.py
│   │   │   │   ├── selenium.py
│   │   │   │   └── pickle.py
│   │   │   ├── const
│   │   │   │   ├── const_element.py
│   │   │   │   ├── const_str.py
│   │   │   │   └── const_prompt.py
│   │   │   ├── generate_image_flow.py
│   │   │   ├── input_db_flow.py
│   │   │   ├── main_flow.py
│   │   │   └── scraper_flow.py
│   │   └── main.py
│   └── tests
├── README.md
├── .gitignore
└── requirements.txt
```

<br>



## 【ルール】
- すべての実装コードは installer/ 以下にまとめます
- config/ 配下にはセキュリティ情報を格納し、Gitに含めません
- 各ディレクトリは 責務ごとに明確に分類し、混在しないように注意します


<br>



## 【ポイント】
- 新たにディレクトリを作成する場合は、PMに相談・レビューを通してから作成すること
- ディレクトリ名はすべて snake_case で統一してください（例：data_loader, user_service）


<br>



## 【補足（任意）】
- 初期セットアップ後に tree コマンドで構成を確認することをおすすめします：

<br>

## ✅ ディレクトリ構成チェックリスト

新しいディレクトリやファイルを作成・追加する際には、以下の項目を確認してください：

- [ ] 作成前に PM に相談し、構成の妥当性について確認した
- [ ] 目的・責務に合った適切な場所にファイルを配置している
- [ ] ディレクトリ名は snake_caseで命名した
- [ ] セキュリティ・認証情報などは config配下 .gitignore に追加確認した
- [ ] 実装コードは installer/src/ 以下にまとめた（外に出していない）

