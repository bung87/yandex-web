
from datetime import datetime
from cached_property import cached_property
from dateutil.tz import gettz
from tzlocal import get_localzone
from .exceptions import TimeoutException

class Datetime:
    def __init__(self,ctime):
        self.datetime_now = datetime.fromtimestamp(ctime)

    def now(self):
        return self.datetime_now

class DatetimeMixin:

    def _ctime_now(self):
        s = 'var d=new Date();return d.getTime()/1000+d.getTimezoneOffset()'
        r = self.driver.execute_script(s)
        return float(r)

    @property
    def datetime(self):
        return Datetime( self._ctime_now() )

    @cached_property
    def timezone(self):
        js = "return Intl.DateTimeFormat().resolvedOptions().timeZone"
        try:
            tz = self.driver.execute_script(js)
        except TimeoutException:
            local = get_localzone()
            tz = local.zone
        return tz

    def get_date(self):
        s = 'var d=new Date();return d.toISOString().split("T")[0]'
        return self.driver.execute_script(s)

    @cached_property
    def tzinfo(self):
        return gettz(self.timezone)

class InterationMixin:

    def locate(self):
        self.element.location_once_scrolled_into_view

    def locate_and_click(self):
        self.element.location_once_scrolled_into_view
        self.element.click()
    

    