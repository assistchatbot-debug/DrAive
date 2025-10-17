"""
Organizational Chart (7x21 methodology)
21 positions across 7 departments
"""

# 21 positions organizational structure
ORGBOARD_21_POSITIONS = [
    {"pos": 21, "name": "Офис Учредителя", "dept": 7, "div": 3},
    {"pos": 20, "name": "Отдел официальных вопросов", "dept": 7, "div": 3},
    {"pos": 19, "name": "Офис директоров (CEO)", "dept": 7, "div": 3},
    {"pos": 1, "name": "Отдел персонала", "dept": 1, "div": 1},
    {"pos": 2, "name": "Отдел коммуникаций", "dept": 1, "div": 1},
    {"pos": 3, "name": "Отдел инспекций", "dept": 1, "div": 1},
    {"pos": 4, "name": "Отдел маркетинга", "dept": 2, "div": 1},
    {"pos": 5, "name": "Отдел рекламы", "dept": 2, "div": 1},
    {"pos": 6, "name": "Отдел продаж", "dept": 2, "div": 1},
    {"pos": 7, "name": "Отдел дохода", "dept": 3, "div": 1},
    {"pos": 8, "name": "Отдел расходов", "dept": 3, "div": 1},
    {"pos": 9, "name": "Отдел документации", "dept": 3, "div": 1},
    {"pos": 10, "name": "Отдел планирования", "dept": 4, "div": 2},
    {"pos": 11, "name": "Отдел обеспечения", "dept": 4, "div": 2},
    {"pos": 12, "name": "Отдел производства", "dept": 4, "div": 2},
    {"pos": 13, "name": "Отдел качества", "dept": 5, "div": 2},
    {"pos": 14, "name": "Отдел обучения", "dept": 5, "div": 2},
    {"pos": 15, "name": "Отдел коррекций", "dept": 5, "div": 2},
    {"pos": 16, "name": "Отдел информирования", "dept": 6, "div": 2},
    {"pos": 17, "name": "Отдел новых клиентов", "dept": 6, "div": 2},
    {"pos": 18, "name": "Отдел представительств", "dept": 6, "div": 2},
]

# Department names
DEPARTMENT_NAMES = {
    1: "Департамент 1: Кадровое отделение",
    2: "Департамент 2: Отделение расширения",
    3: "Департамент 3: Финансовое отделение",
    4: "Департамент 4: Технологическое отделение",
    5: "Департамент 5: Квалификационное отделение",
    6: "Департамент 6: Публичное отделение",
    7: "Департамент 7: Исполнительное отделение"
}


async def create_company_positions(company_id: str, founder_user_id: str):
    """
    Create all 21 positions for a new company
    Founder gets assigned to all positions initially
    """
    from bot.core.database import create_position

    for pos_data in ORGBOARD_21_POSITIONS:
        await create_position(
            company_id=company_id,
            position_number=pos_data["pos"],
            position_name=pos_data["name"],
            department_number=pos_data["dept"],
            division_number=pos_data["div"],
            assigned_user_id=founder_user_id,
            is_founder=(pos_data["pos"] == 21),  # Position 21 is founder
            is_ceo=False
        )


def format_orgchart(positions: list, lang: str = "ru") -> str:
    """Format organizational chart as text"""
    if lang == "ru":
        text = "📊 Организационная структура компании\n\n"
    else:
        text = "📊 Company Organizational Structure\n\n"

    current_dept = None
    for pos in positions:
        if current_dept != pos["department_number"]:
            current_dept = pos["department_number"]
            text += f"\n{DEPARTMENT_NAMES.get(current_dept, f'Department {current_dept}')}:\n"

        status = "✅" if pos["assigned_user_id"] else "⚪"
        text += f"{status} #{pos['position_number']}. {pos['position_name']}\n"

    return text
