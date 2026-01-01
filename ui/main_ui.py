# ui/main_ui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

from core.parser import parse_qsfs
from core.calculate import (
    qsfs_add, qsfs_mul,
    qsfs_coe, qsfs_pow
)
from core.defuzzify import qsfs_def
from core.aggregate import qsfs_agg, qsfs_aggw

from PIL import Image, ImageTk
from core.resource import resource_path

# ======================================================
# Formula image helper
# ======================================================
_formula_cache = {}

def add_formula_image(parent, img_path, width=360):
    img = Image.open(resource_path(img_path))
    w, h = img.size
    scale = width / w
    img = img.resize((int(w * scale), int(h * scale)))
    photo = ImageTk.PhotoImage(img)
    _formula_cache[img_path] = photo
    lbl = tk.Label(parent, image=photo)
    lbl.pack(pady=8)

# ======================================================
# Main App
# ======================================================
def start_app():
    root = tk.Tk()
    root.title("Quantum Spherical Fuzzy Set Tool")
    root.geometry("1100x750")

    style = ttk.Style(root)
    style.configure("TNotebook.Tab", font=("Segoe UI", 11), padding=[14, 8])
    style.configure("TButton", font=("Segoe UI", 10))

    nb = ttk.Notebook(root)
    nb.pack(expand=True, fill="both")

    # ==================================================
    # Binary operation tab (SUM, MUL)
    # ==================================================
    def binary_tab(title, func, formula_img):
        tab = ttk.Frame(nb)
        nb.add(tab, text=title)

        add_formula_image(tab, formula_img)

        f = tk.Frame(tab)
        f.pack(pady=20)

        tk.Label(f, text="QSFS A").grid(row=0, column=0, sticky="e")
        ea = tk.Entry(f, width=55)
        ea.grid(row=0, column=1, padx=10)

        tk.Label(f, text="QSFS B").grid(row=1, column=0, sticky="e")
        eb = tk.Entry(f, width=55)
        eb.grid(row=1, column=1, padx=10)

        er = tk.Entry(f, width=65)
        er.grid(row=3, column=0, columnspan=2, pady=15)

        def calc():
            try:
                A = parse_qsfs(ea.get())
                B = parse_qsfs(eb.get())
                er.delete(0, tk.END)
                er.insert(0, str(func(A, B)))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(f, text="Calculate", command=calc)\
            .grid(row=2, column=1, pady=10)

    # ==================================================
    # COE / POW tab
    # ==================================================
    def eps_tab(title, func, formula_img):
        tab = ttk.Frame(nb)
        nb.add(tab, text=title)

        add_formula_image(tab, formula_img)

        f = tk.Frame(tab)
        f.pack(pady=20)

        tk.Label(f, text="QSFS").grid(row=0, column=0, sticky="e")
        en = tk.Entry(f, width=55)
        en.grid(row=0, column=1, padx=10)

        tk.Label(f, text="λ").grid(row=1, column=0, sticky="e")
        ee = tk.Entry(f, width=10)
        ee.grid(row=1, column=1, sticky="w")

        er = tk.Entry(f, width=65)
        er.grid(row=3, column=0, columnspan=2, pady=15)

        def calc():
            try:
                nz = parse_qsfs(en.get())
                lmb = float(ee.get())
                er.delete(0, tk.END)
                er.insert(0, str(func(nz, lmb)))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(f, text="Calculate", command=calc)\
            .grid(row=2, column=1, pady=10)

    # ==================================================
    # DEF tab
    # ==================================================
    tab_def = ttk.Frame(nb)
    nb.add(tab_def, text="DEF")
    add_formula_image(tab_def, "assets/def.png")

    f = tk.Frame(tab_def)
    f.pack(pady=30)

    tk.Label(f, text="QSFS").grid(row=0, column=0, sticky="e")
    en = tk.Entry(f, width=55)
    en.grid(row=0, column=1, padx=10)

    res_lbl = tk.Label(f, text="—", font=("Segoe UI", 13, "bold"))
    res_lbl.grid(row=3, column=0, columnspan=2, pady=10)

    def calc_def():
        try:
            nz = parse_qsfs(en.get())
            res_lbl.config(text=f"DEF = {qsfs_def(nz):.5f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(f, text="Calculate", command=calc_def)\
        .grid(row=1, column=1, pady=10)

    # ==================================================
    # AGG / AGGW (manual list + Excel import)
    # ==================================================
    def aggregation_tab(title, weighted=False):
        tab = ttk.Frame(nb)
        nb.add(tab, text=title)

        # ---- formula image (smaller for AGG/AGGW) ----
        add_formula_image(
            tab,
            "assets/aggw.png" if weighted else "assets/agg.png",
            width=360
        )

        # ==================================================
        # DATA
        # ==================================================
        if weighted:
            items = []          # [(QSFSNumber, weight)]
        else:
            items = []          # [QSFSNumber]

        # ==================================================
        # TABLE
        # ==================================================
        if weighted:
            tree = ttk.Treeview(
                tab,
                columns=("qsfs", "w"),
                show="headings",
                height=15
            )
            tree.heading("qsfs", text="QSFS")
            tree.heading("w", text="Weight")
            tree.column("qsfs", width=650)
            tree.column("w", width=100, anchor="center")
        else:
            tree = ttk.Treeview(
                tab,
                columns=("qsfs",),
                show="headings",
                height=15
            )
            tree.heading("qsfs", text="QSFS")
            tree.column("qsfs", width=780)

        tree.pack(padx=15, pady=15, fill="x")

        # ==================================================
        # CONTROLS
        # ==================================================
        ctrl = tk.Frame(tab)
        ctrl.pack(pady=8)

        e_q = tk.Entry(ctrl, width=70)
        e_q.pack(side="left", padx=5)

        if weighted:
            e_w = tk.Entry(ctrl, width=8)
            e_w.pack(side="left", padx=5)

        # ==================================================
        # REFRESH FUNCTIONS
        # ==================================================
        def refresh_agg():
            tree.delete(*tree.get_children())
            if not items:
                return
            for q in items:
                tree.insert("", "end", values=(str(q),))

        def refresh_aggw():
            tree.delete(*tree.get_children())
            if not items:
                return

            total = sum(w for _, w in items)
            for q, w in items:
                nw = w / total if total != 0 else 0
                tree.insert("", "end", values=(str(q), round(nw, 5)))

        # ==================================================
        # ADD / DELETE
        # ==================================================
        def add_item():
            try:
                q = parse_qsfs(e_q.get())
                if weighted:
                    w = float(e_w.get())
                    items.append((q, w))
                    refresh_aggw()
                else:
                    items.append(q)
                    refresh_agg()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def delete_item():
            sel = tree.selection()
            if not sel:
                return
            idx = tree.index(sel[0])
            items.pop(idx)
            if weighted:
                refresh_aggw()
            else:
                refresh_agg()

        # ==================================================
        # IMPORT EXCEL
        # ==================================================
        def import_excel():
            path = filedialog.askopenfilename(
                filetypes=[("Excel", "*.xlsx *.xls")]
            )
            if not path:
                return

            try:
                df = pd.read_excel(path, header=None)
                items.clear()

                if weighted:
                    # template aggw.xlsx: QSFS | Weight
                    for _, row in df.iterrows():
                        if pd.isna(row[0]) or pd.isna(row[1]):
                            continue
                        q = parse_qsfs(str(row[0]))
                        w = float(row[1])
                        items.append((q, w))
                    refresh_aggw()
                else:
                    # template agg.xlsx: QSFS only
                    for _, row in df.iterrows():
                        if pd.isna(row[0]):
                            continue
                        q = parse_qsfs(str(row[0]))
                        items.append(q)
                    refresh_agg()

            except Exception as e:
                messagebox.showerror("Excel import error", str(e))

        # ==================================================
        # BUTTONS
        # ==================================================
        tk.Button(ctrl, text="Add", command=add_item).pack(side="left", padx=5)
        tk.Button(ctrl, text="Delete", command=delete_item).pack(side="left", padx=5)
        tk.Button(ctrl, text="Import Excel", command=import_excel)\
            .pack(side="left", padx=5)

        # ==================================================
        # RESULT
        # ==================================================
        res_entry = tk.Entry(tab, width=75)
        res_entry.pack(pady=10)

        def aggregate():
            if not items:
                return

            if weighted:
                qs = [q for q, _ in items]
                ws = [w for _, w in items]
                s = sum(ws)
                ws = [w / s for w in ws]
                res = qsfs_aggw(qs, ws)
            else:
                res = qsfs_agg(items)

            res_entry.delete(0, tk.END)
            res_entry.insert(0, str(res))

        tk.Button(tab, text="Aggregate", command=aggregate).pack(pady=5)


    # ==================================================
    # Register Tabs
    # ==================================================
    binary_tab("SUM", qsfs_add, "assets/add.png")
    binary_tab("MUL", qsfs_mul, "assets/mul.png")
    eps_tab("COE", qsfs_coe, "assets/coe.png")
    eps_tab("POW", qsfs_pow, "assets/pow.png")

    aggregation_tab("AGG", weighted=False)
    aggregation_tab("AGGW", weighted=True)

    # ==================================================
    # MULTI-SHEET TAB (Excel – core feature)
    # ==================================================
    tab_ms = ttk.Frame(nb)
    nb.add(tab_ms, text="MULTI-SHEET")

    excel_ctx = {
        "xls": None,
        "ans_sheets": [],
        "weights": [],
        "result": None,
        "row_names": [],
        "col_names": []
    }
    

    def import_excel():
        path = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx *.xls")]
        )
        if not path:
            return

        excel_ctx["xls"] = pd.ExcelFile(path)
        excel_ctx["ans_sheets"] = [
            s for s in excel_ctx["xls"].sheet_names
            if s.lower().startswith("ans")
        ]

        if not excel_ctx["ans_sheets"]:
            messagebox.showerror("Error", "No Ans* sheet found")
            return

        if "Weight" in excel_ctx["xls"].sheet_names:
            wdf = pd.read_excel(excel_ctx["xls"], "Weight", header=None)
            ws = wdf.iloc[:len(excel_ctx["ans_sheets"]), 0].astype(float).tolist()
        else:
            ws = [1.0] * len(excel_ctx["ans_sheets"])

        s = sum(ws)
        excel_ctx["weights"] = [w / s for w in ws]

        sheet_cb["values"] = excel_ctx["ans_sheets"]
        sheet_var.set(excel_ctx["ans_sheets"][0])
        load_preview(sheet_var.get())

    def load_preview(sheet):
        df = pd.read_excel(excel_ctx["xls"], sheet, header=None)
        preview.delete(*preview.get_children())
        preview["columns"] = list(range(df.shape[1]))

        for c in range(df.shape[1]):
            preview.heading(c, text=str(df.iloc[0, c]))
            preview.column(c, width=150)

        for i in range(1, df.shape[0]):
            preview.insert("", "end", values=df.iloc[i].tolist())

    def export_excel():
        if excel_ctx["result"] is None:
            messagebox.showerror("Error", "No result to export")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")]
        )
        if not path:
            return

        try:
            with pd.ExcelWriter(path, engine="openpyxl") as writer:

                # ---------- Result sheet ----------
                res_df = pd.DataFrame(
                    excel_ctx["result"],
                    index=excel_ctx["row_names"],
                    columns=excel_ctx["col_names"]
                )
                res_df.to_excel(writer, sheet_name="Result")

                # ---------- Weight sheet ----------
                w_df = pd.DataFrame({
                    "Sheet": excel_ctx["ans_sheets"],
                    "Weight": excel_ctx["weights"]
                })
                w_df.to_excel(writer, sheet_name="Weight", index=False)

            messagebox.showinfo("Export", "Export completed successfully")

        except Exception as e:
            messagebox.showerror("Export error", str(e))


    def aggregate_ms():
        matrices = [
            pd.read_excel(excel_ctx["xls"], s, header=None)
            for s in excel_ctx["ans_sheets"]
        ]

        base = matrices[0]
        rows, cols = base.shape

        excel_ctx["row_names"] = base.iloc[1:, 0].tolist()
        excel_ctx["col_names"] = base.iloc[0, 1:].tolist()

        result = [[None] * (cols - 1) for _ in range(rows - 1)]

        for i in range(1, rows):
            for j in range(1, cols):
                qs = [parse_qsfs(str(m.iloc[i, j])) for m in matrices]
                result[i - 1][j - 1] = str(
                    qsfs_aggw(qs, excel_ctx["weights"])
                )

        excel_ctx["result"] = result

        result_tree.delete(*result_tree.get_children())
        result_tree["columns"] = ["row"] + list(range(len(excel_ctx["col_names"])))

        result_tree.heading("row", text="")
        result_tree.column("row", width=120)

        for i, c in enumerate(excel_ctx["col_names"]):
            result_tree.heading(i, text=c)
            result_tree.column(i, width=170)

        for r, rn in enumerate(excel_ctx["row_names"]):
            result_tree.insert("", "end", values=[rn] + result[r])

    def delete_current_sheet():
        if not excel_ctx["ans_sheets"]:
            return

        name = sheet_var.get()
        if name not in excel_ctx["ans_sheets"]:
            return

        idx = excel_ctx["ans_sheets"].index(name)

        # Remove sheet + weight
        excel_ctx["ans_sheets"].pop(idx)
        excel_ctx["weights"].pop(idx)

        if not excel_ctx["ans_sheets"]:
            # Reset UI if no sheet left
            sheet_cb["values"] = []
            sheet_var.set("")
            weight_var.set("—")
            preview.delete(*preview.get_children())
            result_tree.delete(*result_tree.get_children())
            excel_ctx["result"] = None
            return

        # Re-normalize weights
        s = sum(excel_ctx["weights"])
        excel_ctx["weights"] = [w / s for w in excel_ctx["weights"]]

        # Update combobox
        sheet_cb["values"] = excel_ctx["ans_sheets"]
        sheet_var.set(excel_ctx["ans_sheets"][0])

        # Refresh preview + weight display
        on_sheet_change()


    # UI
    top = tk.Frame(tab_ms)
    top.pack(fill="x", pady=5)

    tk.Label(top, text="Weight").pack(side="left", padx=(15, 2))

    weight_var = tk.StringVar(value="—")
    weight_entry = tk.Entry(
        top,
        textvariable=weight_var,
        width=8,
        state="readonly",
        justify="center"
    )
    weight_entry.pack(side="left", padx=5)

    tk.Button(top, text="Import Excel", command=import_excel)\
        .pack(side="left", padx=5)

    sheet_var = tk.StringVar()
    sheet_cb = ttk.Combobox(top, textvariable=sheet_var, state="readonly", width=18)
    sheet_cb.pack(side="left", padx=5)
    def on_sheet_change(event=None):
        name = sheet_var.get()
        load_preview(name)

        if name in excel_ctx["ans_sheets"]:
            idx = excel_ctx["ans_sheets"].index(name)
            w = excel_ctx["weights"][idx]
            weight_var.set(f"{w:.5f}")
        else:
            weight_var.set("—")

    sheet_cb.bind("<<ComboboxSelected>>", on_sheet_change)

    tk.Button(
        top,
        text="Delete Sheet",
        command=delete_current_sheet
    ).pack(side="left", padx=5)

    tk.Button(top, text="Aggregate", command=aggregate_ms)\
        .pack(side="left", padx=10)
    
    tk.Button(top, text="Export Excel", command=export_excel)\
        .pack(side="left", padx=5)
    

    preview = ttk.Treeview(tab_ms, show="headings", height=7)
    preview.pack(fill="both", expand=True, padx=10, pady=5)

    result_tree = ttk.Treeview(tab_ms, show="headings", height=8)
    result_tree.pack(fill="both", expand=True, padx=10, pady=5)

    root.mainloop()
