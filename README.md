## 多言語対応文書要約アプリケーション
このアプリケーションは、テキスト、Word、PDFファイルの内容を自動的に要約する多言語対応のツールです。日本語と英語の両方に対応しており、簡単に文書の要約を生成することができます。

主な機能：
- 複数のファイル形式（.txt, .docx, .pdf）に対応
- 日本語と英語の文書に対応
- 要約の長さ（文の数）を調整可能
- 要約結果のコピーと保存機能
- プログレスバーによる処理状況の可視化
- アプリケーション言語の切り替え（日本語/英語）

## 必要条件
- Python 3.8以上
- 必要なライブラリ：
  - spacy
  - networkx
  - scikit-learn
  - docx2txt
  - PyPDF2
 
## 言語モデルの設定
事前に使用する言語モデルをダウンロードしてください。
- [英語モデル](
https://github.com/explosion/spacy-models/releases/download/es_core_news_lg-3.1.0/es_core_news_lg-3.1.0.tar.gz)

- [日本語モデル](https://github.com/explosion/spacy-models/releases/download/ja_core_news_sm-3.7.0/ja_core_news_sm-3.7.0.tar.gz
)

## インストール
1. このリポジトリをクローンまたはダウンロードします。
```
git clone https://github.com/xM1guel/SummaryApp.git
```
2. `setup_and_run.bat` をダブルクリックして実行します。
3. セットアッププロセスが完了すると、アプリケーションが自動的に起動します。

## 注意事項
- このスクリプトを実行するには、Pythonがシステムにインストールされ、PATHに追加されている必要があります。
- 初回実行時には時間がかかる場合があります。
- セットアッププロセス中にWindows SmartScreenの警告が表示される場合があります。その場合は「詳細情報」をクリックし、「実行」を選択してください。

- 大きなファイルの処理には時間がかかる場合があります。
- 言語モデルの精度により、要約の質が変わる可能性があります。

## 作成者
- xM1guel
- [Zenn](https://zenn.dev/miguel)
