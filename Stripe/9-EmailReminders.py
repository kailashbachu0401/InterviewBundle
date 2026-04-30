email_rules = {
    "subscribed": 0,
    "reminder": [-7, -3, -1],
    "expired": 0
}

subscriptions = [
    {"user_id": "u1", "start_date": "2025-01-01", "end_date": "2025-01-10"},
    {"user_id": "u2", "start_date": "2025-01-05", "end_date": "2025-01-08"},
]

from datetime import datetime, timedelta

def offset_date(offset, date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    new_date = dt + timedelta(days = offset)
    return new_date.strftime("%Y-%m-%d")


def subscribed_email_scheduler(offset, subscriptions):
    subscribed_schedules= []
    for subscription in subscriptions:
        subscribed_schedules.append(
            {
                "user_id": subscription["user_id"],
                "email_type": "subscribed",
                "send_date": offset_date(offset, subscription["start_date"])
            }
        )
    return subscribed_schedules

def expired_email_scheduler(offset, subscriptions):
    expired_schedules = []
    for subscription in subscriptions:
        expired_schedules.append(
            {
                "user_id": subscription["user_id"],
                "email_type": "expired",
                "send_date": offset_date(offset, subscription["end_date"])
            }
        )
    return expired_schedules

def reminder_email_scheduler(offsets, subscriptions):
    reminder_schedules = []
    for subscription in subscriptions:
        for offset in offsets:
            scheduled_date = offset_date(offset, subscription["end_date"])
            if scheduled_date >= subscription["start_date"]:
                reminder_schedules.append(
                    {
                        "user_id": subscription["user_id"],
                        "email_type": "reminder",
                        "send_date": scheduled_date
                    }
                )

    return reminder_schedules


def email_scheduler(email_rules, subscriptions):
    schedules = []
    schedules += subscribed_email_scheduler(email_rules["subscribed"], subscriptions)
    schedules += expired_email_scheduler(email_rules["expired"], subscriptions)
    schedules += reminder_email_scheduler(email_rules["reminder"], subscriptions)
    schedules.sort(key = lambda x: (x["send_date"], x["user_id"], x["email_type"]))
    return schedules

print(email_scheduler(email_rules, subscriptions))


# Priority mapping
# priority ={
#     "subscribed": 0,
#     "reminder": 1,
#     "expired": 2
# }

# schedules.sort(key = lambda x: (x["send_date"], x["user_id"], priority[x["email_type"]]))

# deduplicate_schedules
# def deduplicate_schedules(schedules):
#     seen = set()
#     deduped = []

#     for schedule in schedules:
#         key = (schedule["user_id"], schedule["email_type"], schedule["send_date"])
#         if key in seen:
#             continue
#         seen.add(key)
#         deduped.append(schedule)

#     return deduped