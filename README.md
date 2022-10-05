# Авіакомпанія

# Сутності:

1. Ticket
2. Flight
3. Passenger
3. Contacts
4. Mgr

Role:
1. Client
2. Mgr
# короткий опис:

Кількість місць на рейсі обмежена
У клієнтів є можливість реєстрації на рейс( введення особистих даних на сайті , отримання місця, бронювання додаткового багаж., інфа по кількості вільних місць, отримання знижки,якщо до вильоту певна кількість днів, вислати їм виписані квитки на пошту )
Менеджер АК може переглядати кількість вже заброньованих/ще вільних місць, дані про пасажирів.

# Ticket:
- add_info//mgr, client
- get_info (about ticket details)//mgr, client
- get_discount//client
- get_numberofsit//client

# Flight

- get_flight_info//client,mgr
- get_maxsits//mgr,client
- check_count_freesits//mgr, client
- check_usedsits//mgr

# User
- registration
- login
- logout

# Passenger

- add_personal_info//mgr,client
- get_allinfo//mgr,client
- update_info//mgr,client
- cancel_book//mgr,client

# Contacts

- getcontacts//mgr, client

# Mgr
- login
- logout
- get_allpassengersinfo//mgr

![image](https://user-images.githubusercontent.com/113307928/193950619-b9c5050b-997b-4367-8810-3691e0eab379.png)




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
