from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.driver.models import Driver, DriverClassEnum
from src.house.models import House

def seed_drivers():
    db: Session = SessionLocal()
    try:
        drivers = [
            ("Иванов Иван Иванович", "+7(910) 123 45-67", "Toyota Camry", DriverClassEnum.econom),
            ("Петров Петр Петрович", "+7(911) 234 56-78", "Honda Accord", DriverClassEnum.comfortable),
            ("Сидоров Сидор Сидорович", "+7(912) 345 67-89", "Ford Focus", DriverClassEnum.business),
            ("Смирнов Смирнова Смирновна", "+7(913) 456 78-90", "Chevrolet Malibu", DriverClassEnum.econom),
            ("Кузнецов Алексей Викторович", "+7(914) 567 89-01", "Volkswagen Passat", DriverClassEnum.comfortable),
            ("Попов Артем Сергеевич", "+7(915) 678 90-12", "Renault Duster", DriverClassEnum.business),
            ("Васильев Сергей Анатольевич", "+7(916) 789 01-23", "Nissan Qashqai", DriverClassEnum.econom),
            ("Зайцев Андрей Олегович", "+7(917) 890 12-34", "Kia Sportage", DriverClassEnum.comfortable),
            ("Михайлов Михаил Дмитриевич", "+7(918) 901 23-45", "Subaru Forester", DriverClassEnum.business),
            ("Лебедев Игорь Николаевич", "+7(919) 012 34-56", "Hyundai Tucson", DriverClassEnum.econom),
            ("Федоров Николай Юрьевич", "+7(920) 123 45-67", "Mazda CX-5", DriverClassEnum.comfortable),
            ("Морозов Антон Павлович", "+7(921) 234 56-78", "BMW 3 Series", DriverClassEnum.business),
            ("Соловьев Валерий Владимирович", "+7(922) 345 67-89", "Mercedes-Benz C-Class", DriverClassEnum.econom),
            ("Чернов Виктор Игоревич", "+7(923) 456 78-90", "Audi A4", DriverClassEnum.comfortable),
            ("Тихонов Вячеслав Сергеевич", "+7(924) 567 89-01", "Lexus ES", DriverClassEnum.business),
            ("Петрова Ольга Ивановна", "+7(925) 678 90-12", "Volkswagen Tiguan", DriverClassEnum.econom),
            ("Синицын Дмитрий Владимирович", "+7(926) 789 01-23", "Skoda Kodiaq", DriverClassEnum.comfortable),
            ("Григорьев Денис Андреевич", "+7(927) 890 12-34", "Opel Astra", DriverClassEnum.business),
            ("Ковалев Арсений Александрович", "+7(928) 901 23-45", "Toyota RAV4", DriverClassEnum.econom),
            ("Николаев Роман Сергеевич", "+7(929) 012 34-56", "Honda CR-V", DriverClassEnum.comfortable),
            ("Белов Василий Николаевич", "+7(930) 123 45-67", "Nissan X-Trail", DriverClassEnum.business),
            ("Лысенко Сергей Иванович", "+7(931) 234 56-78", "Ford Kuga", DriverClassEnum.econom),
            ("Костин Юрий Васильевич", "+7(932) 345 67-89", "Citroën C4", DriverClassEnum.comfortable),
            ("Захаров Виктор Петрович", "+7(933) 456 78-90", "Renault Koleos", DriverClassEnum.business),
            ("Романов Павел Игоревич", "+7(934) 567 89-01", "Kia Seltos", DriverClassEnum.econom),
        ]

        for name, tel, car, driver_class in drivers:
            driver = Driver(name=name, tel=tel, car=car, driver_class=driver_class)
            db.add(driver)

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Произошла ошибка: {e}")
    finally:
        db.close()

def seed_houses():
    db: Session = SessionLocal()
    try:
        houses = [
            ("12A", "1", "ул. Ленина"),
            ("3", None, "ул. Пушкина"),
            ("45Б", "2", "ул. Гоголя"),
            ("17", None, "ул. Садовая"),
            ("8", "1", "пр. Мира"),
            ("101A", None, "ул. Красная"),
            ("22", "3", "ул. Октябрьская"),
            ("5", None, "ул. Комсомольская"),
            ("19", "1", "ул. Советская"),
            ("28", "2", "ул. Гагарина"),
            ("33", None, "ул. Тимирязева"),
            ("7A", "1", "ул. Беринга"),
            ("14", None, "ул. Чехова"),
            ("26Б", "1", "ул. Степана Разина"),
            ("37", None, "ул. Кленовая"),
            ("9", "2", "ул. Полярная"),
            ("50А", None, "ул. Лесная"),
            ("11", "1", "ул. Центральная"),
            ("32", None, "ул. Дружбы"),
            ("4", "2", "ул. Уральская"),
            ("44", None, "ул. Ломоносова"),
            ("30А", "1", "ул. Солнечная"),
            ("18", None, "ул. Новая"),
            ("25", "1", "ул. Восточная"),
            ("60Б", None, "ул. Западная"),
            ("1", None, "ул. Ленина"),
            ("2", None, "ул. Пушкина"),
            ("3", None, "ул. Садовая"),
            ("4А", None, "ул. Мира"),
            ("5", "1", "ул. Кирова"),
            ("6Б", None, "ул. Школьная"),
            ("7", None, "ул. Тихая"),
            ("8", None, "ул. Северная"),
            ("9", "2", "ул. Южная"),
            ("10", None, "ул. Заречная"),
            ("11", None, "ул. Центральная"),
            ("12", None, "ул. Новая"),
            ("13А", None, "ул. Красная"),
            ("14", "3", "ул. Солнечная"),
            ("15Б", None, "ул. Космическая"),
            ("16", None, "ул. Московская"),
            ("17", None, "ул. Лесная"),
            ("18", "1", "ул. Речная"),
            ("19", None, "ул. Тюльпанная"),
            ("20", None, "ул. Зелёная"),
            ("21", None, "ул. Ясеневая"),
            ("22А", None, "ул. Берёзовая"),
            ("23", None, "ул. Фрунзе"),
            ("24", "2", "ул. Гармония"),
            ("25", None, "ул. Промышленная"),
            ("26Б", None, "ул. Западная"),
            ("27", None, "ул. Восточная"),
            ("28", None, "ул. Широкая"),
            ("29", "3", "ул. Кленовая"),
            ("30", None, "ул. Тихая"),
            ("31", None, "ул. Мирная"),
            ("32", None, "ул. Сосновая"),
            ("33А", None, "ул. Рябиновая"),
            ("34", "1", "ул. Набережная"),
            ("35", None, "ул. Солнечная"),
            ("36", None, "ул. Тихая"),
            ("37Б", None, "ул. Лесная"),
            ("38", None, "ул. Космическая"),
            ("39", None, "ул. Новая"),
            ("40А", None, "ул. Тихая"),
            ("41", None, "ул. Садовая"),
            ("42", None, "ул. Центральная"),
            ("43", "1", "ул. Гармония"),
            ("44", None, "ул. Фрунзе"),
            ("45Б", None, "ул. Широкая"),
            ("46", None, "ул. Заречная"),
            ("47", "2", "ул. Красная"),
            ("48", None, "ул. Зелёная"),
            ("49", "3", "ул. Кленовая"),
            ("50", None, "ул. Набережная"),
        ]

        for number, building, street in houses:
            house = House(number=number, building=building, street=street)
            db.add(house)

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Произошла ошибка: {e}")
    finally:
        db.close()

seed_drivers()
seed_houses()