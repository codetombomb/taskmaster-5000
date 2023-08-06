from faker import Faker
from datetime import datetime
from models import User, Task
from session import session

fake = Faker()

users = []

for _ in range(20):
    
    fake_first = fake.first_name()
    fake_last = fake.last_name()
    
    users.append(
        User(
            first_name=fake_first,
            last_name=fake_last,
            username=f"{fake_first}_{fake_last}",
            birthday=datetime.strptime(fake.date(), '%Y-%m-%d').date()
        )
    )
    
session.query(User).delete()
session.query(Task).delete()
session.commit()

    
session.bulk_save_objects(users)
session.commit()

all_users = session.query(User).all()
for user in all_users:
    
    for _ in range(5):
        task = Task(
            description=fake.paragraph(nb_sentences=2),
            due_date=datetime.strptime(fake.date(), '%Y-%m-%d').date(),
            user_id=user.id
        )
        session.add(task)
        session.commit()


if __name__ == "__main__":
    
#  SQLAlchemy query with common filters https://rimsovankiry.medium.com/sqlalchemy-query-with-common-filters-c7adbd3321a6
    
# Retrieve all rows from a table. - session.query(User).all()

# Retrieve a specific row by primary key. 
#   - session.query(User).get(10)
#  Alternate - session.query(User).filter_by(id=10).first()
# ---------------------------

# Filter rows based on a column value. 
# - session.query(User).filter(User.last_name.like("W%")).all() 
# - The % sign is a wildcard character, meaning any characters can come after "W".
# ---------------------------

# Retrieve all rows from the User table where the birthday column is between two given dates, for example, between '1990-01-01' and '2000-12-31'.
# - session.query(User).filter(User.birthday.between("1990-01-01", "2000-12-31")).all()
# ---- ALTERNATIVE ----

# from datetime import datetime

# start_date = datetime(1990, 1, 1)
# end_date = datetime(2000, 12, 31)

# result = session.query(User).filter(User.birthday >= start_date, User.birthday <= end_date).all()

# ---------------------------

# Filter rows using multiple conditions (AND, OR).

# Query with case-insensitive filtering. session.query(User).filter(User.last_name.like("W%")).all() 

# Ordering query results.

# Limit the number of rows returned.

# Using the IN operator to filter by multiple values.

# Count the number of rows that match a condition.

# Performing aggregate functions (e.g., SUM, AVG) on a column.

    import ipdb

    ipdb.set_trace()
