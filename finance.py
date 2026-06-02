"""Hybrid Finance OS v0.0.4 — финансовая экосистема трейдера."""

import math


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
        "       Hybrid Finance OS v0.0.4",
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
    risk_amount = balance * (risk_pct / 100)
    if stop_pct <= 0:
        position_size = 0.0
    else:
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


# ─── CLI ─────────────────────────────────────────────────────

def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠ Введите число.")


def main():
    print("\n  Hybrid Finance OS v0.0.4\n")
    print("  [1] Баланс + Риск")
    print("  [2] Goal Engine")
    print("  [3] Risk Engine")
    print("  [4] Всё\n")
    choice = input("  Выбор: ").strip()

    if choice not in ("1", "2", "3", "4"):
        print("  ⚠ Неверный выбор.")
        return

    if choice in ("1", "4"):
        balance = input_float("\n  Баланс (текущий депозит): $")
        profit = input_float("  Прибыль со сделки:       $")
        withdraw = input_float("  Забираю на жизнь/кредит: $")
        data = calculate(balance, profit, withdraw)
        print()
        print(summary(data))

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


if __name__ == "__main__":
    main()
