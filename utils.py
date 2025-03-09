import asyncio
import functools
import concurrent.futures
import streamlit as st

def async_to_sync(func):
    """
    Декоратор для преобразования асинхронной функции в синхронную
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper

# Импортируем функцию run_async из event_loop.py вместо своей реализации
from event_loop import run_async

def handle_exception(func):
    """
    Декоратор для обработки исключений и отображения сообщений об ошибках
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
            return None
    return wrapper
