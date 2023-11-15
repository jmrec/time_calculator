def determine_current_day(start_day, number_of_days_lapsed):
    name_of_days_in_a_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    adjusted_day = name_of_days_in_a_week[
        (name_of_days_in_a_week.index(start_day) + number_of_days_lapsed)
        % 7
        ] 
    return adjusted_day

def rendered_date(hour, minutes, time_phase, number_of_days_lapsed, current_day=None):
    if hour == 0:
        hour = 12
    if len(str(minutes)) == 1:
        minutes = "0" + str(minutes)

    if current_day is None:
        if number_of_days_lapsed == 0:
            return f"{hour}:{minutes} {time_phase}"
        elif number_of_days_lapsed == 1:
            return f"{hour}:{minutes} {time_phase} (next day)"
        else:
            return f"{hour}:{minutes} {time_phase} ({number_of_days_lapsed} days later)"
    else:
        if number_of_days_lapsed == 0:
            return f"{hour}:{minutes} {time_phase}, {current_day}"
        elif number_of_days_lapsed == 1:
            return f"{hour}:{minutes} {time_phase}, {current_day} (next day)"
        else:
            return f"{hour}:{minutes} {time_phase}, {current_day} ({number_of_days_lapsed} days later)"

def determine_number_of_days_lapsed(hour_start, phase_of_day, hour_duration):
    if phase_of_day == "AM":
        return (hour_duration + hour_start) // 24
    else:
        return (hour_duration + (hour_start + 12)) // 24

def get_time_phase(time_start_with_phase):
    return time_start_with_phase.split()[1]

def get_time_start(time_start_with_phase):
    return time_start_with_phase.split()[0]

def get_hour(specified_time):
    hour = specified_time.split(":")[0]
    if hour == 12:
        return 0
    else:
        return hour

def add_1_to_hour_each_time_minutes_reach_60(total_minutes):
    return total_minutes // 60

def invert_time_phase(time_phase):
    match time_phase:
        case "AM":
            return "PM"
        case "PM":
            return "AM"

def have_to_invert_time_phase(hour_start, hour_duration, number_of_days_lapsed, time_phase):
    if number_of_days_lapsed > 0:
        if time_phase == "AM":
            return (hour_duration + hour_start) % 24 >= 12
        else:
            return (hour_duration + (hour_start - 12)) % 24 < 12
    else:
        return hour_duration >= (12 - hour_start)

def get_minute(specified_time):
    return specified_time.split(":")[1]

def add_time(time_start_with_phase, time_duration, start_day=None):
    time_start = get_time_start(time_start_with_phase)
    time_phase = get_time_phase(time_start_with_phase)

    hour_start = int(get_hour(time_start))
    minute_start = int(get_minute(time_start))

    hour_duration = int(get_hour(time_duration))
    minute_duration = int(get_minute(time_duration))

    hour_duration += add_1_to_hour_each_time_minutes_reach_60(
        minute_start + minute_duration
    )

    number_of_days_lapsed = determine_number_of_days_lapsed(
        hour_start, time_phase, hour_duration
        )

    if have_to_invert_time_phase(
        hour_start, hour_duration, number_of_days_lapsed, time_phase
        ): 
        time_phase = invert_time_phase(time_phase)

    if start_day is None:
        return rendered_date(
            hour= (hour_start + hour_duration) % 12,
            minutes= (minute_start + minute_duration) % 60,
            time_phase= time_phase,
            number_of_days_lapsed= number_of_days_lapsed,
        )
    else:
        current_day = determine_current_day(start_day.capitalize(), number_of_days_lapsed)

        return rendered_date(
            hour= (hour_start + hour_duration) % 12,
            minutes= (minute_start + minute_duration) % 60,
            time_phase= time_phase,
            number_of_days_lapsed= number_of_days_lapsed,
            current_day= current_day
        )
