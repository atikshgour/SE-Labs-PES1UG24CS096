import math


def _parts(text, separator):
    if not isinstance(text, str):
        raise ValueError("input must be text")
    parts = text.split(separator)
    if len(parts) != 2 or not all(part.strip() for part in parts):
        raise ValueError(f"expected two nonempty values separated by {separator!r}")
    return parts


def _nonnegative_number(text, label):
    try:
        value = float(text)
    except ValueError as exc:
        raise ValueError(f"invalid {label}") from exc
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"invalid {label}")
    return value


def parse_zone(text):
    name, area_text = _parts(text, ':')
    area = _nonnegative_number(area_text, "area")
    if area == 0:
        raise ValueError("area must be positive")
    return name.strip().title(), area

def moisture_average(readings_csv):
    if not isinstance(readings_csv, str) or not readings_csv.strip():
        raise ValueError("readings must be nonempty text")
    readings = readings_csv.split(',')
    if not all(reading.strip() for reading in readings):
        raise ValueError("readings must not be empty")
    values = [int(reading) for reading in readings]
    if any(value < 0 or value > 100 for value in values):
        raise ValueError("moisture readings must be between 0 and 100")
    return sum(values) // len(values)

def water_needed(text):
    plot, rain = _parts(text, '|')
    area = _nonnegative_number(plot, "area")
    rainfall = _nonnegative_number(rain, "rainfall")
    need = area * 5 - rainfall
    if not math.isfinite(need):
        raise ValueError("water calculation overflowed")
    return max(need, 0)

def main():
    print("==== Running parse_zone ====")
    user_input = input("Enter zone:area in m2 (e.g. north:120): ")
    result = parse_zone(user_input)
    print("Zone and Area:", result)

    print("\n==== Running moisture_average ====")
    user_input = input("Enter moisture readings as CSV (e.g. 40,35,50): ")
    result = moisture_average(user_input)
    print("Average Moisture:", result)

    print("\n==== Running water_needed ====")
    user_input = input("Enter area|rainfall (e.g. 120|8): ")
    result = water_needed(user_input)
    print("Water Needed:", result)

if __name__ == "__main__":
    main()
