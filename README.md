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

## インストール
1. このリポジトリをクローンまたはダウンロードします。
```
git clone https://github.com/xM1guel/SummaryApp.git
```
2. 必要なライブラリをインストールします。
```
pip install spacy networkx scikit-learn docx2txt PyPDF2
```
3. spaCyの言語モデルをダウンロードします
```
python -m spacy download ja_core_news_sm
python -m spacy download en_core_web_sm
```

## 注意事項

- 大きなファイルの処理には時間がかかる場合があります。
- 言語モデルの精度により、要約の質が変わる可能性があります。

## 作成者
- xM1guel
- [Zenn](https://zenn.dev/miguel)
