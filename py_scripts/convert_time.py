def convert_hours_to_days_hours_minutes(hours):
    days = int(hours // 24)
    remaining_hours = hours % 24
    minutes = int((remaining_hours - int(remaining_hours)) * 60)
    return days, int(remaining_hours), minutes
