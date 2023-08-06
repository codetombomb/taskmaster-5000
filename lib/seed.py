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
    import ipdb

    ipdb.set_trace()
