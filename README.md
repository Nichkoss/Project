1. Install python 3.8.2
   - pyenv install 3.8.2
2. Create virtual environment:
   - python3 -m venv venv
3. Activate 
   - venv\Scripts\activate.ps1
4. Install requirements.txt:
   - pip install -r requirements.txt
5. In order to check which python version you are using
   - python --version
   ![image](https://user-images.githubusercontent.com/113307928/194427176-2e020990-4307-4e20-b2b2-a33b0bb820ad.png)

6. Запускаємо програму у файлі app.py
   Копіюєм адресу з цього файлу та вставляємо у браузер
   АБО
   Запускаємо програму у файлі app1.py і переходим за виданим посиланням, додаючи /api/v1/hello-world-13.



# Авіакомпанія

# Сутності:
1. User
2. Passenger
3. Book
4. Ticket
5. Sit
6. Flight

# Ролі:
1. role_viewer
2. role_client
3. role_mgr

# Короткий опис:
Кількість місць на рейсі обмежена.
У клієнтів є можливість реєстрації на рейси (введення особистих даних на сайті , отримання місця, бронювання додаткового багаж.
Інфа по кількості вільних місць, отримання знижки, якщо до вильоту певна кількість днів, вислати їм виписані квитки на пошту)
Менеджер-юзер може переглядати кількість вже заброньованих/ще вільних місць, дані про пасажирів.

# User
  - Add // role_viewer
  - UpdatePersonalInfo // role_client, role_mgr
  - Login // role_client, role_mgr
  - Logout // role_client, role_mgr
  - Delete // role_client, role_mgr
  - GetUser // role_client, role_mgr
  - GetAllUsers // role_mgr
  - SetRole // role_mgr

# Book (order)
  - Add // role_client
  - GetBookInfo // role_client, role_mgr
  - UpdateBookInfo // role_client
  - GetDiscount // role_client
  - Delete // role_client

# Ticket
  - AddTicketInfo // role_client
  - UpdateTicketInfo // role_client
  - GetTicketInfo (details about ticket) // role_client, role_mgr
  - DeleteTicketInfo // role_client

# Sit
  - AddSitInfo // role_mgr
  - UpdateSitInfo // role_mgr
  - GetSitInfo // role_client, role_mgr
  - DeleteSitInfo // role_mgr

# Flight
  - AddFlightInfo // role_mgr
  - UpdateFlightInfo // role_mgr
  - GetFlightInfo // role_client, role_mgr
  - DeleteFlightInfo // role_mgr
  - GetFreeSits // role_client, role_mgr
  - GetUsedSits // role_mgr

# Passenger
  - AddPersonalInfo // role_client
  - UpdatePersonalInfo // role_client
  - GetPersonalInfo // role_client, role_mgr
  
  ![image](https://user-images.githubusercontent.com/113307928/194432980-3028bb13-897d-453c-bbe4-c0571ace6bc8.png)
  
Нижче вже неактуально
- скільки пасів букають разом || pass_count
- реєстрація на рейс: прізв., імя, дата нар, серія паспорта, номер паспорта, термін дії паспорта, чи потрбіен дод багаж.   Пошта ,контактний н.т., "галочка" для погодження з умовами. || book_add_info
- відміна бронювання || book_cancel
- редагувати особисті дані? || info_update
- перегляд введених даних на виписаному квитку 
- кількість вільних місць || available_sit

#АК

- адмін вхід? 
- відміна бронювання працівником || cancel_by_al
- кількість доступних місць на рейс || available_sit  // та сама дія, що вище
- кількість вже заброньованих || unavailable_sit
- дані про кожного пасажира на рейсі || passengers_info
- додавати зі своєї сторони нових пасів ||book_add_info // та сама дія, що вище
