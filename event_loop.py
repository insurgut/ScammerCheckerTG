"""
Модуль для управления глобальным циклом событий asyncio
"""
import asyncio
import nest_asyncio
import functools
import streamlit as st
import os

# Применяем nest_asyncio для вложенного использования asyncio
nest_asyncio.apply()

# Единый глобальный цикл событий для всего приложения
LOOP = None

def setup_asyncio():
    """
    Устанавливает глобальный цикл событий для всего приложения.
    Вызывается только один раз при импорте модуля.
    """
    global LOOP
    try:
        LOOP = asyncio.get_event_loop()
    except RuntimeError:
        LOOP = asyncio.new_event_loop()
        asyncio.set_event_loop(LOOP)

# Инициализируем глобальный цикл сразу при импорте модуля
setup_asyncio()

def run_async(coroutine):
    """
    Выполняет асинхронную функцию из синхронного контекста, 
    используя единый глобальный цикл событий.
    
    Args:
        coroutine: Корутина для выполнения
        
    Returns:
        Результат корутины
    """
    global LOOP
    
    try:
        if not LOOP or LOOP.is_closed():
            setup_asyncio()
            
        result = LOOP.run_until_complete(coroutine)
        return result
    except Exception as e:
        st.error(f"Ошибка асинхронного выполнения: {str(e)}")
        raise e
