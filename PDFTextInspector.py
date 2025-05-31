import fitz # PyMuPDFの別名
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import re
import os
import configparser

INI_FILE_NAME = "PDFTextInspector.ini"

def load_rules():
    config = configparser.ConfigParser()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INI_FILE_PATH = os.path.join(BASE_DIR, INI_FILE_NAME)
    if not os.path.exists(INI_FILE_PATH):
        # iniがなければデフォルト値
        return {
            "enabled_heading_levels":"1,2,3,4,5",
            "big_heading_page": 1,
            "big_heading_x_min": 20.0,
            "big_heading_x_max": 100.0,
            "big_heading_y_min": 300.0,
            "big_heading_y_max": 500.0,
            "chapter_min_size": 100.0,
            "chapter_max_size": 200.0,
            "small_heading_min_size": 17.8,
            "small_heading_max_size": 18.2,
            "lower_heading_min_size": 14.8,
            "lower_heading_max_size": 15.2,
            "lower2_heading_min_size": 13.8,
            "lower2_heading_max_size": 14.2,
            "unordered_list_pattern": r"^•",
            "ordered_list_pattern": r"^\d",
            "ignore_left_pt": 50,
            "ignore_right_pt": 50,
            "ignore_top_pt": 50,
            "ignore_bottom_pt": 50,
            "line_group_threshold": 5.0,
        }

    config.read(INI_FILE_PATH, encoding="utf-8")
    rules = config["Rules"]

    def get_float(key, default):
        try:
            return float(rules.get(key, default))
        except Exception:
            return default

    def get_int(key, default):
        try:
            return int(rules.get(key, default))
        except Exception:
            return default
    
    levels_str = rules.get("enabled_heading_levels", "1,2,3,4,5")
    enabled_levels = levels_str.split(",")

    return {
        "enabled_heading_levels": enabled_levels,
        "big_heading_page": get_int("big_heading_page", 1),
        "big_heading_x_min": get_float("big_heading_x_min", 20.0),
        "big_heading_x_max": get_float("big_heading_x_max", 100.0),
        "big_heading_y_min": get_float("big_heading_y_min", 300.0),
        "big_heading_y_max": get_float("big_heading_y_max", 500.0),
        "chapter_min_size": get_float("chapter_min_size", 100.0),
        "chapter_max_size": get_float("chapter_max_size", 200.0),
        "small_heading_min_size": get_float("small_heading_min_size", 17.8),
        "small_heading_max_size": get_float("small_heading_max_size", 18.2),
        "lower_heading_min_size": get_float("lower_heading_min_size", 14.8),
        "lower_heading_max_size": get_float("lower_heading_max_size", 15.2),
        "lower2_heading_min_size": get_float("lower2_heading_min_size", 13.8),
        "lower2_heading_max_size": get_float("lower2_heading_max_size", 14.2),
        "unordered_list_pattern": rules.get("unordered_list_pattern", r"^•"),
        "ordered_list_pattern": rules.get("ordered_list_pattern", r"^\d"),
        "ignore_left_pt": get_float("ignore_left_pt", 50),
        "ignore_right_pt": get_float("ignore_right_pt", 50),
        "ignore_top_pt": get_float("ignore_top_pt", 50),
        "ignore_bottom_pt": get_float("ignore_bottom_pt", 50),
        "line_group_threshold": get_float("line_group_threshold", 5.0)
    }


class PDFTextInspector:
    def __init__(self, root):
        self.root = root
        self.root.title("PDFTextInspector")
        self.root.geometry("900x600")

        self.pdf_path = None
        self.doc = None

        self.left_frame = tb.Frame(self.root, padding=10)
        self.right_frame = tb.Frame(self.root, padding=10)
        self.left_frame.pack(side=LEFT, fill=Y)
        self.right_frame.pack(side=RIGHT, expand=True, fill=BOTH)

        self.file_button = tb.Button(
            self.left_frame, text="ファイルの選択", command=self.select_file, bootstyle="success"
        )
        self.file_button.pack(fill=X, pady=(0, 5))

        self.page_label = tb.Label(
            self.left_frame, text="ページ番号を入力してください:（ファイル未選択）", bootstyle="info"
        )
        self.page_label.pack(pady=(0, 5))
        self.page_entry = tb.Entry(self.left_frame, state="disabled")
        self.page_entry.pack(fill=X, pady=(0, 10))

        self.analyze_button = tb.Button(
            self.left_frame, text="解析", command=self.analyze_pdf, bootstyle="primary", state="disabled"
        )
        self.analyze_button.pack(fill=X, pady=(0, 5))

        self.extract_all_button = tb.Button(
            self.left_frame,
            text="全テキスト出力",
            command=self.extract_all_text,
            bootstyle="primary",
            state="disabled"
        )
        self.extract_all_button.pack(fill=X)

        self.result_text = tb.ScrolledText(
            self.right_frame, wrap="word", font=("Courier New", 11)
        )
        self.result_text.pack(expand=True, fill=BOTH)
        self.result_text.configure(state="disabled")

    def set_result_text(self, message):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", message)
        self.result_text.configure(state="disabled")
        self.result_text.see("end")

    def select_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("PDFファイル", "*.pdf")], title="PDFファイルを選択してください"
        )
        if not path:
            return
        try:
            doc = fitz.open(path)
        except Exception as e:
            messagebox.showerror("エラー", f"PDFファイルを開けませんでした。\n{e}")
            return

        self.pdf_path = path
        self.doc = doc

        max_page = len(self.doc)
        page0 = self.doc[0]
        page_width = round(page0.rect.width, 2)
        page_height = round(page0.rect.height, 2)

        self.page_label.configure(
            text=f"ページ番号を入力してください:（1〜{max_page}）", bootstyle="info"
        )
        self.page_entry.configure(state="normal")
        self.analyze_button.configure(state="normal")
        self.extract_all_button.configure(state="normal")

        self.set_result_text(
            f"選択ファイル: {self.pdf_path}\n合計ページ数: {max_page}\n"
            f"ページサイズ (横×縦): {page_width}pt × {page_height}pt"
        )

    def analyze_pdf(self):
        if not self.doc:
            messagebox.showwarning("エラー", "先にPDFファイルを選択してください。")
            return

        page_str = self.page_entry.get().strip()
        if not page_str.isdigit():
            messagebox.showwarning("エラー", "ページ番号は数字で入力してください。")
            return

        page_num = int(page_str)
        max_page = len(self.doc)
        if page_num < 1 or page_num > max_page:
            messagebox.showwarning("エラー", f"ページ番号は1〜{max_page}の範囲で入力してください。")
            return

        text = self.extract_page_text_info(page_num)
        self.set_result_text(text)

    def extract_page_text_info(self, page_number):
        page = self.doc[page_number - 1]
        text_dict = page.get_text("dict")

        lines = [f"--- ページ {page_number} のテキストとフォントサイズ一覧 ---\n"]

        blocks = [b for b in text_dict["blocks"] if b["type"] == 0]
        blocks.sort(key=lambda b: (b["bbox"][1], b["bbox"][0]))

        block_index = 0
        for block in blocks:
            block_index = block_index + 1
            lines_in_block = block["lines"]
            lines_in_block.sort(key=lambda l: (l["bbox"][1], l["bbox"][0]))

            for line in lines_in_block:
                line_x0 = round(line["bbox"][0], 2)
                line_y0 = round(line["bbox"][1], 2)

                line_text = "".join(span["text"] for span in line["spans"]).strip()
                if not line_text:
                    continue
                line_text = line_text.replace('\n', '\\n')

                max_size = max(span["size"] for span in line["spans"])
                max_size_rounded = round(max_size, 2)

                lines.append(
                    f"ブロック: '{block_index} 'テキスト: '{line_text}'  サイズ: {max_size_rounded}pt  座標(x0, y0): ({line_x0}, {line_y0})"
                )

        lines.append(f"\n--- ページ {page_number} の出力終了 ---")
        return "\n".join(lines)

    def extract_structured_text(self, rules):
        if not self.pdf_path:
            return "PDFファイルが選択されていません。"

        try:
            doc = fitz.open(self.pdf_path)
        except Exception as e:
            return f"PDFファイルを開けませんでした: {e}"

        ignore_left_pt = rules["ignore_left_pt"]
        ignore_right_pt = rules["ignore_right_pt"]
        ignore_top_pt = rules["ignore_top_pt"]
        ignore_bottom_pt = rules["ignore_bottom_pt"]
        enabled_levels = rules["enabled_heading_levels"]
        unordered_list_re = re.compile(rules["unordered_list_pattern"])
        ordered_list_re = re.compile(rules["ordered_list_pattern"])
        block_group_threshold = rules["line_group_threshold"]

        output = []
        title = ""

        for page_idx, page in enumerate(doc, start=1):
            page_width = page.rect.width
            page_height = page.rect.height

            blocks = [b for b in page.get_text("dict")["blocks"] if b["type"] == 0]

            # ③ブロックのソート（yの閾値付きで）
            def block_sort_key(b):
                y0 = round(b["bbox"][1] / block_group_threshold) * block_group_threshold
                x0 = b["bbox"][0]
                return (y0, x0)

            blocks.sort(key=block_sort_key)

            for block in blocks:
                bbox = block.get("bbox", None)
                if bbox:
                    left, top, right, bottom = bbox
                    if (left < ignore_left_pt or
                        left > page_width - ignore_right_pt or
                        top < ignore_top_pt or
                        bottom > page_height - ignore_bottom_pt):
                        continue

                for line in block["lines"]:
                    line_text = "".join(span["text"] for span in line["spans"]).strip()
                    if not line_text:
                        continue

                    max_size = max(span["size"] for span in line["spans"])
                    x0 = line["bbox"][0]
                    y0 = line["bbox"][1]

                    # 見出し・リスト検出
                    if ('1' in enabled_levels and
                        page_idx == rules["big_heading_page"] and
                        rules["big_heading_x_min"] <= x0 <= rules["big_heading_x_max"] and
                        rules["big_heading_y_min"] <= y0 <= rules["big_heading_y_max"]):
                        if title == "":
                            title = line_text
                        else:
                            title = title + " " + line_text
                        continue

                    if ('2' in enabled_levels and rules["chapter_min_size"] <= max_size <= rules["chapter_max_size"]):
                        output.append(f"\n## {line_text}\n\n")
                        continue

                    if ('3' in enabled_levels and rules["small_heading_min_size"] <= max_size <= rules["small_heading_max_size"]):
                        output.append(f"\n### {line_text}\n\n")
                        continue

                    if ('4' in enabled_levels and rules["lower_heading_min_size"] <= max_size <= rules["lower_heading_max_size"]):
                        output.append(f"\n#### {line_text}\n\n")
                        continue

                    if ('5' in enabled_levels and rules["lower2_heading_min_size"] <= max_size <= rules["lower2_heading_max_size"]):
                        output.append(f"\n##### {line_text}\n\n")
                        continue

                    first_text = line["spans"][0]["text"].strip() if line["spans"] else ""
                    if unordered_list_re.match(first_text):
                        content = first_text[1:].strip() + "".join(span["text"] for span in line["spans"][1:])
                        content = content.lstrip()
                        output.append(f"* {content}\n")
                        continue

                    if ordered_list_re.match(first_text):
                        content = first_text[1:].strip() + "".join(span["text"] for span in line["spans"][1:])
                        content = content.lstrip()
                        output.append(f"1. {content}\n")
                        continue

                    # 通常テキスト
                    output.append(line_text + "\n")

        if title != "":
            output = [f"# {title}\n\n"] + output 
        return "".join(output)


    def extract_all_text(self):
        if not self.pdf_path:
            messagebox.showwarning("エラー", "先にPDFファイルを選択してください。")
            return

        self.set_result_text("PDFから全テキストを抽出中…しばらくお待ちください。")
        self.root.update()

        rules = load_rules()
        result = self.extract_structured_text(rules)
        if not result.strip():
            messagebox.showinfo("情報", "抽出されたテキストがありません。")
            self.set_result_text("")
            return

        txt_path = os.path.splitext(self.pdf_path)[0] + ".txt"
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(result)
        except Exception as e:
            messagebox.showerror("エラー", f"テキストファイルの保存に失敗しました。\n{e}")
            return

        messagebox.showinfo("完了", f"構造化テキストを保存しました:\n{txt_path}")
        self.set_result_text(f"構造化テキストをファイルに保存しました。\n{txt_path}")


def main():
    root = tb.Window(themename="cosmo")
    app = PDFTextInspector(root)
    root.mainloop()


if __name__ == "__main__":
    main()