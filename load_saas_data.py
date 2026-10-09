import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker
from sqlalchemy import create_engine

# Initialize Faker & Seeds for reproducibility
fake = Faker()
Faker.seed(42)
np.random.seed(42)

NUM_USERS = 5000
START_DATE = datetime(2026, 1, 1)

print("Generating synthetic SaaS user data...")
users = []
plans = ["Free_Trial", "Pro_Monthly", "Enterprise_Annual"]

for user_id in range(1001, 1001 + NUM_USERS):
    signup = fake.date_time_between(start_date=START_DATE, end_date="now")
    plan = np.random.choice(plans, p=[0.70, 0.22, 0.08])
    users.append(
        {
            "user_id": user_id,
            "company_name": fake.company(),
            "industry": random.choice(
                ["Fintech", "Healthcare", "E-commerce", "EdTech", "SaaS"]
            ),
            "signup_date": signup,
            "plan_tier": plan,
            "country": fake.country_code(),
        }
    )

df_users = pd.DataFrame(users)

print("Generating product event logs & onboarding funnels...")
events = []
event_types = [
    "signup_completed",
    "profile_setup",
    "team_invite_sent",
    "integration_connected",
    "first_campaign_launched",
]

for _, user in df_users.iterrows():
    u_id = user["user_id"]
    base_time = user["signup_date"]
    
    # Realistic funnel drop-off probabilities per step
    drop_off_probs = [1.0, 0.80, 0.50, 0.30, 0.15]

    for idx, event_name in enumerate(event_types):
        if random.random() <= drop_off_probs[idx]:
            event_time = base_time + timedelta(hours=random.randint(2, 72) * (idx + 1))
            events.append(
                {
                    "event_id": fake.uuid4(),
                    "user_id": u_id,
                    "event_name": event_name,
                    "event_timestamp": event_time,
                }
            )
        else:
            break

df_events = pd.DataFrame(events)

# Connect to local PostgreSQL database and load tables
print("Loading data into PostgreSQL database: saas_growth_analytics...")
engine = create_engine(
    "postgresql://tejdeepreddygudise@localhost:5432/saas_growth_analytics"
)

df_users.to_sql("users", engine, if_exists="replace", index=False)
df_events.to_sql("events_log", engine, if_exists="replace", index=False)

print("Success! Data successfully generated and loaded into PostgreSQL.")