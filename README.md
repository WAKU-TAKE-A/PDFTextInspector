# PDFTextInspector

**PDFTextInspector** は、PDFファイルからテキストを抽出し、フォントサイズや座標をもとに「見出し」「リスト」などを自動判別し、構造化されたテキスト（Markdown風）を出力するGUIアプリケーションです。

## 特徴

- フォントサイズなどに基づき見出しレベルを自動判定
- リスト形式（箇条書き・番号付き）も検出（正規表現）
- INIファイルで検出ルールをある程度カスタマイズ可能
- GUIで簡単操作
- 構造化されたテキストを `.txt` ファイルとして保存

## GUIスクリーンショット

![GUI](https://raw.githubusercontent.com/WAKU-TAKE-A/PDFTextInspector/refs/heads/main/screeshot01.jpg)

## 使用方法

1. このリポジトリをクローンまたはダウンロード
2. 必要なライブラリをインストール:
    ```bash
    pip install pymupdf ttkbootstrap
    ```
3. アプリを起動:
    ```bash
    python PDFTextInspector.py
    ```
4. GUIからPDFファイルを選択
5. 任意のページ番号を入力して[解析]でフォントサイズや位置を調べます。
6. iniファイルを編集します。
7. [全テキスト出力]で構造化テキストを保存

## 出力ファイル

- 入力したPDFと同じフォルダに、構造化されたテキストファイル（例: `document.txt`）が保存されます。

## ルールのカスタマイズ

`PDFTextInspector.ini` というINIファイルにて、以下のような抽出ルールを変更できます

```ini
[Rules]

; 利用する見出しの設定
enabled_heading_levels = 1,2,3,4,5

; 指定したページの指定範囲の文字列をタイトル (#) 
big_heading_page = 1
big_heading_x_min = 20.0
big_heading_x_max = 100.0
big_heading_y_min = 300.0
big_heading_y_max = 500.0

; 大見出し (##) のフォントサイズ範囲
chapter_min_size = 100.0
chapter_max_size = 200.0

; 中見出し (###) のフォントサイズ範囲
small_heading_min_size = 17.8
small_heading_max_size = 18.2

; 小見出し (####) のフォントサイズ範囲
lower_heading_min_size = 14.8
lower_heading_max_size = 15.2

; 小小見出し (#####) のフォントサイズ範囲
lower2_heading_min_size = 13.8
lower2_heading_max_size = 14.2

; 無秩リストの頭文字マッチ用正規表現パターン
unordered_list_pattern = ^・

; 有秩リストの頭文字マッチ用正規表現パターン
ordered_list_pattern = ^\d

; ページ内で除外する領域（テキストのブロックの左上座標が、下の設定より紙面の外側にある場合は除外）
ignore_left_pt = 0
ignore_right_pt = 20
ignore_top_pt = 20
ignore_bottom_pt = 50

; テキストのブロックの上下関係が同じと考える範囲
line_group_threshold = 5.0
```

## 依存ライブラリ

- PyMuPDF (fitz)
- ttkbootstrap

## ライセンス

MIT License

## 補足

* 本ツールは文章中心のPDFを対象としています。画像中心のPDFやスキャンPDFには対応していません。
* テキスト構造の抽出ルールは文書のフォーマットにより調整が必要な場合があります。