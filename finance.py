"""Hybrid Finance OS v0.0.1 — простой калькулятор финансов трейдера."""


def calculate(balance: float, profit: float, withdraw: float) -> dict:
    """Рассчитать остаток на рост и безопасные риски."""
    available = balance + profit - withdraw
    return {
        "balance": balance,
        "profit": profit,
        "withdraw": withdraw,
        "available": available,
        "risk_1": available * 0.01,
        "risk_2": available * 0.02,
        "risk_5": available * 0.05,
    }


def summary(data: dict) -> str:
    """Короткий вывод."""
    lines = [
        "═══════════════════════════════════════",
        "       Hybrid Finance OS v0.0.1",
        "═══════════════════════════════════════",
        f"  Баланс:          ${data['balance']:,.2f}",
        f"  Прибыль:         ${data['profit']:,.2f}",
        f"  Вывод (жизнь):   ${data['withdraw']:,.2f}",
        "───────────────────────────────────────",
        f"  На рост:         ${data['available']:,.2f}",
        "───────────────────────────────────────",
        "  Безопасный риск:",
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
    print("\n  Hybrid Finance OS v0.0.1\n")
    balance = input_float("  Баланс (текущий депозит): $")
    profit = input_float("  Прибыль со сделки:       $")
    withdraw = input_float("  Забираю на жизнь/кредит: $")

    data = calculate(balance, profit, withdraw)
    print()
    print(summary(data))


if __name__ == "__main__":
    main()
