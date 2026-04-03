import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图片水平镜像工具")
        self.resizable(False, False)
        self._build()

    def _build(self):
        pad = {"padx": 10, "pady": 6}

        # ── 文件输入区 ──
        file_frame = ttk.LabelFrame(self, text="输入", padding=10)
        file_frame.grid(row=0, column=0, sticky="ew", **pad)

        self.input_var = tk.StringVar()
        ttk.Label(file_frame, text="图片 / 目录", width=10, anchor="e").grid(row=0, column=0, sticky="e")
        ttk.Entry(file_frame, textvariable=self.input_var, width=46).grid(row=0, column=1, padx=4)
        ttk.Button(file_frame, text="浏览", command=self._pick_input, width=6).grid(row=0, column=2)

        # ── 开始按钮 ──
        self.btn = ttk.Button(self, text="开始处理", command=self._start)
        self.btn.grid(row=1, column=0, pady=(0, 6))

        # ── 进度条 ──
        self.progress = ttk.Progressbar(self, length=460, mode="determinate")
        self.progress.grid(row=2, column=0, padx=10, pady=(0, 4))

        # ── 日志 ──
        log_frame = ttk.LabelFrame(self, text="日志", padding=6)
        log_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.log = tk.Text(log_frame, height=10, width=62, state="disabled", wrap="word")
        sb = ttk.Scrollbar(log_frame, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        self.log.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

    def _pick_input(self):
        path = filedialog.askdirectory(title="选择图片目录")
        if not path:
            path = filedialog.askopenfilename(
                title="或选择单张图片",
                filetypes=[("图片文件", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff")]
            )
        if path:
            self.input_var.set(path)

    def _log(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _start(self):
        if not self.input_var.get().strip():
            messagebox.showwarning("缺少输入", "请先选择图片或目录。")
            return
        self.btn.configure(state="disabled")
        self.progress["value"] = 0
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        src = self.input_var.get().strip()

        if os.path.isdir(src):
            files = [f for f in os.listdir(src)
                     if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS]
            if not files:
                self._log("[错误] 目录中没有支持的图片文件。")
                self.btn.configure(state="normal")
                return
            out_dir = os.path.join(src, "mirror")
            os.makedirs(out_dir, exist_ok=True)
            self._log(f"找到 {len(files)} 张图片，输出到: {out_dir}\n")
            self.progress["maximum"] = len(files)
            for i, fname in enumerate(files, 1):
                self._mirror(os.path.join(src, fname), out_dir, i, len(files))
                self.progress["value"] = i
            self._log(f"\n全部完成，共处理 {len(files)} 张。")
        else:
            out_dir = os.path.join(os.path.dirname(src), "mirror")
            os.makedirs(out_dir, exist_ok=True)
            self.progress["maximum"] = 1
            self._mirror(src, out_dir, 1, 1)
            self.progress["value"] = 1

        self.btn.configure(state="normal")

    def _mirror(self, src_path, out_dir, idx, total):
        try:
            base, ext = os.path.splitext(os.path.basename(src_path))
            img = Image.open(src_path)
            mirrored = img.transpose(Image.FLIP_LEFT_RIGHT)
            dst = os.path.join(out_dir, f"{base}_mirror{ext}")
            mirrored.save(dst)
            self._log(f"[{idx}/{total}] ✓ {base}_mirror{ext}")
        except Exception as e:
            self._log(f"[{idx}/{total}] ✗ {os.path.basename(src_path)}: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
