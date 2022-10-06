1. Install python 3.8.2
 - pyenv install 3.8.2
2. Create virtual environment:
 - python3 -m venv venv
3. Activate 
  - venv\Scripts\activate.ps1
4. In order to check which pythin version you are using
  - python --version
  
 ![image](https://user-images.githubusercontent.com/113307928/194427176-2e020990-4307-4e20-b2b2-a33b0bb820ad.png)

5. Запускаємо програму у файлі app.py
6. Копіюєм адресу з цього файлу та вставляємо у браузер




# Авіакомпанія

# Сутності:

1. Ticket
2. Flight
3. Book
4. Passenger
5. User
6. Admin

Role:
1. user
2. user_mgr

# короткий опис:

Кількість місць на рейсі обмежена
У клієнтів є можливість реєстрації на рейси( введення особистих даних на сайті , отримання місця, бронювання додаткового багаж., інфа по кількості вільних місць, отримання знижки,якщо до вильоту певна кількість днів, вислати їм виписані квитки на пошту )
Менеджер-юзер може переглядати кількість вже заброньованих/ще вільних місць, дані про пасажирів.

# User
- create_account
- login
- logout

# Book(order)
- createbook?
- addticket_tobook
- deleteticket
- getTotalPrice//user

# Ticket:
- add_info//mgr, user
- get_info (details about ticket)//mgr, user
- get_discount//mgr, client
- get_numberofsit//mgr,client

# Flight

- get_flight_info//mgr, user
- get_maxsits//mgr,user
- check_count_freesits//mgr, user
- check_usedsits//mgr

# Passenger

- add_personal_info//mgr,client
- update_info//mgr,client
- get_info//mgr,client

# Mgr//user_mgr
- get_allpassengersinfo//mgr

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
