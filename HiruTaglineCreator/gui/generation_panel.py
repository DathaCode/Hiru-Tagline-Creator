import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import datetime


class ProgressDialog(tk.Toplevel):
    """Modal progress bar shown while generating PNGs."""

    def __init__(self, parent, title="Generating PNGs…"):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x130")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        ttk.Label(self, text=title, font=("Arial", 11, "bold")).pack(pady=(14, 6))
        self.progress = ttk.Progressbar(self, length=360, mode='determinate')
        self.progress.pack(pady=4)
        self.status_label = ttk.Label(self, text="Preparing…")
        self.status_label.pack(pady=4)

    def update_progress(self, current, total):
        pct = int((current / max(total, 1)) * 100)
        self.progress['value'] = pct
        self.status_label.config(text=f"Generated {current} of {total} files…")
        self.update_idletasks()

    def close(self):
        self.grab_release()
        self.destroy()


class PreviewPopup(tk.Toplevel):
    """Shows a rendered PNG preview in a popup window."""

    def __init__(self, parent, title, pil_image):
        super().__init__(parent)
        self.title(f"Preview — {title}")
        self.geometry("960x580")
        self.resizable(True, True)

        self._photo = None  # prevent GC

        canvas = tk.Canvas(self, bg="black")
        canvas.pack(fill=tk.BOTH, expand=True)
        self.bind('<Configure>', lambda e: self._fit(canvas, pil_image))
        self.after(50, lambda: self._fit(canvas, pil_image))

        ttk.Button(self, text="Close", command=self.destroy).pack(pady=6)

    def _fit(self, canvas, img):
        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        if cw < 10 or ch < 10:
            return
        iw, ih = img.size
        scale = min(cw / iw, ch / ih)
        nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS
        resized = img.resize((nw, nh), resample)
        self._photo = ImageTk.PhotoImage(resized)
        canvas.delete("all")
        canvas.create_image(cw // 2, ch // 2, anchor=tk.CENTER, image=self._photo)


class GenerationPanel(ttk.LabelFrame):
    """
    Expandable panel with per-element checkboxes, preview buttons,
    warnings, progress bar, and result summary.
    """

    def __init__(self, parent, *,
                 session_mgr, text_renderer, validator,
                 get_inputs_fn, get_template_fn, get_adjustments_fn):
        super().__init__(parent, text="📸  PNG GENERATION PANEL", padding=6)

        self.session_mgr      = session_mgr
        self.text_renderer    = text_renderer
        self.validator        = validator
        self.get_inputs       = get_inputs_fn         # () -> (topic, tag_lines, white)
        self.get_template     = get_template_fn       # () -> "MAIN_TAG" | "SUB_TAG"
        self.get_adjustments  = get_adjustments_fn    # () -> dict

        self.tag_vars = []
        self.expanded = True

        # ── Header ──────────────────────────────────────────────
        hdr = ttk.Frame(self)
        hdr.pack(fill=tk.X)
        self.expand_btn = ttk.Button(hdr, text="▲ Collapse", width=12,
                                     command=self._toggle)
        self.expand_btn.pack(side=tk.RIGHT)

        # ── Collapsible content ──────────────────────────────────
        self.body = ttk.Frame(self)
        self.body.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        self._build_body()

    # ── build ────────────────────────────────────────────────────

    def _build_body(self):
        body = self.body

        # --- Topic Bed row ---
        self.topic_frame = ttk.LabelFrame(body, text="TOPIC BED (1 file)", padding=4)
        self.topic_frame.pack(fill=tk.X, pady=2)

        self.topic_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.topic_frame, text="Topic Bed",
                        variable=self.topic_var).pack(side=tk.LEFT)
        self.topic_text_lbl = ttk.Label(self.topic_frame, text="", foreground="gray")
        self.topic_text_lbl.pack(side=tk.LEFT, padx=8)
        ttk.Button(self.topic_frame, text="👁️ Preview", width=10,
                   command=lambda: self._preview('topic')).pack(side=tk.RIGHT)

        # --- TAG lines scrollable area ---
        tag_lf = ttk.LabelFrame(body, text="TAG BEDS", padding=4)
        tag_lf.pack(fill=tk.BOTH, expand=True, pady=2)

        btn_row = ttk.Frame(tag_lf)
        btn_row.pack(fill=tk.X)
        ttk.Button(btn_row, text="☑ Select All", command=self._check_all).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row, text="☐ None",       command=self._uncheck_all).pack(side=tk.LEFT, padx=3)
        self.tag_count_lbl = ttk.Label(btn_row, text="(0 lines)")
        self.tag_count_lbl.pack(side=tk.RIGHT, padx=6)

        scroll_outer = ttk.Frame(tag_lf)
        scroll_outer.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        self.tag_canvas = tk.Canvas(scroll_outer, height=150, bg="#f8f8f8",
                                    highlightthickness=0)
        sb = ttk.Scrollbar(scroll_outer, orient=tk.VERTICAL,
                           command=self.tag_canvas.yview)
        self.tag_canvas.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tag_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tag_inner = ttk.Frame(self.tag_canvas)
        self._cw = self.tag_canvas.create_window((0, 0), window=self.tag_inner,
                                                  anchor=tk.NW)
        self.tag_inner.bind('<Configure>',
                           lambda e: self.tag_canvas.configure(
                               scrollregion=self.tag_canvas.bbox(tk.ALL)))
        self.tag_canvas.bind('<Configure>',
                            lambda e: self.tag_canvas.itemconfig(
                                self._cw, width=e.width))

        # --- White Bed row ---
        white_lf = ttk.LabelFrame(body, text="WHITE BED (1 file)", padding=4)
        white_lf.pack(fill=tk.X, pady=2)

        self.white_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(white_lf, text="White Bed",
                        variable=self.white_var).pack(side=tk.LEFT)
        self.white_text_lbl = ttk.Label(white_lf, text="", foreground="gray")
        self.white_text_lbl.pack(side=tk.LEFT, padx=8)
        ttk.Button(white_lf, text="👁️ Preview", width=10,
                   command=lambda: self._preview('white')).pack(side=tk.RIGHT)

        # --- Summary ---
        sep = ttk.Separator(body, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=6)

        sum_frm = ttk.Frame(body)
        sum_frm.pack(fill=tk.X)
        self.summary_lbl = ttk.Label(sum_frm, text="SUMMARY: 0 of 0 selected",
                                     font=("Arial", 9, "bold"))
        self.summary_lbl.pack(side=tk.LEFT)
        self.output_lbl = ttk.Label(sum_frm, text="Output: —", foreground="gray")
        self.output_lbl.pack(side=tk.RIGHT)

        # --- Action buttons ---
        act = ttk.Frame(body)
        act.pack(fill=tk.X, pady=(6, 0))
        ttk.Button(act, text="📸 Generate Selected PNGs",
                   command=self._generate).pack(side=tk.LEFT, padx=4)
        ttk.Button(act, text="📂 Open Folder",
                   command=self._open_folder).pack(side=tk.LEFT, padx=4)

    # ── public API ───────────────────────────────────────────────

    def update_tag_lines(self, tag_lines):
        """Rebuild TAG checkbox list and refresh summary."""
        for w in self.tag_inner.winfo_children():
            w.destroy()
        self.tag_vars = []

        for i, line in enumerate(tag_lines):
            var = tk.BooleanVar(value=True)
            self.tag_vars.append(var)

            row = ttk.Frame(self.tag_inner)
            row.pack(fill=tk.X, padx=4, pady=1)

            ttk.Checkbutton(row, variable=var,
                            command=self._update_summary).pack(side=tk.LEFT)

            preview = line[:55] + ("…" if len(line) > 55 else "")
            ttk.Label(row, text=f"{i+1:>2}. {preview}").pack(side=tk.LEFT, padx=4)

            # Warning indicator
            valid, msg = self.validator.validate_tag_line(line)
            if msg:
                fg = "orange" if valid else "red"
                ttk.Label(row, text=f"⚠️ {msg}", foreground=fg).pack(side=tk.LEFT, padx=4)

            ttk.Button(row, text="👁️", width=3,
                       command=lambda idx=i: self._preview('tag', idx)).pack(side=tk.RIGHT)

        self.tag_count_lbl.config(text=f"({len(tag_lines)} lines)")
        self._update_summary()

    def update_text_labels(self, topic, white):
        """Update the short text previews for Topic and White beds."""
        self.topic_text_lbl.config(text=(topic[:45] + "…") if len(topic) > 45 else topic)
        self.white_text_lbl.config(text=(white[:45] + "…") if len(white) > 45 else white)

    def set_topic_visible(self, visible: bool):
        if visible:
            # Ensure it's packed at the top of the body
            self.topic_frame.pack(fill=tk.X, pady=2)
            # Move it to the front (first child)
            children = self.body.winfo_children()
            if len(children) > 1:
                self.topic_frame.pack(fill=tk.X, pady=2, before=children[1])
        else:
            self.topic_frame.pack_forget()
        self._update_summary()

    def get_selections(self):
        return {
            'topic': self.topic_var.get(),
            'white': self.white_var.get(),
            'tags':  [v.get() for v in self.tag_vars],
        }

    # ── internal ─────────────────────────────────────────────────

    def _toggle(self):
        if self.expanded:
            self.body.pack_forget()
            self.expand_btn.config(text="▼ Expand")
        else:
            self.body.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
            self.expand_btn.config(text="▲ Collapse")
        self.expanded = not self.expanded

    def _check_all(self):
        for v in self.tag_vars: v.set(True)
        self._update_summary()

    def _uncheck_all(self):
        for v in self.tag_vars: v.set(False)
        self._update_summary()

    def _update_summary(self):
        total, selected, warns = 0, 0, 0

        # Topic (only if visible)
        if self.topic_frame.winfo_manager():
            total += 1
            if self.topic_var.get(): selected += 1

        # Tags
        topic, tags, white = self.get_inputs()
        total += len(self.tag_vars)
        for i, v in enumerate(self.tag_vars):
            if v.get(): selected += 1
            if i < len(tags):
                ok, msg = self.validator.validate_tag_line(tags[i])
                if msg: warns += 1

        # White
        total += 1
        if self.white_var.get(): selected += 1

        txt = f"SUMMARY: {selected} of {total} selected"
        if warns: txt += f"  ({warns} warning{'s' if warns > 1 else ''})"
        self.summary_lbl.config(text=txt)

        path = self.session_mgr.get_session_path() or "— no session —"
        self.output_lbl.config(text=f"Output: {path}")

    # ── preview ──────────────────────────────────────────────────

    def _preview(self, kind, idx=0):
        topic, tags, white = self.get_inputs()
        template = self.get_template()
        adj      = self.get_adjustments()
        h_scale  = adj.get('h_scale', 100)
        letter_spacing = adj.get('letter_spacing', 0)

        try:
            # Load base template image for compositing
            base_img = self.text_renderer.template_mgr.get_template_image(template)

            if kind == 'topic':
                bed = self.text_renderer.template_mgr.get_bed_config(template, 'TOPIC_BED')
                text_layer = self.text_renderer.render_topic_bed(topic, bed, letter_spacing)
                title = "Topic Bed"
            elif kind == 'tag':
                if idx >= len(tags): return
                bed = self.text_renderer.template_mgr.get_bed_config(template, 'TAG_BED')
                text_layer = self.text_renderer.render_tag_bed_text(tags[idx], bed, h_scale, letter_spacing)
                title = f"TAG Line {idx + 1}"
            elif kind == 'white':
                bed = self.text_renderer.template_mgr.get_bed_config(template, 'WHITE_BED')
                text_layer = self.text_renderer.render_white_bed_text(white, bed, h_scale, letter_spacing)
                title = "White Bed"
            else:
                return

            # Composite text on template
            if base_img:
                comp = base_img.convert('RGBA')
                # Clear pre-baked topic bed red bar so dynamic sizing works
                if kind == 'topic' and bed:
                    bx, by = bed.get('x', 126), bed.get('y', 750)
                    bh = bed.get('height', 64)
                    cw = 1800  # Wide enough to erase all anti-aliased right edges
                    comp.paste(Image.new('RGBA', (cw, bh), (0,0,0,0)), (bx, by))
                img = Image.alpha_composite(comp, text_layer)
            else:
                img = text_layer

            PreviewPopup(self.winfo_toplevel(), title, img)
        except Exception as e:
            import traceback; traceback.print_exc()
            messagebox.showerror("Preview Error", str(e))

    # ── generation ───────────────────────────────────────────────

    def _generate(self):
        topic, tags, white = self.get_inputs()
        template = self.get_template()
        adj      = self.get_adjustments()

        # Validate
        all_valid, errors = self.validator.validate_all(tags, white)
        hard = [e for e in errors if "✖" in e]
        if hard:
            messagebox.showerror("Validation Error", "\n".join(hard))
            return
        if errors:
            if not messagebox.askyesno("Warnings",
                                       "\n".join(errors) + "\n\nContinue anyway?"):
                return

        session_path = self.session_mgr.get_session_path()
        if not session_path:
            messagebox.showinfo("No Session",
                                "Please create a session first (🆕 New).")
            return

        sel  = self.get_selections()
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Count how many will be generated
        total = 0
        if self.topic_frame.winfo_manager() and sel['topic'] and topic: total += 1
        total += sum(1 for i, c in enumerate(sel['tags']) if c and i < len(tags) and tags[i])
        if sel['white'] and white: total += 1

        if total == 0:
            messagebox.showwarning("Nothing Selected",
                                   "No items selected or all fields are empty.")
            return

        # Progress dialog
        prog = ProgressDialog(self.winfo_toplevel())
        generated, gen_errors = [], []
        done = 0

        # Get horizontal scale and letter spacing
        h_scale = adj.get('h_scale', 100)
        letter_spacing = adj.get('letter_spacing', 0)

        try:
            # ═══════════════════════════════════════════════
            # GENERATE TOPIC BED (MAIN TAG only)
            # ═══════════════════════════════════════════════
            if self.topic_frame.winfo_manager() and sel['topic'] and topic:
                try:
                    bed = self.text_renderer.template_mgr.get_bed_config(template, 'TOPIC_BED')
                    base_img = self.text_renderer.template_mgr.get_template_image(template)
                    text_layer = self.text_renderer.render_topic_bed(topic, bed, letter_spacing)
                    if base_img:
                        comp = base_img.convert('RGBA')
                        # Clear pre-baked topic bed red bar so dynamic sizing works
                        bx, by = bed.get('x', 126), bed.get('y', 750)
                        bh = bed.get('height', 64)
                        cw = 1800  # Wide enough to erase all anti-aliased right edges
                        comp.paste(Image.new('RGBA', (cw, bh), (0,0,0,0)), (bx, by))
                        img = Image.alpha_composite(comp, text_layer)
                    else:
                        img = text_layer
                    filename = f"TopicBed_{date}.png"
                    filepath = os.path.join(session_path, filename)
                    self.text_renderer.save_png(img, filepath)
                    generated.append(filepath)
                except Exception as e:
                    gen_errors.append(f"Topic Bed: {e}")
                done += 1
                prog.update_progress(done, total)

            # ═══════════════════════════════════════════════
            # GENERATE TAG BEDS (one per line)
            # ═══════════════════════════════════════════════
            for i, checked in enumerate(sel['tags']):
                if checked and i < len(tags) and tags[i]:
                    try:
                        line = tags[i]
                        bed = self.text_renderer.template_mgr.get_bed_config(template, 'TAG_BED')
                        # Base image not needed for TAG BED output, must be totally transparent
                        img = self.text_renderer.render_tag_bed_text(line, bed, h_scale, letter_spacing)
                        
                        # Generate filename from first 3 words
                        words = line.split()[:3]
                        prefix = '-'.join(w[:20] for w in words)
                        for ch in r'\/:*?"<>|':
                            prefix = prefix.replace(ch, '')
                        
                        filename = f"{prefix or 'Untitled'}_TAG_{date}.png"
                        filepath = os.path.join(session_path, filename)
                        self.text_renderer.save_png(img, filepath)
                        generated.append(filepath)
                    except Exception as e:
                        gen_errors.append(f"TAG {i+1}: {e}")
                    done += 1
                    prog.update_progress(done, total)

            # ═══════════════════════════════════════════════
            # GENERATE WHITE BED
            # ═══════════════════════════════════════════════
            if sel['white'] and white:
                try:
                    bed = self.text_renderer.template_mgr.get_bed_config(template, 'WHITE_BED')
                    # Base image not needed for WHITE BED output, must be totally transparent
                    img = self.text_renderer.render_white_bed_text(white, bed, h_scale, letter_spacing)
                    
                    # Generate filename
                    words = white.split()[:3]
                    prefix = '-'.join(w[:20] for w in words)
                    for ch in r'\/:*?"<>|':
                        prefix = prefix.replace(ch, '')
                        
                    filename = f"{prefix or 'Untitled'}_WhiteBed_{date}.png"
                    filepath = os.path.join(session_path, filename)
                    self.text_renderer.save_png(img, filepath)
                    generated.append(filepath)
                except Exception as e:
                    gen_errors.append(f"White Bed: {e}")
                done += 1
                prog.update_progress(done, total)
        finally:
            prog.close()

        # Result dialog
        self._show_results(generated, gen_errors, session_path)

    def _show_results(self, generated, errors, session_path):
        win = tk.Toplevel(self.winfo_toplevel())
        win.title("Generation Complete")
        win.geometry("600x420")
        win.resizable(True, True)

        head = f"✅ Generated {len(generated)} PNG file(s)"
        if errors: head += f"   ⚠️ {len(errors)} error(s)"
        ttk.Label(win, text=head, font=("Arial", 12, "bold")).pack(pady=(12, 4))
        ttk.Label(win, text=f"Saved to: {session_path}",
                  foreground="gray").pack(anchor=tk.W, padx=12)

        nb = ttk.Notebook(win)
        nb.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        # Files tab
        f_tab = ttk.Frame(nb); nb.add(f_tab, text=f"Files ({len(generated)})")
        lb = tk.Listbox(f_tab)
        for p in generated:
            lb.insert(tk.END, os.path.basename(p))
        lb.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Errors tab (if any)
        if errors:
            e_tab = ttk.Frame(nb); nb.add(e_tab, text=f"Errors ({len(errors)})")
            elb = tk.Listbox(e_tab, foreground="red")
            for em in errors:
                elb.insert(tk.END, em)
            elb.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        btn_row = ttk.Frame(win)
        btn_row.pack(fill=tk.X, pady=6, padx=12)
        ttk.Button(btn_row, text="📂 Open Folder",
                   command=lambda: os.startfile(session_path)).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_row, text="Close",
                   command=win.destroy).pack(side=tk.RIGHT, padx=4)

    def _open_folder(self):
        path = self.session_mgr.get_session_path()
        if not path:
            path = self.session_mgr.base_dir
        if path and os.path.exists(path):
            os.startfile(path)
        else:
            messagebox.showinfo("Folder", f"Path does not exist yet:\n{path}")
