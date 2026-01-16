from datetime import datetime

class DateHandler:
    """
    Handles all the heavy lifting with the dates in this program
    It can return proper strings with the current clock and date.

    Additionally, it can also account for timezones :)
    """
    def __init__(self) -> None:
        """
        __init__ Initializes the DateHandler
        """
        self.tz = datetime.now().astimezone().tzinfo
        self.date = datetime.now()
        self.tzname = datetime.tzname(self.date)

    def update_datetime(self) -> None:
        """
        update_datetime Updates the current datetime.
        """
        self.date = datetime.now(self.tz)

    @property
    # @_update_datetime (wenn ich decorator benutze dann kracht es gewaltig)
    def clock_string(self) -> str:
        """
        clock_string Returns the current time as a string.
        You can also modify the elements in the string.

        Right now, it only returns the Hour and Minute in the
        
        `Hour:Minute` format. For further information check the
        datetime.strftime() function.

        Returns:
            Time as string
        """
        return self.date.strftime("%H:%M")
    
    @property
    # @_update_datetime
    def date_string(self) -> str:
        """
        date_string Returns the current date as a string.

        Just like with the clock_string() you can also modify
        the elements and format on this one aswell.

        By default, it returns a string that looks like this:
        `Weekday: Day.Month.Year`

        Returns:
            Current date as string.
        """
        return self.date.strftime("%a: %d.%m.%Y")