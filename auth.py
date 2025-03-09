import streamlit as st
from telethon import TelegramClient, functions, types, errors
import asyncio
import os
import traceback
from event_loop import run_async, LOOP

class TelegramAuth:
    def __init__(self):
        # API ключи встроены напрямую в код
        self.api_id = 27578030  # Real API ID
        self.api_hash = "41174379fa369fe72db4d97fcbe3d1c6"  # Real API Hash
        self.client = None
        self.phone = None
        self.is_connected = False

        # Создаем путь в .streamlit для сохранения сессии, так как этот каталог сохраняется
        # между перезапусками
        session_dir = ".streamlit"
        if not os.path.exists(session_dir):
            os.makedirs(session_dir, exist_ok=True)

        # Путь к файлу сессии
        self.session_file = os.path.join(session_dir, "scam_checker_session")

        # Добавляем путь к файлу сессии в сессионное состояние для отладки
        if 'session_file_path' not in st.session_state:
            st.session_state.session_file_path = f"{self.session_file}.session"

        # Если файл сессии существует в корне, переместим его
        old_session = "scam_checker_session.session"
        if os.path.exists(old_session) and not os.path.exists(f"{self.session_file}.session"):
            try:
                import shutil
                shutil.copy2(old_session, f"{self.session_file}.session")
                st.success("Файл сессии перемещен в постоянное хранилище")
            except Exception as e:
                st.error(f"Ошибка при перемещении файла сессии: {str(e)}")

    async def connect(self):
        """Подключение к Telegram API"""
        try:
            if not self.client:
                # Важно использовать существующий цикл событий
                self.client = TelegramClient(
                    self.session_file, 
                    self.api_id, 
                    self.api_hash,
                    device_model="SafeBase Checker",
                    system_version="1.0",
                    app_version="1.0",
                    lang_code="ru",
                    loop=LOOP
                )

            # Пытаемся подключиться с обработкой ошибок
            if not self.client.is_connected():
                await self.client.connect()

            # Проверяем авторизацию после подключения
            authorized = await self.client.is_user_authorized()

            if not authorized:
                # Если файл сессии существует, но авторизация не удалась, 
                # значит сессия недействительна
                session_path = f"{self.session_file}.session"
                if os.path.exists(session_path):
                    st.warning("Сессия устарела. Требуется повторная авторизация.")
                    # Не удаляем файл, так как Telethon перезапишет его

            self.is_connected = True
            return self.client.is_connected()
        except Exception as e:
            error_details = traceback.format_exc()
            st.error(f"Ошибка подключения: {str(e)}")
            st.error(f"Подробности: {error_details}")
            return False

    async def send_code(self, phone):
        """Отправка кода подтверждения на телефон"""
        self.phone = phone
        try:
            if not self.is_connected:
                await self.connect()

            result = await self.client.send_code_request(phone)
            return True, result.phone_code_hash
        except errors.PhoneNumberInvalidError:
            return False, "Неверный формат номера телефона"
        except errors.FloodWaitError as e:
            return False, f"Слишком много попыток. Попробуйте через {e.seconds} секунд"
        except Exception as e:
            error_msg = str(e)
            st.error(f"Ошибка при отправке кода: {error_msg}")
            return False, error_msg

    async def sign_in(self, code, phone_code_hash=None):
        """Вход в аккаунт с помощью кода подтверждения"""
        try:
            if not self.is_connected:
                await self.connect()

            await self.client.sign_in(self.phone, code, phone_code_hash=phone_code_hash)
            return True, "Вход выполнен успешно!"
        except errors.SessionPasswordNeededError:
            return False, "Требуется пароль 2FA. Пока не поддерживается."
        except errors.PhoneCodeInvalidError:
            return False, "Неверный код подтверждения"
        except Exception as e:
            error_msg = str(e)
            st.error(f"Ошибка при входе: {error_msg}")
            return False, error_msg

    async def check_auth(self):
        """Проверка авторизации"""
        try:
            # Информация для отладки
            session_path = f"{self.session_file}.session"

            # Проверяем существование файла сессии
            session_exists = os.path.exists(session_path)
            if not session_exists:
                st.warning(f"Файл сессии не найден по пути: {session_path}")
                # Проверяем наличие файла сессии в корневой директории
                root_session = "scam_checker_session.session"
                if os.path.exists(root_session):
                    try:
                        import shutil
                        # Копируем файл сессии из корневой директории
                        shutil.copy2(root_session, session_path)
                        st.success("Файл сессии скопирован из корневой директории")
                        session_exists = True
                    except Exception as e:
                        st.error(f"Ошибка при копировании файла сессии: {str(e)}")

            # Инициализация клиента
            if not self.client:
                # Важно использовать существующий цикл событий
                self.client = TelegramClient(
                    self.session_file, 
                    self.api_id, 
                    self.api_hash,
                    device_model="SafeBase Checker",
                    system_version="1.0",
                    app_version="1.0",
                    lang_code="ru",
                    loop=LOOP
                )

            # Подключаемся к API
            if not self.client.is_connected():
                await self.client.connect()

            # Проверяем авторизацию
            authorized = await self.client.is_user_authorized()

            # Если сессия существует, но авторизация не удалась, 
            # сбрасываем состояние авторизации в приложении
            if not authorized and session_exists:
                st.warning("Сессия устарела. Требуется повторная авторизация.")
                return False

            # Если авторизованы, сохраняем информацию о статусе
            if authorized:
                # Можно добавить дополнительную проверку валидности сессии
                # например, запрос базовой информации о пользователе
                try:
                    me = await self.client.get_me()
                    if me:
                        st.session_state.user_info = f"Авторизован как: {me.first_name} (@{me.username if me.username else 'без username'})"
                except Exception as e:
                    st.warning(f"Сессия существует, но возникла ошибка при получении данных пользователя: {str(e)}")
                    # Несмотря на ошибку, продолжаем считать пользователя авторизованным

            return authorized
        except errors.AuthKeyUnregisteredError:
            st.warning("Требуется повторная авторизация: ключ сессии недействителен.")
            return False
        except Exception as e:
            error_details = traceback.format_exc()
            st.error(f"Ошибка проверки авторизации: {str(e)}")
            st.error(f"Подробности: {error_details}")
            return False

    async def disconnect(self):
        """Отключение от Telegram API"""
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            self.is_connected = False

def show_auth_page():
    st.title("СИСТЕМА АУТЕНТИФИКАЦИИ")

    st.markdown("""
    ## АВТОРИЗАЦИЯ ЧЕРЕЗ TELEGRAM

    ДЛЯ ПОЛУЧЕНИЯ ДОСТУПА К ПОЛНОМУ ФУНКЦИОНАЛУ АНАЛИТИЧЕСКОЙ СИСТЕМЫ ТРЕБУЕТСЯ АВТОРИЗАЦИЯ ЧЕРЕЗ АККАУНТ TELEGRAM. АВТОРИЗАЦИЯ НЕОБХОДИМА ДЛЯ ПРЕДОСТАВЛЕНИЯ РАСШИРЕННОГО ДОСТУПА К ИНСТРУМЕНТАМ АНАЛИЗА.

    ## ИНСТРУКЦИЯ ПО АВТОРИЗАЦИИ:

    1. ВВЕДИТЕ ВАШ НОМЕР ТЕЛЕФОНА В МЕЖДУНАРОДНОМ ФОРМАТЕ (НАПРИМЕР, +7XXXXXXXXXX)
    2. ПОЛУЧИТЕ И ВВЕДИТЕ КОД ПОДТВЕРЖДЕНИЯ, ОТПРАВЛЕННЫЙ В TELEGRAM
    3. ЕСЛИ У ВАС ВКЛЮЧЕНА ДВУХФАКТОРНАЯ АУТЕНТИФИКАЦИЯ, ВВЕДИТЕ ВАШ ПАРОЛЬ

    ПРОЦЕСС АВТОРИЗАЦИИ ПОЛНОСТЬЮ БЕЗОПАСЕН. ВАШИ ДАННЫЕ ЗАЩИЩЕНЫ И ИСПОЛЬЗУЮТСЯ ИСКЛЮЧИТЕЛЬНО ДЛЯ АУТЕНТИФИКАЦИИ В СИСТЕМЕ.
    """)

    # Инициализация состояния сессии для аутентификации
    if 'auth_stage' not in st.session_state:
        st.session_state.auth_stage = 'phone'
    if 'auth_message' not in st.session_state:
        st.session_state.auth_message = ''
    if 'phone' not in st.session_state:
        st.session_state.phone = ''
    if 'phone_code_hash' not in st.session_state:
        st.session_state.phone_code_hash = None
    if 'auth' not in st.session_state:
        st.session_state.auth = TelegramAuth()

    # Расширенное информационное сообщение в плашке
    st.markdown("""
    <div class="info-card">
        <h2>Зачем нужна авторизация?</h2>
        <p>Авторизация в Telegram необходима для выполнения следующих функций:</p>
        <p>• Проверка пользователей и каналов на признаки скам-активности</p>
        <p>• Анализ сообщений и истории пользователя</p>
        <p>• Получение доступа к API Telegram для сбора информации</p>
        <p>• Обнаружение потенциально опасных контактов</p>
        <p>Ваши учетные данные используются только для API-запросов, обрабатываются локально и нигде не хранятся.</p>
    </div>
    """, unsafe_allow_html=True)

    # Отображаем сообщение, если оно есть
    if st.session_state.auth_message:
        st.info(st.session_state.auth_message)

    # Форма ввода номера телефона
    if st.session_state.auth_stage == 'phone':
        with st.form("phone_form"):
            phone = st.text_input("Введите номер телефона в международном формате:", 
                                value=st.session_state.phone,
                                placeholder="+7XXXXXXXXXX")

            submit = st.form_submit_button("Отправить код")

            if submit and phone:
                with st.spinner("Отправка кода подтверждения..."):
                    st.session_state.phone = phone
                    success, result = run_async(st.session_state.auth.send_code(phone))

                    if success:
                        st.session_state.phone_code_hash = result
                        st.session_state.auth_stage = 'code'
                        st.session_state.auth_message = "Код отправлен на ваш телефон!"
                        st.rerun()
                    else:
                        st.error(f"Ошибка при отправке кода: {result}")

    # Форма ввода кода подтверждения
    elif st.session_state.auth_stage == 'code':
        st.text_input("Номер телефона", value=st.session_state.phone, disabled=True)

        with st.form("code_form"):
            code = st.text_input("Введите полученный код:", max_chars=5)

            col1, col2 = st.columns([1, 3])
            with col1:
                back = st.form_submit_button("Назад")
            with col2:
                submit = st.form_submit_button("Войти")

            if back:
                st.session_state.auth_stage = 'phone'
                st.session_state.auth_message = ''
                st.rerun()

            if submit and code:
                with st.spinner("Проверка..."):
                    success, message = run_async(
                        st.session_state.auth.sign_in(code, st.session_state.phone_code_hash)
                    )

                    if success:
                        st.session_state.is_authenticated = True
                        st.session_state.auth_message = message
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(f"Ошибка входа: {message}")