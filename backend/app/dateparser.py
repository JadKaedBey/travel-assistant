from datetime import datetime, timedelta
from dateutil.parser import parse

def parse_date(date_str: str) -> datetime.date:
    date_str = date_str.strip().lower()
    if date_str == "today":
        return datetime.now().date()
    elif date_str == "tomorrow":
        return (datetime.now() + timedelta(days=1)).date()
    else:
        try:
            # Parse the date string to a datetime object
            parsed_date = parse(date_str, fuzzy=True, default=datetime(datetime.now().year, 1, 1))
            # If no year was explicitly provided, it defaults to the current year
            if parsed_date.year == 1900:  # Common default year used by `dateutil`
                parsed_date = parsed_date.replace(year=datetime.now().year)
            return parsed_date.date()
        except ValueError:
            raise ValueError(f"Could not parse date string: {date_str}")
        
def get_start_end_date(parsed_date):
  start_date = parsed_date.replace(hour=0, minute=0, second=0, microsecond=0)
  end_date = parsed_date.replace(hour=23, minute=59, second=59, microsecond=0)
  return start_date.isoformat(), end_date.isoformat()