
import streamlit as st
from telethon import functions, errors
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
import traceback
import asyncio
from event_loop import run_async, LOOP
from auth import TelegramAuth, show_auth_page

async def check_scammer(auth, username_or_id):
    """Проверка пользователя на скам через SafeBase_checkbot"""
    try:
        # Проверяем авторизацию перед выполнением запроса
        if not await auth.check_auth():
            st.session_state.is_authenticated = False
            if 'session_file_path' in st.session_state:
                st.info(f"Сессия {st.session_state.session_file_path} устарела или недействительна.")
            return False, "error", "Необходима повторная авторизация в Telegram"
            
        # Проверка соединения с Telegram API
        if not auth.client.is_connected():
            await auth.client.connect()
            if not auth.client.is_connected():
                return False, "error", "Не удалось установить соединение с Telegram API. Пожалуйста, обновите страницу и попробуйте снова."

        # Находим бота SafeBase_checkbot
        bot = await auth.client.get_entity("SafeBase_checkbot")
        
        # Находим каналы для подписки
        safe_base_channel = await auth.client.get_entity("SafeBaseList")
        lisurgutin_channel = await auth.client.get_entity("lisurgutinbio")
        
        # Отправляем /start боту
        await auth.client.send_message(bot, "/start")
        await asyncio.sleep(2)  # Ждем ответа бота
        
        # Подписываемся на каналы
        await auth.client(JoinChannelRequest(safe_base_channel))
        await asyncio.sleep(1)
        await auth.client(JoinChannelRequest(lisurgutin_channel))
        await asyncio.sleep(1)
        
        # Отправляем запрос на проверку
        await auth.client.send_message(bot, f"чек {username_or_id}")
        
        # Ждем ответа бота (с таймаутом 10 секунд)
        response = None
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < 10:
            messages = await auth.client.get_messages(bot, limit=5)
            for message in messages:
                if "чек" in message.text.lower() and username_or_id.lower() in message.text.lower():
                    # Нашли запрос, теперь ищем ответ (должен быть следующим сообщением)
                    response_messages = [m for m in messages if m.id > message.id]
                    if response_messages:
                        response = response_messages[0].text
                        break
            if response:
                break
            await asyncio.sleep(1)
        
        # Выходим из канала SafeBaseList и удаляем историю чата с ботом
        await auth.client(LeaveChannelRequest(safe_base_channel))
        await auth.client(DeleteHistoryRequest(
            peer=bot,
            max_id=0,
            just_clear=True,
            revoke=True
        ))
        
        # Если не получили ответ
        if not response:
            return False, "error", "БОТ НЕ ОТВЕТИЛ НА ЗАПРОС ПРОВЕРКИ. ПОЖАЛУЙСТА, ПОПРОБУЙТЕ ПОЗДНЕЕ ИЛИ УБЕДИТЕСЬ, ЧТО БОТ АКТИВЕН И ДОСТУПЕН. СИСТЕМА БЕЗОПАСНОСТИ TELEGRAM МОЖЕТ ВРЕМЕННО ОГРАНИЧИВАТЬ АВТОМАТИЧЕСКИЕ ЗАПРОСЫ. РЕКОМЕНДУЕТСЯ ПОВТОРИТЬ ПОПЫТКУ ЧЕРЕЗ НЕСКОЛЬКО МИНУТ."
        
        # Анализируем ответ
        if "в нашей базе данных нет записей об этом аккаунте" in response:
            return true, "clean", "аккаунт не найден в базе данных подозрительных пользователей. система анализа профилей не обнаружила признаков мошеннической активности на текущий момент. однако рекомендуется соблюдать стандартные меры предосторожности при взаимодействии с данным пользователем. безопасность ваших данных и средств остается вашей ответственностью. ни при каких обстоятельствах не передавайте конфиденциальную информацию или доступ к вашим счетам третьим лицам."
        elif "данного юзернейма не существует" in response:
            return true, "not_exist", "указанный идентификатор пользователя не существует в системе telegram. проверка невозможна ввиду отсутствия данного аккаунта в сети. пожалуйста, убедитесь в правильности введенных данных и повторите попытку. обратите внимание, что имена пользователей в telegram чувствительны к регистру и должны вводиться без символа '@'. если вы уверены в корректности введенной информации, возможно, аккаунт был удален или заблокирован администрацией telegram."
        elif "скаммер" in response:
            return true, "scammer", "внимание! обнаружена критическая угроза! данный аккаунт находится в базе данных мошенников и представляет высокий риск безопасности. система выявила многочисленные случаи мошеннических действий, связанных с этим пользователем. настоятельно рекомендуется избегать любых взаимодействий с данным аккаунтом, блокировать все контакты и ни при каких обстоятельствах не предоставлять личную информацию или доступ к финансовым инструментам. если вы уже вступили в контакт с этим пользователем, немедленно прекратите общение и свяжитесь со службой поддержки."
        else:
            return true, "unknown", "результат проверки неоднозначен. система не смогла точно классифицировать статус данного аккаунта в соответствии с установленными критериями безопасности. рекомендуется проявлять повышенную осторожность при взаимодействии с этим пользователем. избегайте передачи конфиденциальной информации, финансовых деталей и доступа к личным аккаунтам. в случае подозрительной активности немедленно прекратите общение и сообщите о возможном нарушении в службу поддержки telegram. \n\n Повторите проверку снова, для получения достоверных сведений."

    except Exception as e:
        error_details = traceback.format_exc()
        st.error(f"Ошибка при проверке: {str(e)}")
        st.error(f"Детали ошибки: {error_details}")
        return False, "error", f"КРИТИЧЕСКАЯ ОШИБКА СИСТЕМЫ ПРИ ВЫПОЛНЕНИИ ПРОВЕРКИ. ТЕХНИЧЕСКАЯ ИНФОРМАЦИЯ: {str(e)}. ПОЖАЛУЙСТА, УБЕДИТЕСЬ В КОРРЕКТНОСТИ ВВЕДЕННЫХ ДАННЫХ И СТАБИЛЬНОСТИ ВАШЕГО ПОДКЛЮЧЕНИЯ К СЕТИ. ЕСЛИ ПРОБЛЕМА СОХРАНЯЕТСЯ, ОБРАТИТЕСЬ К АДМИНИСТРАТОРУ СИСТЕМЫ ИЛИ ПОПРОБУЙТЕ ПОВТОРИТЬ ЗАПРОС ПОЗДНЕЕ."

def show_scam_checker_page():
    """Отображает страницу проверки скамеров"""
    st.title("АНАЛИЗАТОР ПРОФИЛЕЙ TELEGRAM")
    st.markdown("""
    ## РАСШИРЕННАЯ ПРОВЕРКА ПОЛЬЗОВАТЕЛЕЙ

    ВВЕДИТЕ ИМЯ ПОЛЬЗОВАТЕЛЯ (@username) ИЛИ ИДЕНТИФИКАТОР АККАУНТА TELEGRAM ДЛЯ ПОЛНОГО АНАЛИЗА ПРОФИЛЯ. СИСТЕМА ПРОВЕДЕТ КОМПЛЕКСНУЮ ПРОВЕРКУ И ПРЕДОСТАВИТ ДЕТАЛЬНЫЙ ОТЧЕТ О РЕЗУЛЬТАТАХ.
    """)

    with st.form("check_form"):
        username_or_id = st.text_input("Введите ID или имя пользователя:")
        check_button = st.form_submit_button("Проверить")

        if check_button and username_or_id:
            with st.spinner("Проверка пользователя..."):
                success, status, message = run_async(
                    check_scammer(st.session_state.auth, username_or_id)
                )

                if success:
                    st.session_state.check_result = username_or_id
                    st.session_state.check_status = status
                    st.session_state.check_message = message
                else:
                    # Проверяем, что пользователь все еще авторизован
                    if not st.session_state.is_authenticated and "авторизация" in message.lower():
                        st.error(f"Необходима повторная авторизация")
                        st.session_state.auth_stage = 'phone'
                        st.rerun() # Перезапускаем страницу, чтобы отобразить форму авторизации
                    else:
                        st.error(f"Ошибка проверки: {message}")

    # Отображение результатов
    if 'check_result' in st.session_state and st.session_state.check_result:
        st.subheader("Результаты проверки")

        if st.session_state.check_status == "scammer":
            st.error(f"⚠️ ОБНАРУЖЕНА ПОДОЗРИТЕЛЬНАЯ АКТИВНОСТЬ! ПОЛЬЗОВАТЕЛЬ {st.session_state.check_result} ПРИСУТСТВУЕТ В НАШЕЙ БАЗЕ ДАННЫХ!")
            st.markdown(f"{st.session_state.check_message}")
        elif st.session_state.check_status == "clean":
            st.success(f"✅ РЕЗУЛЬТАТ ПРОВЕРКИ: ПОЛЬЗОВАТЕЛЬ {st.session_state.check_result} НЕ ИМЕЕТ ОТРИЦАТЕЛЬНОЙ ИСТОРИИ В НАШЕЙ БАЗЕ ДАННЫХ.")
            st.markdown(f"{st.session_state.check_message}")
        elif st.session_state.check_status == "not_exist":
            st.warning(f"ℹ️ ПОЛЬЗОВАТЕЛЬ {st.session_state.check_result} НЕ СУЩЕСТВУЕТ.")
            st.markdown(f"{st.session_state.check_message}")
        elif st.session_state.check_status == "error":
            st.error(f"❌ АНАЛИЗ НЕ ЗАВЕРШЕН: {st.session_state.check_message}")
        else:
            st.info(f"ℹ️ {st.session_state.check_message}")
