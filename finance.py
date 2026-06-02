"""Hybrid Finance OS v0.0.2 — простой калькулятор финансов трейдера."""


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
        "       Hybrid Finance OS v0.0.2",
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


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠ Введите число.")


def main():
    print("\n  Hybrid Finance OS v0.0.2\n")
    balance = input_float("  Баланс (текущий депозит): $")
    profit = input_float("  Прибыль со сделки:       $")
    withdraw = input_float("  Забираю на жизнь/кредит: $")

    data = calculate(balance, profit, withdraw)
    print()
    print(summary(data))


if __name__ == "__main__":
    main()
