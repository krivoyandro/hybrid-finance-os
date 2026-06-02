"""Hybrid Finance OS v0.2.0 — финансовая экосистема трейдера."""

import json
import math
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")


def calculate(balance: float, profit: float, withdraw: float) -> dict:
    """Рассчитать рост, новый баланс, риски и статус."""
    growth = profit - withdraw
    new_balance = balance + growth

    if growth > 0.01:
        status = "📈 Растёшь"
    elif abs(growth) < 0.01:
        status = "⏸ Стоишь"
    else:
        status = "🔻 Проедаешь"

    return {
        "balance": balance,
        "profit": profit,
        "withdraw": withdraw,
        "growth": growth,
        "new_balance": new_balance,
        "status": status,
        "risk_1": new_balance * 0.01,
        "risk_2": new_balance * 0.02,
        "risk_5": new_balance * 0.05,
    }


def summary(data: dict) -> str:
    """Короткий вывод."""
    lines = [
        "═══════════════════════════════════════",
        "       Hybrid Finance OS v0.2.0",
        "═══════════════════════════════════════",
        f"  Баланс:          ${data['balance']:,.2f}",
        f"  Прибыль:         ${data['profit']:,.2f}",
        f"  Вывод (жизнь):   ${data['withdraw']:,.2f}",
        "───────────────────────────────────────",
        f"  Рост:            ${data['growth']:,.2f}",
        f"  Новый баланс:    ${data['new_balance']:,.2f}",
        f"  Статус:          {data['status']}",
        "───────────────────────────────────────",
        "  Безопасный риск (от нового баланса):",
        f"    1% →  ${data['risk_1']:,.2f}",
        f"    2% →  ${data['risk_2']:,.2f}",
        f"    5% →  ${data['risk_5']:,.2f}",
        "═══════════════════════════════════════",
    ]
    return "\n".join(lines)


# ─── Goal Engine ─────────────────────────────────────────────

def goal_calculate(balance: float, goal: float, avg_growth: float) -> dict:
    """Посчитать путь до цели."""
    remaining = max(0, goal - balance)
    if remaining == 0:
        trades_needed = 0
    elif avg_growth <= 0:
        trades_needed = float("inf")
    else:
        trades_needed = math.ceil(remaining / avg_growth)
    return {
        "balance": balance,
        "goal": goal,
        "avg_growth": avg_growth,
        "remaining": remaining,
        "trades_needed": trades_needed,
    }


def goal_summary(data: dict) -> str:
    """Вывод Goal Engine."""
    if data["remaining"] <= 0:
        status = "🏆 Цель достигнута!"
    elif data["trades_needed"] == float("inf"):
        status = "⚠ Невозможно при текущем росте"
    else:
        status = f"🎯 {data['trades_needed']} успешных сделок"

    lines = [
        "═══════════════════════════════════════",
        "       🎯 Goal Engine",
        "═══════════════════════════════════════",
        f"  Сейчас:          ${data['balance']:,.2f}",
        f"  Цель:           ${data['goal']:,.2f}",
        f"  Ср. рост/сделка: ${data['avg_growth']:,.2f}",
        "───────────────────────────────────────",
        f"  Осталось:       ${data['remaining']:,.2f}",
        f"  {status}",
        "═══════════════════════════════════════",
    ]
    return "\n".join(lines)


# ─── Risk Engine ─────────────────────────────────────────────

def risk_calculate(balance: float, risk_pct: float, stop_pct: float) -> dict:
    """Рассчитать допустимую потерю и размер позиции."""
    risk_pct = max(0, min(risk_pct, 100))
    stop_pct = max(0.01, min(stop_pct, 100))
    risk_amount = balance * (risk_pct / 100)
    position_size = risk_amount / (stop_pct / 100)
    return {
        "balance": balance,
        "risk_pct": risk_pct,
        "stop_pct": stop_pct,
        "risk_amount": risk_amount,
        "position_size": position_size,
    }


def risk_summary(data: dict) -> str:
    """Вывод Risk Engine."""
    lines = [
        "═══════════════════════════════════════",
        "       ⚙ Risk Engine",
        "═══════════════════════════════════════",
        f"  Баланс:          ${data['balance']:,.2f}",
        f"  Риск:            {data['risk_pct']}%",
        f"  Стоп-лосс:       {data['stop_pct']}%",
        "───────────────────────────────────────",
        f"  Макс. потеря:    ${data['risk_amount']:,.2f}",
        f"  Размер позиции:  ${data['position_size']:,.2f}",
        "═══════════════════════════════════════",
    ]
    return "\n".join(lines)


# ─── Strategy Engine ────────────────────────────────────────

MODES = {
    "SURVIVAL": {
        "withdraw_limit": 0.0,
        "recommended_risk": 0.5,
        "advice": "Не выводи. Сохраняй капитал. Минимальный риск.",
    },
    "GROWTH": {
        "withdraw_limit": 0.3,
        "recommended_risk": 2.0,
        "advice": "Продолжай рост, но не увеличивай риск без причины.",
    },
    "AGGRESSIVE": {
        "withdraw_limit": 0.5,
        "recommended_risk": 1.5,
        "advice": "Можно выводить до 50% прибыли. Не зарывайся.",
    },
    "DANGER": {
        "withdraw_limit": 0.0,
        "recommended_risk": 0.5,
        "advice": "Стоп. Снижай риск. Не выводи. Пересмотри стратегию.",
    },
}


def strategy_engine(balance: float, growth: float, goal: float,
                    risk_pct: float, avg_growth: float) -> dict:
    """Определить режим, рекомендации и health score."""
    # 1. Режим трейдера
    if growth < 0 and risk_pct > 3:
        mode = "DANGER"
    elif growth < 0:
        mode = "SURVIVAL"
    elif balance >= goal * 0.8:
        mode = "AGGRESSIVE"
    else:
        mode = "GROWTH"

    cfg = MODES[mode]

    # 2. Лимит вывода
    if growth > 0:
        max_withdraw = growth * cfg["withdraw_limit"]
    else:
        max_withdraw = 0.0

    # 3. Рекомендованный риск
    recommended_risk = cfg["recommended_risk"]

    # 4. Health Score (0–100)
    score = 50

    if growth > 0:
        score += 20
    else:
        score -= 30

    if risk_pct <= 2:
        score += 10
    elif risk_pct > 5:
        score -= 20

    if avg_growth > 0:
        score += 10

    if goal > 0 and balance >= goal * 0.5:
        score += 10

    score = max(0, min(score, 100))

    return {
        "mode": mode,
        "health_score": score,
        "risk_pct": risk_pct,
        "recommended_risk": recommended_risk,
        "max_withdraw": max_withdraw,
        "advice": cfg["advice"],
    }


def strategy_summary(data: dict) -> str:
    """Вывод Strategy Engine."""
    withdraw_line = (
        f"  Можно выводить до ${data['max_withdraw']:,.2f}"
        if data["max_withdraw"] > 0
        else "  Вывод не рекомендуется."
    )
    lines = [
        "═══════════════════════════════════════",
        "       🧠 Strategy Engine",
        "═══════════════════════════════════════",
        f"  Режим:            {data['mode']}",
        f"  Health Score:     {data['health_score']}/100",
        f"  Риск сейчас:      {data['risk_pct']}%",
        f"  Реком. риск:      {data['recommended_risk']}%",
        "───────────────────────────────────────",
        "  Вывод:",
        f"  {withdraw_line}",
        "",
        "  Совет:",
        f"  {data['advice']}",
        "═══════════════════════════════════════",
    ]
    return "\n".join(lines)


# ─── Portfolio Memory ────────────────────────────────────────

def load_session() -> dict | None:
    """Загрузить последнюю сессию."""
    if not os.path.exists(HISTORY_FILE):
        return None
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
    if not data.get("sessions"):
        return None
    return data["sessions"][-1]


def save_session(balance: float, goal: float, avg_growth: float, risk_pct: float,
                 mode: str = "", health_score: int = 0):
    """Сохранить сессию."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {"sessions": []}

    data["sessions"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "balance": balance,
        "goal": goal,
        "avg_growth": avg_growth,
        "risk_pct": risk_pct,
        "mode": mode,
        "health_score": health_score,
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def memory_summary(session: dict) -> str:
    """Показать сохранённую сессию."""
    mode_str = session.get("mode", "—")
    hs = session.get("health_score", "—")
    lines = [
        "───────────────────────────────────────",
        "  💾 Последняя сессия:",
        f"    Дата:       {session['date']}",
        f"    Баланс:    ${session['balance']:,.2f}",
        f"    Цель:      ${session['goal']:,.2f}",
        f"    Ср. рост:  ${session['avg_growth']:,.2f}",
        f"    Риск:      {session['risk_pct']}%",
        f"    Режим:     {mode_str}",
        f"    Health:    {hs}/100",
        "───────────────────────────────────────",
    ]
    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────

def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠ Введите число.")


def main():
    print("\n  Hybrid Finance OS v0.2.0\n")

    # Показать последнюю сессию
    last = load_session()
    if last:
        print(memory_summary(last))

    print("  [1] Баланс + Риск")
    print("  [2] Goal Engine")
    print("  [3] Risk Engine")
    print("  [4] Всё")
    print("  [5] Strategy Engine\n")
    choice = input("  Выбор: ").strip()

    if choice not in ("1", "2", "3", "4", "5"):
        print("  ⚠ Неверный выбор.")
        return

    # Дефолты из памяти
    mem_balance = last["balance"] if last else None
    mem_goal = last["goal"] if last else None
    mem_growth = last["avg_growth"] if last else None
    mem_risk = last["risk_pct"] if last else None

    # --- Balance ---
    if choice in ("1", "4"):
        balance = input_float("\n  Баланс (текущий депозит): $")
        profit = input_float("  Прибыль со сделки:       $")
        withdraw = input_float("  Забираю на жизнь/кредит: $")
        data = calculate(balance, profit, withdraw)
        print()
        print(summary(data))

    # --- Goal ---
    if choice in ("2", "4"):
        if choice == "4":
            bal = data["new_balance"]
            print(f"\n  (берём новый баланс: ${bal:,.2f})")
        else:
            bal = input_float("\n  Текущий баланс: $")
        goal = input_float("  Цель:            $")
        avg_growth = input_float("  Ср. рост/сделка: $")
        gdata = goal_calculate(bal, goal, avg_growth)
        print()
        print(goal_summary(gdata))

    # --- Risk ---
    if choice in ("3", "4"):
        if choice == "4":
            bal = data["new_balance"]
            print(f"\n  (берём новый баланс: ${bal:,.2f})")
        else:
            bal = input_float("\n  Баланс: $")
        risk_pct = input_float("  Риск (%):        ")
        stop_pct = input_float("  Стоп-лосс (%):   ")
        rdata = risk_calculate(bal, risk_pct, stop_pct)
        print()
        print(risk_summary(rdata))

    # --- Strategy ---
    if choice in ("4", "5"):
        if choice == "5":
            bal = input_float("\n  Баланс: $")
            growth_val = input_float("  Рост (последний):  $")
            goal = input_float("  Цель:            $")
            risk_pct = input_float("  Текущий риск (%): ")
            avg_growth = input_float("  Ср. рост/сделка: $")
        else:
            bal = data["new_balance"]
            growth_val = data["growth"]
            # goal и avg_growth уже определены выше
            # risk_pct уже определён выше

        sdata = strategy_engine(bal, growth_val, goal, risk_pct, avg_growth)
        print()
        print(strategy_summary(sdata))

    # --- Сохранить сессию ---
    s_mode = ""
    s_health = 0

    if choice == "4":
        s_mode = sdata["mode"]
        s_health = sdata["health_score"]
        save_session(data["new_balance"], goal, avg_growth, risk_pct, s_mode, s_health)
    elif choice == "5":
        s_mode = sdata["mode"]
        s_health = sdata["health_score"]
        save_session(bal, goal, avg_growth, risk_pct, s_mode, s_health)
    elif choice == "1":
        save_session(data["new_balance"], mem_goal or 0, mem_growth or 0, mem_risk or 2)
    elif choice == "2":
        save_session(bal, goal, avg_growth, mem_risk or 2)
    elif choice == "3":
        save_session(bal, mem_goal or 0, mem_growth or 0, risk_pct)

    print("\n  💾 Сессия сохранена.")


if __name__ == "__main__":
    main()
