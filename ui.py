import tkinter as tk
from tkcalendar import Calendar
from tkinter import simpledialog, messagebox
import datetime

from db import (
    add_schedule,
    get_schedule,
    delete_schedule,
    update_schedule
)


def create_ui():
    # ==============================
    # 기본 창 설정
    # ==============================
    root = tk.Tk()
    root.geometry("300x500+20+20")
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.configure(bg="#f5f5f5")
    root.attributes("-alpha", 0.95)   # 기본 투명도

    # ==================================================
    # STEP 4. 창 드래그 이동
    # ==================================================
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def do_move(event):
        x = root.winfo_x() + event.x - root.x
        y = root.winfo_y() + event.y - root.y
        root.geometry(f"+{x}+{y}")

    root.bind("<Button-1>", start_move)
    root.bind("<B1-Motion>", do_move)

    # ==================================================
    # STEP 7. 우클릭 메뉴
    # ==================================================
    menu = tk.Menu(root, tearoff=0)

    def hide_window():
        root.withdraw()

    def show_window(event=None):
        root.deiconify()
        root.attributes("-topmost", True)

    menu.add_command(label="숨기기", command=hide_window)
    menu.add_command(label="종료", command=root.destroy)

    root.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))
    root.bind_all("<Control-Shift-s>", show_window)

    # ==============================
    # 캘린더
    # ==============================
    cal = Calendar(
        root,
        selectmode="day",
        date_pattern="yyyy-mm-dd",
        background="#f5f5f5",
        borderwidth=0,
        headersbackground="#f5f5f5",
        normalbackground="#ffffff",
        weekendbackground="#ffffff"
    )
    cal.pack(pady=(5, 2))

    # ==================================================
    # STEP 5. 오늘 날짜 강조
    # ==================================================
    today = datetime.date.today()
    cal.selection_set(today)
    cal.tag_config("today", background="#2f80ed", foreground="white")
    cal.calevent_create(today, "TODAY", "today")

    # ==============================
    # 일정 리스트
    # ==============================
    listbox = tk.Listbox(
        root,
        height=6,
        activestyle="none",
        borderwidth=0,
        highlightthickness=0,
        selectbackground="#2f80ed",
        font=("맑은 고딕", 9)
    )
    listbox.pack(padx=10, pady=5, fill="both")

    def on_date_select(event=None):
        listbox.delete(0, tk.END)
        for s in get_schedule(cal.get_date()):
            listbox.insert(tk.END, s[0])

    cal.bind("<<CalendarSelected>>", on_date_select)

    # ==============================
    # 버튼 (미니멀)
    # ==============================
    btn_frame = tk.Frame(root, bg="#f5f5f5")
    btn_frame.pack(pady=3)

    def make_btn(text, cmd):
        return tk.Button(
            btn_frame,
            text=text,
            command=cmd,
            relief="flat",
            bg="#eaeaea",
            padx=6,
            pady=2,
            font=("맑은 고딕", 9)
        )

    make_btn("＋", lambda: add_event()).pack(side="left", padx=3)
    make_btn("✎", lambda: edit_event()).pack(side="left", padx=3)
    make_btn("🗑", lambda: delete_event()).pack(side="left", padx=3)

    # ==============================
    # 일정 함수
    # ==============================
    def add_event():
        text = simpledialog.askstring("일정 추가", "일정 입력")
        if text:
            add_schedule(cal.get_date(), text)
            on_date_select()

    def edit_event():
        if not listbox.curselection():
            return
        old = listbox.get(listbox.curselection())
        new = simpledialog.askstring("일정 수정", "내용 수정", initialvalue=old)
        if new:
            update_schedule(cal.get_date(), old, new)
            on_date_select()

    def delete_event():
        if not listbox.curselection():
            return
        if messagebox.askyesno("삭제", "정말 삭제하시겠습니까?"):
            delete_schedule(cal.get_date(), listbox.get(listbox.curselection()))
            on_date_select()

    # ==================================================
    # STEP 8. 투명도 슬라이더
    # ==================================================
    def set_alpha(value):
        root.attributes("-alpha", float(value))

    alpha = tk.Scale(
        root,
        from_=0.6,
        to=1.0,
        resolution=0.05,
        orient="horizontal",
        command=set_alpha,
        showvalue=False,
        length=260,
        troughcolor="#dddddd"
    )
    alpha.set(0.95)
    alpha.pack(pady=(2, 6))

    # ==============================
    # 시작 시
    # ==============================
    on_date_select()
    root.mainloop()
