from flask_admin.contrib.sqla.filters import BaseSQLAFilter
from models import *


class FilterByDepartment(BaseSQLAFilter):
    def __init__(self, column, name, *args, **kwargs):
        super(FilterByDepartment, self).__init__(column, name, *args, **kwargs)

    def apply(self, query, value, alias=None):
        if value:
            # Use the LIKE operator for partial matching
            return query.join(Guide).join(Department).filter(Department.dname.like(f'%{value}%'))
        return query

    def operation(self):
        return 'like'
    

class FilterByCurrentStatus(BaseSQLAFilter):
    def __init__(self, column, name, *args, **kwargs):
        super(FilterByCurrentStatus, self).__init__(column, name, *args, **kwargs)

    def apply(self, query, value, alias=None):
        if value:
            return query.join(Status).filter(Status.current_status.like(f'%{value}%'))
        return query

    def operation(self):
        return 'like'

class FilterByTiming(BaseSQLAFilter):
    def __init__(self, column, name, *args, **kwargs):
        super(FilterByTiming, self).__init__(column, name, *args, **kwargs)
        self.options = (("part-time","Part-Time"),("full-time", "Full-Time"))
    
    def apply(self, query, value, alias=None):
        if value:
            return query.filter(Details.timing.like(f"%{value}%"))
        return query
    
    def operation(self):
        return 'like'