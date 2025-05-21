from datetime import date, timedelta

def reset_weekly_progress(habit):
    today = date.today()
    if habit.last_reset_date is None or (today - habit.last_reset_date).days >= 7:
        habit.completion_count = 0
        habit.last_reset_date = today