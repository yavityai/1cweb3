# 1cweb3

# FastApiServer

FastApiServer — это серверное приложение, построенное на основе [FastAPI](https://fastapi.tiangolo.com/).  API нужен для интеграции 1C с Web3.

## Требования
Для запуска FastAPI убедитесь, что у вас установлены следующие компоненты:

- **Python**: 3.8 или выше
- **Git**: Для клонирования репозитория
- 
## Установка

### 1. Клонируйте репозиторий

git clone https://github.com/yavityai/1cweb3.git
cd 1cweb3/FastApiServer

### 2. Установите зависимости

pip install -r requirements.txt

### 3. Настройте конфиг API 

Измените файл config.json в директории FastApiServer

- Замените YOUR_ALCHEMY_API_KEY на ваш ключ API от Alchemy или другого провайдера.
- Укажите актуальные адреса токенов и их параметры в разделе tokens.

### 4. Запустите сервер

uvicorn main:app --reload

### 5. Проверьте API

Откройте браузер и перейдите по адресу http://127.0.0.1:8000/docs для доступа к интерактивной документации Swagger.
Альтернативно, используйте http://127.0.0.1:8000/redoc для документации ReDoc






