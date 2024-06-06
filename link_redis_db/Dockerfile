# Використовуйте офіційний образ PostgreSQL з Docker Hub
FROM redis:latest

# Встановіть користувача, пароль та базу даних
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=microservices

# Відкрийте порт для з'єднань PostgreSQL
EXPOSE 5432

# Копіюйте SQL-файли для ініціалізації бази даних
COPY init.sql /docker-entrypoint-initdb.d/

# CMD вказує на команду, яку виконуватиме контейнер при запуску
CMD ["postgres"]