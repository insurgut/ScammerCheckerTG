
# Телеграм Чекер

## О проекте

Телеграм Чекер — это комплексная система анализа профилей Telegram для обеспечения безопасного цифрового взаимодействия и предотвращения мошеннических действий. Приложение позволяет проверять аккаунты Telegram на предмет их надежности, используя различные методы верификации и анализа данных.

## Функциональные возможности

- Авторизация через официальный API Telegram
- Многоуровневая проверка аккаунтов на надежность
- Детальный анализ профилей с рекомендациями
- Интуитивно понятный пользовательский интерфейс
- Защита персональных данных пользователей

## Архитектура системы

```mermaid
flowchart TB
    A[Пользовательский интерфейс] --> B[Модуль авторизации]
    B --> C[Telegram API]
    A --> D[Система верификации]
    D --> E[Сервис проверки профилей]
    E --> F[База данных ненадежных аккаунтов]
    E --> G[Алгоритмы машинного обучения]
    E --> H[Поведенческий анализ]
    D --> I[Модуль генерации отчетов]
    I --> A
```

## Процесс верификации аккаунта

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant App as Телеграм Защитник
    participant Auth as Модуль авторизации
    participant TG as Telegram API
    participant VS as Сервис верификации
    participant DB as База данных

    User->>App: Ввод username/ID для проверки
    App->>Auth: Проверка авторизации
    Auth->>TG: Запрос сессии
    TG-->>Auth: Подтверждение
    Auth-->>App: Авторизован
    App->>VS: Запрос на верификацию
    VS->>DB: Поиск в базе данных
    VS->>TG: Получение информации о профиле
    DB-->>VS: Результаты поиска
    TG-->>VS: Информация о профиле
    VS->>VS: Анализ данных
    VS-->>App: Результаты верификации
    App-->>User: Отображение результатов и рекомендаций
```

## Компоненты системы

```mermaid
classDiagram
    class TelegramDefender {
        +run()
    }
    class AuthModule {
        +phone_number: string
        +code: string
        +client: TelegramClient
        +connect()
        +login()
        +check_auth()
        +disconnect()
    }
    class VerificationService {
        +check_account(username_or_id: string)
        -analyze_profile(profile_data: object)
        -generate_report(analysis_results: object)
    }
    class UserInterface {
        +show_auth_page()
        +show_verification_page()
        +display_results(results: object)
    }
    class EventLoop {
        +LOOP: AsyncIOEventLoop
        +run_async(coroutine: function)
    }
    
    TelegramDefender --> AuthModule
    TelegramDefender --> VerificationService
    TelegramDefender --> UserInterface
    AuthModule --> EventLoop
    VerificationService --> EventLoop
    UserInterface --> AuthModule
    UserInterface --> VerificationService
```

## Статистика проверок

```mermaid
pie title Результаты проверок (последние 1000)
    "Надежные аккаунты" : 723
    "Ненадежные аккаунты" : 198
    "Неопределенные" : 59
    "Не найдены" : 20
```

## Установка и запуск

1. Клонируйте репозиторий
2. Установите зависимости из файла requirements.txt
3. Запустите приложение командой `streamlit run app.py`

## Требования

- Python 3.8 или выше
- Streamlit
- Telethon
- API ключи Telegram (получите их на https://my.telegram.org)

## Лицензия

© 2023 Все права защищены. Версия 2.1.0
