import os
import asyncio
import websockets
import json

connected_clients = set()

async def handle_connection(websocket, path):
    """Обрабатываем подключение клиента."""
    connected_clients.add(websocket)
    print(f"Клиент подключился: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Получено сообщение: {message}")
            data = json.loads(message)

            if "sender" in data and "text" in data and "timestamp" in data:
                await broadcast_message(message)
            else:
                print("Неверный формат сообщения:", data)
    except websockets.ConnectionClosed:
        print(f"Клиент отключился: {websocket.remote_address}")
    finally:
        connected_clients.remove(websocket)

async def broadcast_message(message):
    """Рассылаем сообщение всем подключенным клиентам."""
    if connected_clients:
        # Используем asyncio.gather вместо asyncio.wait
        await asyncio.gather(
            *(client.send(message) for client in connected_clients)
        )

async def main():
    """Основной метод запуска сервера."""
    port = int(os.environ.get("PORT", 8080))  # Получаем порт из переменной окружения
    print(f"Сервер запущен на ws://0.0.0.0:{port}")
    async with websockets.serve(handle_connection, "0.0.0.0", port):
        await asyncio.Future()  # Блокировка выполнения

if __name__ == "__main__":
    asyncio.run(main())
