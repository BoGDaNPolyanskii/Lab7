import psycopg2

# Підключення до БД
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="shop_db",
    user="admin",
    password="root"
)
cur = conn.cursor()

# Створення таблиць
# Таблиця "Клієнти"
cur.execute("""
CREATE TABLE IF NOT EXISTS Clients (
    client_id SERIAL PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    entity_type VARCHAR(10) CHECK (entity_type IN ('юридична', 'фізична')),
    address TEXT,
    phone VARCHAR(15) CHECK (phone SIMILAR TO '\\+380[0-9]{9}'),
    contact_person VARCHAR(50),
    account_number VARCHAR(120) UNIQUE
);
""")

# Таблиця "Товари"
cur.execute("""
CREATE TABLE IF NOT EXISTS Products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0
);
""")

# Таблиця "Продаж товарів"
cur.execute("""
CREATE TABLE IF NOT EXISTS Sales (
    sale_id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL,
    client_id INT REFERENCES Clients(client_id),
    product_id INT REFERENCES Products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    discount DECIMAL(3, 2) CHECK (discount BETWEEN 0.03 AND 0.20),
    payment_form VARCHAR(15) CHECK (payment_form IN ('готівковий', 'безготівковий')),
    delivery_needed BOOLEAN DEFAULT FALSE,
    delivery_cost DECIMAL(10, 2) DEFAULT 0
);
""")


# Додавання клієнтів
cur.execute("""
INSERT INTO Clients (client_name, entity_type, address, phone, contact_person, account_number)
VALUES
('ТОВ "Будматеріали"', 'юридична', 'м. Київ, вул. Центральна, 10', '+380123456789', 'Іван Петрович', '123456789012'),
('ФОП "Сидоров"', 'фізична', 'м. Львів, вул. Степана, 23', '+380987654321', 'Сидоренко С.С.', '987654321098'),
('ТОВ "Електроніка"', 'юридична', 'м. Харків, вул. Академічна, 45', '+380999999999', 'Олена Іванівна', '113416111111'),
('ФОП "Іванов"', 'фізична', 'м. Одеса, вул. Головна, 5', '+380555555555', 'Іванов І.І.', '224622222222');
""")

# Додавання товарів
cur.execute("""
INSERT INTO Products (product_name, price, stock)
VALUES
('Цегла', 10.50, 100),
('Бетон', 50.00, 200),
('Плитка', 25.30, 500),
('Лампочки', 5.99, 200),
('Дошки', 12.00, 300),
('Шурупи', 0.50, 1000),
('Гіпсокартон', 30.00, 500),
('Шпаклівка', 15.00, 1500),
('Фарба', 25.00, 750),
('Цемент', 60.00, 300);
""")

# Додавання продажів
cur.execute("""
INSERT INTO Sales (sale_date, client_id, product_id, quantity, discount, payment_form, delivery_needed, delivery_cost)
VALUES
('2024-10-01', 1, 1, 5, 0.10, 'готівковий', TRUE, 100),
('2024-10-02', 2, 3, 10, 0.15, 'безготівковий', FALSE, 0),
('2024-10-03', 3, 2, 3, 0.05, 'готівковий', TRUE, 50),
('2024-10-04', 4, 4, 20, 0.20, 'готівковий', FALSE, 0),
('2024-10-05', 1, 2, 2, 0.10, 'безготівковий', TRUE, 75),
('2024-10-06', 2, 1, 8, 0.12, 'готівковий', FALSE, 0),
('2024-10-07', 3, 3, 15, 0.07, 'безготівковий', TRUE, 100),
('2024-10-08', 4, 2, 10, 0.10, 'готівковий', FALSE, 0),
('2024-10-09', 1, 4, 5, 0.05, 'готівковий', TRUE, 60),
('2024-10-10', 2, 3, 7, 0.15, 'безготівковий', TRUE, 120),
('2024-10-11', 3, 1, 3, 0.08, 'готівковий', FALSE, 0),
('2024-10-12', 4, 2, 6, 0.20, 'готівковий', TRUE, 50),
('2024-10-13', 1, 3, 9, 0.10, 'безготівковий', FALSE, 0),
('2024-10-14', 2, 4, 4, 0.05, 'готівковий', TRUE, 80),
('2024-10-15', 3, 2, 12, 0.15, 'готівковий', FALSE, 0),
('2024-10-16', 4, 1, 7, 0.07, 'безготівковий', TRUE, 100),
('2024-10-17', 1, 2, 11, 0.10, 'готівковий', TRUE, 90),
('2024-10-18', 2, 4, 13, 0.20, 'безготівковий', FALSE, 0),
('2024-10-19', 3, 3, 8, 0.12, 'готівковий', TRUE, 70);
""")

conn.commit()
cur.close()
conn.close()
print("Таблиці бази даних успішно створені!")
