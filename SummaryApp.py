import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import spacy
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt
import PyPDF2

# 言語モデルの初期化
nlp_ja = None
nlp_en = None

# 多言語対応のための辞書
translations = {
    'ja': {
        'title': "文書要約アプリケーション",
        'file_select': "ファイルを選択:",
        'browse': "参照",
        'num_sentences': "要約文の数:",
        'language': "言語:",
        'japanese': "日本語",
        'english': "英語",
        'summarize': "要約開始",
        'copy': "コピー",
        'save': "保存",
        'summary_result': "要約結果:",
        'file_warning': "ファイルを選択してください。",
        'copy_success': "要約がクリップボードにコピーされました!",
        'save_success': "要約が {file_path} に保存されました。",
        'save_warning': "保存する要約がありません。",
        'model_error': "言語モデルのロードに失敗しました。インストールされているか確認してください。"
    },
    'en': {
        'title': "Document Summarization App",
        'file_select': "Select a file:",
        'browse': "Browse",
        'num_sentences': "Number of sentences:",
        'language': "Language:",
        'japanese': "Japanese",
        'english': "English",
        'summarize': "Summarize",
        'copy': "Copy",
        'save': "Save",
        'summary_result': "Summary result:",
        'file_warning': "Please select a file.",
        'copy_success': "Summary copied to clipboard!",
        'save_success': "Summary saved to {file_path}.",
        'save_warning': "No summary to save.",
        'model_error': "Failed to load language model. Please check if it's installed."
    }
}

def load_language_model(lang):
    global nlp_ja, nlp_en
    if lang == 'ja' and nlp_ja is None:
        try:
            nlp_ja = spacy.load("ja_core_news_sm")
        except:
            messagebox.showerror("Error", translations[lang]['model_error'])
            return None
    elif lang == 'en' and nlp_en is None:
        try:
            nlp_en = spacy.load("en_core_web_sm")
        except:
            messagebox.showerror("Error", translations[lang]['model_error'])
            return None
    return nlp_ja if lang == 'ja' else nlp_en

def textrank_summarize(text, num_sentences, lang):
    nlp = load_language_model(lang)
    if nlp is None:
        return "言語モデルのロードに失敗しました。"
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    similarity_matrix = calculate_similarity_matrix(sentences)
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    summary = [ranked_sentences[i][1] for i in range(min(num_sentences, len(ranked_sentences)))]
    return " ".join(summary)

def calculate_similarity_matrix(sentences):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(sentences)
    return cosine_similarity(tfidf_matrix)

def read_file(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return ' '.join([page.extract_text() for page in pdf_reader.pages])
    else:
        return "Unsupported file format."

class SummarizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(translations['ja']['title'])
        self.geometry("800x600")
        self.lang = 'ja'
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ファイル選択
        ttk.Label(main_frame, text=translations[self.lang]['file_select']).grid(column=0, row=0, sticky=tk.W, pady=5)
        self.file_entry = ttk.Entry(main_frame, width=50)
        self.file_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text=translations[self.lang]['browse'], command=self.browse_file).grid(column=2, row=0, sticky=tk.W)

        # 要約文の数
        ttk.Label(main_frame, text=translations[self.lang]['num_sentences']).grid(column=0, row=1, sticky=tk.W, pady=5)
        self.num_sentences = ttk.Scale(main_frame, from_=1, to=10, orient=tk.HORIZONTAL, length=200)
        self.num_sentences.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

        # 言語選択
        ttk.Label(main_frame, text=translations[self.lang]['language']).grid(column=0, row=2, sticky=tk.W, pady=5)
        self.lang_var = tk.StringVar(value="ja")
        ttk.Radiobutton(main_frame, text=translations[self.lang]['japanese'], variable=self.lang_var, value="ja").grid(column=1, row=2, sticky=tk.W)
        ttk.Radiobutton(main_frame, text=translations[self.lang]['english'], variable=self.lang_var, value="en").grid(column=1, row=2, sticky=tk.E)

        # ボタン
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(column=0, row=3, columnspan=3, pady=10)
        ttk.Button(button_frame, text=translations[self.lang]['summarize'], command=self.summarize).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=translations[self.lang]['copy'], command=self.copy_summary).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=translations[self.lang]['save'], command=self.save_summary).pack(side=tk.LEFT, padx=5)

        # 出力エリア
        self.output_text = tk.Text(main_frame, height=20, width=80)
        self.output_text.grid(column=0, row=4, columnspan=3, pady=10)

        # プログレスバー
        self.progress = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress.grid(column=0, row=5, columnspan=3, pady=10)

        # 言語切り替えボタン
        ttk.Button(main_frame, text="Switch to English", command=self.switch_language).grid(column=2, row=6, sticky=tk.E)

    def switch_language(self):
        self.lang = 'en' if self.lang == 'ja' else 'ja'
        self.title(translations[self.lang]['title'])
        self.update_widgets()

    def update_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Files", "*.docx"), ("PDF Files", "*.pdf")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def summarize(self):
        file_path = self.file_entry.get()
        num_sentences = self.num_sentences.get()
        lang = self.lang_var.get()

        if not file_path:
            messagebox.showwarning("警告", "ファイルを選択してください。")
            return

        text = read_file(file_path)
        self.progress['value'] = 0
        self.update_idletasks()

        for i in range(101):
            self.progress['value'] = i
            self.update_idletasks()
            if i % 10 == 0:
                self.update()

        summary = textrank_summarize(text, num_sentences, lang)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"要約結果:\n{summary}")
        self.progress['value'] = 100

    def copy_summary(self):
        summary = self.output_text.get(1.0, tk.END)
        self.clipboard_clear()
        self.clipboard_append(summary)
        messagebox.showinfo("情報", "要約がクリップボードにコピーされました!")

    def save_summary(self):
        summary = self.output_text.get(1.0, tk.END)
        if summary.strip():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(summary)
                messagebox.showinfo("情報", f"要約が {file_path} に保存されました。")
        else:
            messagebox.showwarning("警告", "保存する要約がありません。")

if __name__ == '__main__':
    app = SummarizerApp()
    app.mainloop()
