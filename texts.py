"""
Multilingual text resources for DrAivBot
Centralized i18n management
"""

TEXTS = {
    "ru": {
        # Welcome & Menu
        "welcome": "👋 Добро пожаловать в AI Strategy Advisor!",
        "intro": (
            "🤖 Я ваш специализированный ИИ-ассистент для бизнеса!\n\n"
            "Помогу:\n"
            "✅ Проанализировать идею и построить бизнес-план\n"
            "✅ Рассчитать финансы и окупаемость\n"
            "✅ Составить организационную структуру\n"
            "✅ Автоматизировать рутинные задачи\n"
            "✅ Устранить слабые и усилить сильные стороны\n"
            "✅ Найти конкурентов и поставщиков"
        ),
        "menu_title": "📋 Что будем делать?",
        "menu_subtitle": "Выберите раздел:",
        "under_dev": "🚧 Раздел в разработке",
        "back_menu": "◀️ Главное меню",

        # Company Registration
        "company_welcome": (
            "🏢 Создаём вашу компанию\n\n"
            "Вы становитесь владельцем компании и можете:\n"
            "✅ Анализировать бизнес-идеи с помощью ИИ\n"
            "✅ Получать готовые бизнес-планы с финансами\n"
            "✅ Приглашать сотрудников и делегировать задачи\n"
            "✅ Автоматизировать рутинные задачи\n\n"
            "📝 Введите название вашей компании:"
        ),
        "company_created": "✅ Компания создана!",
        "company_next_steps": (
            "🎯 Что дальше?\n\n"
            "1️⃣ \"Анализ бизнес-идеи\" - получите бизнес-план с финансовой моделью\n"
            "2️⃣ \"Организационная структура\" - пригласите сотрудников\n"
            "3️⃣ \"Управление целями\" - стройте стратегию развития\n\n"
            "👇 Рекомендую начать с \"Анализа бизнес-идеи\":"
        ),

        # Settings
        "choose_lang": "🌐 Выберите язык:",
        "lang_set": "✅ Язык установлен",

        # Errors
        "error_generic": "❌ Произошла ошибка. Попробуйте позже.",
        "error_no_company": "❌ Компания не найдена",
        "error_no_permission": "❌ Недостаточно прав доступа",
    },

    "en": {
        # Welcome & Menu
        "welcome": "👋 Welcome to AI Strategy Advisor!",
        "intro": (
            "🤖 I'm your specialized AI business assistant!\n\n"
            "I can help you:\n"
            "✅ Analyze your idea and build a business plan\n"
            "✅ Calculate finances and ROI\n"
            "✅ Create organizational structure\n"
            "✅ Automate routine tasks\n"
            "✅ Eliminate weaknesses and strengthen your business\n"
            "✅ Find competitors and suppliers"
        ),
        "menu_title": "📋 What would you like to do?",
        "menu_subtitle": "Choose a section:",
        "under_dev": "🚧 Section under development",
        "back_menu": "◀️ Main Menu",

        # Company Registration
        "company_welcome": (
            "🏢 Creating your company\n\n"
            "You become the company owner and can:\n"
            "✅ Analyze business ideas with AI\n"
            "✅ Get ready business plans with finances\n"
            "✅ Invite employees and delegate tasks\n"
            "✅ Automate routine tasks\n\n"
            "📝 Enter your company name:"
        ),
        "company_created": "✅ Company created!",
        "company_next_steps": (
            "🎯 What's next?\n\n"
            "1️⃣ \"Business Idea Analysis\" - get a business plan with financial model\n"
            "2️⃣ \"Organizational Structure\" - invite employees\n"
            "3️⃣ \"Goal Management\" - build development strategy\n\n"
            "👇 I recommend starting with \"Business Idea Analysis\":"
        ),

        # Settings
        "choose_lang": "🌐 Choose your language:",
        "lang_set": "✅ Language set",

        # Errors
        "error_generic": "❌ An error occurred. Please try again later.",
        "error_no_company": "❌ Company not found",
        "error_no_permission": "❌ Insufficient permissions",
    }
}


def get_text(lang: str, key: str) -> str:
    """Get localized text by key"""
    return TEXTS.get(lang, TEXTS["ru"]).get(key, key)
