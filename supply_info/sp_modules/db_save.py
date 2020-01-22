from supply_info.models import Event



def event_record(user, action):
    event = Event(
        user_name=user,
        event_name=action
    )
    event.save()


