import csv
from datetime import datetime

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"


def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and Celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees Celcius."
    """
    return f"{temp}{DEGREE_SYMBOL}"


def convert_date(iso_string):
    """Converts and ISO formatted date into a human-readable format.

    Args:
        iso_string: An ISO date string.
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    return datetime.fromisoformat(iso_string).strftime("%A %d %B %Y")


def convert_f_to_c(temp_in_fahrenheit):
    """Converts a temperature from Fahrenheit to Celcius.

    Args:
        temp_in_fahrenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees Celcius, rounded to 1 decimal place.
    """
    # Convert to float to handle string inputs
    temp_f = (float(temp_in_fahrenheit) - 32) * 5 / 9
    return round(temp_f, 1)


def calculate_mean(weather_data):
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """
    # Convert all values to float for calculation
    float_data = [float(x) for x in weather_data]
    average = sum(float_data) / len(float_data)
    return average

def load_data_from_csv(csv_file):
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """
    data = []
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:
            if row:  # Skip empty rows
                # Convert numeric columns to integers
                processed_row = [row[0], int(row[1]), int(row[2])]
                data.append(processed_row)
    return data


def find_min(weather_data):
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minimum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:
        return ()
    
    # Convert all values to float for comparison
    float_data = [float(x) for x in weather_data]
    min_value = min(float_data)
    
    # Find the last occurrence of the minimum value
    last_index = len(float_data) - 1 - float_data[::-1].index(min_value)
    
    return (min_value, last_index)


def find_max(weather_data):
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:
        return ()
    
    # Convert all values to float for comparison
    float_data = [float(x) for x in weather_data]
    max_value = max(float_data)
    
    # Find the last occurrence of the maximum value
    last_index = len(float_data) - 1 - float_data[::-1].index(max_value)
    
    return (max_value, last_index)


def generate_summary(weather_data):
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    if not weather_data:
        return ""
    
    # Extract min and max temperatures
    min_temps = [float(day[1]) for day in weather_data]
    max_temps = [float(day[2]) for day in weather_data]
    
    # Find overall minimum and maximum temperatures
    overall_min, min_index = find_min(min_temps)
    overall_max, max_index = find_max(max_temps)
    
    # Convert to Celsius
    overall_min_c = convert_f_to_c(overall_min)
    overall_max_c = convert_f_to_c(overall_max)
    
    # Get the dates for min and max
    min_date = convert_date(weather_data[min_index][0])
    max_date = convert_date(weather_data[max_index][0])
    
    # Calculate averages and round to 1 decimal place
    avg_low = round(calculate_mean([convert_f_to_c(temp) for temp in min_temps]), 1)
    avg_high = round(calculate_mean([convert_f_to_c(temp) for temp in max_temps]), 1)
    
    # Format the summary
    num_days = len(weather_data)
    summary = f"{num_days} Day Overview\n"
    summary += f"  The lowest temperature will be {format_temperature(overall_min_c)}, and will occur on {min_date}.\n"
    summary += f"  The highest temperature will be {format_temperature(overall_max_c)}, and will occur on {max_date}.\n"
    summary += f"  The average low this week is {format_temperature(avg_low)}.\n"
    summary += f"  The average high this week is {format_temperature(avg_high)}.\n"
    
    return summary


def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    if not weather_data:
        return ""
    
    summary = ""
    
    for day in weather_data:
        date_str = convert_date(day[0])
        min_temp_f = float(day[1])
        max_temp_f = float(day[2])
        
        # Convert to Celsius
        min_temp_c = convert_f_to_c(min_temp_f)
        max_temp_c = convert_f_to_c(max_temp_f)
        
        # Format the daily summary
        summary += f"---- {date_str} ----\n"
        summary += f"  Minimum Temperature: {format_temperature(min_temp_c)}\n"
        summary += f"  Maximum Temperature: {format_temperature(max_temp_c)}\n\n"
    
    return summary
