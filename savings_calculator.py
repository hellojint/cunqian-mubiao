# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import scrolledtext
import math

BG_BLUE = "#1a3a5c"
BG_BLUE_LIGHT = "#2a5a8c"
GREEN_ACCENT = "#4caf50"
GREEN_LIGHT = "#81c784"
GREEN_DARK = "#388e3c"
TEXT_WHITE = "#ffffff"
CHAT_BG = "#e8f5e9"
ENTRY_BG = "#ffffff"


def calculate(salary):
    if salary <= 3000:
        return 0, 0.0, "low"
    elif salary <= 6000:
        savings = max(1000, salary * 0.35)
        ratio = savings / salary * 100
        return savings, ratio, "mid"
    elif salary <= 10000:
        keep = 2750
        savings = min(salary - keep, salary * 0.5)
        ratio = savings / salary * 100
        return savings, ratio, "high"
    else:
        keep = 5000
        savings = min(salary - keep, salary * 0.5)
        ratio = savings / salary * 100
        return savings, ratio, "top"


class GoalWindow:
    def __init__(self, parent, monthly_savings, salary):
        self.monthly_savings = monthly_savings
        self.salary = salary
        self.win = tk.Toplevel(parent)
        self.win.title("目标差距计算")
        self.win.geometry("420x580")
        self.win.resizable(False, False)
        self.win.configure(bg=BG_BLUE)
        self.win.grab_set()

        tk.Label(
            self.win, text="目标差距",
            font=("Microsoft YaHei", 18, "bold"),
            bg=BG_BLUE, fg=GREEN_LIGHT
        ).pack(pady=(18, 4))

        tk.Label(
            self.win, text=f"月工资：{salary:.0f} 元   每月可存：{monthly_savings:.0f} 元",
            font=("Microsoft YaHei", 11),
            bg=BG_BLUE, fg="#aaddaa"
        ).pack(pady=(0, 14))

        content = tk.Frame(self.win, bg=CHAT_BG, padx=20, pady=16)
        content.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        # 目标金额
        tk.Label(content, text="目标金额（元）：",
                 font=("Microsoft YaHei", 11), bg=CHAT_BG, fg=BG_BLUE, anchor="w"
                 ).pack(fill=tk.X, pady=(0, 4))

        self.goal_entry = tk.Entry(
            content, font=("Microsoft YaHei", 13),
            bg=ENTRY_BG, fg="#333333", insertbackground="#333333",
            relief=tk.FLAT, highlightthickness=2,
            highlightcolor=GREEN_ACCENT, highlightbackground="#cccccc"
        )
        self.goal_entry.pack(fill=tk.X, ipady=5, pady=(0, 12))

        # 期望月数
        tk.Label(content, text="期望在几个月内达成（可选）：",
                 font=("Microsoft YaHei", 11), bg=CHAT_BG, fg=BG_BLUE, anchor="w"
                 ).pack(fill=tk.X, pady=(0, 4))

        months_frame = tk.Frame(content, bg=CHAT_BG)
        months_frame.pack(fill=tk.X, pady=(0, 14))

        self.months_entry = tk.Entry(
            months_frame, font=("Microsoft YaHei", 13),
            bg=ENTRY_BG, fg="#333333", insertbackground="#333333",
            relief=tk.FLAT, highlightthickness=2,
            highlightcolor=GREEN_ACCENT, highlightbackground="#cccccc"
        )
        self.months_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=5)
        self.months_entry.bind("<Return>", lambda _: self.calc_goal())

        tk.Button(
            months_frame, text="计算",
            font=("Microsoft YaHei", 11, "bold"),
            command=self.calc_goal, width=6,
            bg=GREEN_ACCENT, fg=TEXT_WHITE,
            activebackground=GREEN_DARK, activeforeground=TEXT_WHITE,
            relief=tk.FLAT, cursor="hand2"
        ).pack(side=tk.RIGHT, ipady=3)

        self.result_area = scrolledtext.ScrolledText(
            content, wrap=tk.WORD, font=("Microsoft YaHei", 11),
            state=tk.DISABLED, bg="#f0faf0", fg=BG_BLUE,
            relief=tk.FLAT, highlightthickness=1, highlightbackground=GREEN_ACCENT,
            padx=10, pady=10, height=10
        )
        self.result_area.pack(fill=tk.BOTH, expand=True)

        self.goal_entry.focus_force()

    def calc_goal(self):
        self.result_area.config(state=tk.NORMAL)
        self.result_area.delete("1.0", tk.END)

        try:
            goal = float(self.goal_entry.get().strip())
        except ValueError:
            self.result_area.insert(tk.END, "请输入有效的目标金额哦～")
            self.result_area.config(state=tk.DISABLED)
            return

        if goal <= 0:
            self.result_area.insert(tk.END, "目标金额需要大于 0 哦～")
            self.result_area.config(state=tk.DISABLED)
            return

        months_raw = self.months_entry.get().strip()
        lines = []

        if months_raw:
            # 有期望月数 → 反推每月需存金额和占比
            try:
                target_months = int(months_raw)
            except ValueError:
                self.result_area.insert(tk.END, "期望月数请输入整数哦～")
                self.result_area.config(state=tk.DISABLED)
                return

            if target_months <= 0:
                self.result_area.insert(tk.END, "期望月数需要大于 0 哦～")
                self.result_area.config(state=tk.DISABLED)
                return

            needed = goal / target_months
            ratio = needed / self.salary * 100 if self.salary > 0 else 0
            remain = self.salary - needed

            lines = [
                f"目标金额：{goal:.0f} 元",
                f"期望达成：{target_months} 个月",
                "─" * 28,
                f"每月需存：{needed:.0f} 元",
                f"占工资比例：{ratio:.1f}%",
                f"每月剩余可用：{remain:.0f} 元",
                "─" * 28,
            ]

            if remain < 0:
                lines.append("每月剩余为负，目标月数太短，建议延长期限。")
            elif ratio > 50:
                lines.append(f"所需比例 {ratio:.1f}% 超过 50% 上限，建议延长期限。")
            elif ratio > 40:
                lines.append(f"所需比例较高（{ratio:.1f}%），请量力而行～")
            else:
                years = target_months // 12
                rem = target_months % 12
                if years > 0 and rem > 0:
                    t = f"{years} 年 {rem} 个月"
                elif years > 0:
                    t = f"{years} 年"
                else:
                    t = f"{target_months} 个月"
                lines.append(f"目标可达成！计划存期：{t}，加油！")
        else:
            # 没有期望月数 → 用当前存钱金额正推需要多久
            if self.monthly_savings <= 0:
                self.result_area.insert(tk.END, "当前每月存钱金额为 0，无法计算达成时间。\n建议先增加收入哦～")
                self.result_area.config(state=tk.DISABLED)
                return

            months = math.ceil(goal / self.monthly_savings)
            years = months // 12
            rem = months % 12
            if years > 0 and rem > 0:
                time_str = f"{years} 年 {rem} 个月"
            elif years > 0:
                time_str = f"{years} 年"
            else:
                time_str = f"{months} 个月"

            lines = [
                f"目标金额：{goal:.0f} 元",
                f"每月存入：{self.monthly_savings:.0f} 元",
                "─" * 28,
                f"需要时间：{time_str}（共 {months} 个月）",
                "",
            ]
            if months <= 6:
                lines.append("目标很近，加油冲！")
            elif months <= 12:
                lines.append("不到一年就能达成，坚持住！")
            elif months <= 36:
                lines.append("3 年内可达成，稳步前行～")
            else:
                lines.append("目标较长远，持续坚持是关键！")

        self.result_area.insert(tk.END, "\n".join(lines))
        self.result_area.config(state=tk.DISABLED)


class SavingsCalculator:
    def __init__(self):
        self.last_savings = 0.0
        self.last_salary = 0.0
        self.root = tk.Tk()
        self.root.title("存钱计算器")
        self.root.geometry("500x620")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_BLUE)

        tk.Label(
            self.root, text="存钱计算器",
            font=("Microsoft YaHei", 20, "bold"),
            bg=BG_BLUE, fg=GREEN_LIGHT
        ).pack(side=tk.TOP, pady=(15, 5))

        tk.Label(
            self.root, text="智能储蓄小助手",
            font=("Microsoft YaHei", 10),
            bg=BG_BLUE, fg="#aaaaaa"
        ).pack(side=tk.TOP, pady=(0, 10))

        bottom_frame = tk.Frame(self.root, bg=BG_BLUE_LIGHT, pady=10, padx=10)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        btn_row = tk.Frame(bottom_frame, bg=BG_BLUE_LIGHT)
        btn_row.pack(side=tk.BOTTOM, pady=(8, 0))

        tk.Button(
            btn_row, text="重新计算",
            font=("Microsoft YaHei", 10, "bold"),
            command=self.reset,
            bg=GREEN_DARK, fg=TEXT_WHITE,
            activebackground=GREEN_ACCENT, activeforeground=TEXT_WHITE,
            relief=tk.FLAT, cursor="hand2", padx=15, pady=3
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.goal_btn = tk.Button(
            btn_row, text="目标差距",
            font=("Microsoft YaHei", 10, "bold"),
            command=self.open_goal_window,
            bg=BG_BLUE, fg=GREEN_LIGHT,
            activebackground=BG_BLUE_LIGHT, activeforeground=GREEN_ACCENT,
            relief=tk.FLAT, cursor="hand2", padx=15, pady=3,
            state=tk.DISABLED
        )
        self.goal_btn.pack(side=tk.LEFT)

        input_frame = tk.Frame(bottom_frame, bg=BG_BLUE_LIGHT)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.input_entry = tk.Entry(
            input_frame, font=("Microsoft YaHei", 12),
            bg=ENTRY_BG, fg="#333333", insertbackground="#333333",
            relief=tk.FLAT, highlightthickness=2,
            highlightcolor=GREEN_ACCENT, highlightbackground="#cccccc"
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=5)
        self.input_entry.bind("<Return>", lambda e: self.on_submit())

        tk.Button(
            input_frame, text="发送",
            font=("Microsoft YaHei", 11, "bold"),
            command=self.on_submit, width=6,
            bg=GREEN_ACCENT, fg=TEXT_WHITE,
            activebackground=GREEN_DARK, activeforeground=TEXT_WHITE,
            relief=tk.FLAT, cursor="hand2"
        ).pack(side=tk.RIGHT, ipady=3)

        chat_frame = tk.Frame(self.root, bg=BG_BLUE, padx=10, pady=5)
        chat_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.chat_area = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, font=("Microsoft YaHei", 11),
            state=tk.DISABLED, bg=CHAT_BG, fg="#1a3a5c",
            relief=tk.FLAT, highlightthickness=1, highlightbackground=GREEN_ACCENT,
            padx=10, pady=10
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        self.add_message("助手", "你好！我是存钱计算小助手～")
        self.add_message("助手", "请输入你的月工资收入（元）：")
        self.input_entry.focus_force()

    def add_message(self, sender, text):
        self.chat_area.config(state=tk.NORMAL)
        prefix = "\U0001f4ac" if sender == "助手" else "\U0001f464"
        self.chat_area.insert(tk.END, f" {prefix} 【{sender}】{text}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def on_submit(self):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        self.input_entry.delete(0, tk.END)
        self.add_message("你", user_input)

        try:
            salary = float(user_input)
        except ValueError:
            self.add_message("助手", "请输入有效的数字金额哦～")
            return

        if salary <= 0:
            self.add_message("助手", "工资金额需要大于0哦～")
            return

        savings, ratio, tier = calculate(salary)
        self.last_savings = savings
        self.last_salary = salary

        if tier == "low":
            self.add_message("助手",
                f"你的月工资为 {salary:.0f} 元，≤ 3000 元，统一按 1000 元计算。\n"
                f"当前收入较低，建议先保证基本生活开销，有余力再考虑存钱～"
            )
            self.goal_btn.config(state=tk.DISABLED)
        elif tier == "mid":
            self.add_message("助手",
                f"你的月工资为 {salary:.0f} 元（区间：3000-6000）\n"
                f"{'─' * 30}\n"
                f"存钱比例上限：35%（最低 1000 元）\n"
                f"建议每月存钱：{savings:.0f} 元\n"
                f"存钱占比：{ratio:.1f}%\n"
                f"每月剩余可用：{salary - savings:.0f} 元\n"
                f"{'─' * 30}"
            )
            self.goal_btn.config(state=tk.NORMAL)
        elif tier == "high":
            self.add_message("助手",
                f"你的月工资为 {salary:.0f} 元（区间：6000-10000）\n"
                f"{'─' * 30}\n"
                f"最低保留资金：2750 元\n"
                f"建议每月存钱：{savings:.0f} 元\n"
                f"存钱占比：{ratio:.1f}%\n"
                f"每月剩余可用：{salary - savings:.0f} 元\n"
                f"{'─' * 30}"
            )
            self.goal_btn.config(state=tk.NORMAL)
        else:
            self.add_message("助手",
                f"你的月工资为 {salary:.0f} 元（区间：10000以上）\n"
                f"{'─' * 30}\n"
                f"最低保留资金：5000 元\n"
                f"建议每月存钱：{savings:.0f} 元\n"
                f"存钱占比：{ratio:.1f}%\n"
                f"每月剩余可用：{salary - savings:.0f} 元\n"
                f"{'─' * 30}"
            )
            self.goal_btn.config(state=tk.NORMAL)

        self.add_message("助手", "如需重新计算，请直接输入新的工资金额，或点击【重新计算】按钮。\n计算完成后可点击【目标差距】设定存钱目标。")

    def open_goal_window(self):
        GoalWindow(self.root, self.last_savings, self.last_salary)

    def reset(self):
        self.last_savings = 0.0
        self.last_salary = 0.0
        self.goal_btn.config(state=tk.DISABLED)
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.config(state=tk.DISABLED)
        self.add_message("助手", "你好！我是存钱计算小助手～")
        self.add_message("助手", "请输入你的月工资收入（元）：")
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_force()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SavingsCalculator()
    app.run()
