"""Hybrid Finance OS v0.0.3 — финансовая экосистема трейдера."""

import math


def calculate(balance: float, profit: float, withdraw: float) -> dict:
    """Рассчитать рост, новый баланс, риски и статус."""
    growth = profit - withdraw
    new_balance = balance + growth

    if growth > 0:
        status = "📈 Растёшь"
    elif growth == 0:
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
        "       Hybrid Finance OS v0.0.3",
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
    remaining = goal - balance
    if avg_growth <= 0:
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


# ─── CLI ─────────────────────────────────────────────────────

def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠ Введите число.")


def main():
    print("\n  Hybrid Finance OS v0.0.3\n")
    print("  [1] Баланс + Риск")
    print("  [2] Goal Engine")
    print("  [3] Оба\n")
    choice = input("  Выбор: ").strip()

    if choice in ("1", "3"):
        balance = input_float("\n  Баланс (текущий депозит): $")
        profit = input_float("  Прибыль со сделки:       $")
        withdraw = input_float("  Забираю на жизнь/кредит: $")
        data = calculate(balance, profit, withdraw)
        print()
        print(summary(data))
    else:
        balance = None

    if choice in ("2", "3"):
        if choice == "3":
            bal = data["new_balance"]
            print(f"\n  (берём новый баланс: ${bal:,.2f})")
        else:
            bal = input_float("\n  Текущий баланс: $")
        goal = input_float("  Цель:            $")
        avg_growth = input_float("  Ср. рост/сделка: $")
        gdata = goal_calculate(bal, goal, avg_growth)
        print()
        print(goal_summary(gdata))


if __name__ == "__main__":
    main()
