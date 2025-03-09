import streamlit as st

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Telegram Analyzer",
    page_icon="🔍",
    layout="centered"
)

from event_loop import run_async
from styles import apply_styles
from auth import show_auth_page, TelegramAuth
from scam_checker import show_scam_checker_page

# Инициализация состояния сессии
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'check_result' not in st.session_state:
    st.session_state.check_result = None
if 'check_status' not in st.session_state:
    st.session_state.check_status = None
if 'check_message' not in st.session_state:
    st.session_state.check_message = None

# Apply custom styles
apply_styles()

def main():
    try:
        # Проверка авторизации если сессия уже существует
        if 'auth' in st.session_state:
            st.session_state.is_authenticated = run_async(st.session_state.auth.check_auth())
            
        # Отображаем страницу авторизации, если пользователь не авторизован
        if not st.session_state.is_authenticated:
            show_auth_page()
        else:
            # Отображаем страницу проверки 
            show_scam_checker_page()
    except Exception as e:
        st.error(f"Произошла ошибка соединения: {str(e)}")
        st.warning("Пожалуйста, обновите страницу и попробуйте снова.")
        # Проверяем и очищаем состояние сессии при критической ошибке
        if 'auth' in st.session_state:
            try:
                run_async(st.session_state.auth.disconnect())
            except:
                pass
            st.session_state.is_authenticated = False

        # Кнопка выхода
        if st.button("ВЫЙТИ ИЗ АККАУНТА"):
            if 'auth' in st.session_state:
                # Корректно отключаемся от API Telegram
                run_async(st.session_state.auth.disconnect())

                # Сохраняем путь к файлу сессии для информации
                session_file_path = None
                if 'session_file_path' in st.session_state:
                    session_file_path = st.session_state.session_file_path

                # Очистка состояния сессии
                for key in list(st.session_state.keys()):
                    del st.session_state[key]

                # Восстанавливаем информацию о файле сессии для отладки
                if session_file_path:
                    st.session_state.last_session_file = session_file_path
                    st.info(f"ВЫХОД УСПЕШНО ВЫПОЛНЕН.")
            else:
                # Очистка состояния сессии
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.info("ВЫХОД УСПЕШНО ВЫПОЛНЕН.")

            st.rerun()

        # Нижний колонтитул
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; font-size: 1.4rem; margin-top: 2.5rem;">
            <div>TELEGRAM ANALYZER | МОЩНЫЙ ИНСТРУМЕНТ ДЛЯ РАСШИРЕННОЙ АНАЛИТИКИ</div>
            <div style="margin-top: 1rem;">
                СОЗДАНО СПЕЦИАЛЬНО ДЛЯ ПРОДВИНУТЫХ ПОЛЬЗОВАТЕЛЕЙ
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()