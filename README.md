# AfanasievBarbershop

Это веб-приложение на базе Django для составления расписания работы мастеров в различных филлиалах.

## Функции

- **Управление расписанием**: мастера могут создавать расписание на месяц, редактировать его, контролировать рабочее время.
- **Управление мастерами**: администраторы могут изменять расписание, контролировать рабочее время мастеров. Регистрировать мастеров и удалять.
- **Управление филиалами**: директор имеет все полномчии администратора, а так же может создавать, редактировать и удалять филиалы, назначать администраторов.

## Предварительные требования
  * Python 3.11(не ниже) 
 
## Технологии проекта

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
  
## Установка

1. **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Ryize/AfanasievBarbershop.git
    cd AfanasievBarbershop
    ```

2. **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # для Linux и macOS
    venv\Scripts\activate  # для Windows
    ```

3. **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Создайте миграции базы данных:**
    ```bash
    python3 manage.py makemigrations
    ```

5. **Примените миграции базы данных:**
    ```bash
    python3 manage.py migrate
    ```

6. **Создайте суперпользователя для доступа к административной панели:**
    ```bash
    python3 manage.py createsuperuser
    ```

7. **Запустите сервер разработки:**
    ```bash
    python3 manage.py runserver
    ```

8. **Перейдите по адресу в браузере:**
    ```
    http://127.0.0.1:8000/
    ```




Спасибо, что используете AfanasievBarbershop! Мы надеемся, что это приложение упростит управление вашим барбершопом.
