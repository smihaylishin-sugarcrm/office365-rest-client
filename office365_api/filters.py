# -*- coding: utf-8 -*-
class BaseFilter(object):

    def __init__(self, order_by=[], filter_by=[], select=[], custom_qs=''):
        self.order_by = order_by
        self.filter_by = filter_by
        self.select = select
        self.custom_qs = custom_qs

    def get_query_string(self):
        qs_list = [
            '$orderby={}'.format(','.join(self.order_by)) if self.order_by else '',
            '$filter={}'.format(' AND '.join(self.filter_by)) if self.filter_by else '',
            '$select={}'.format(','.join(self.select)) if self.select else ''
        ]
        qs_list.extend([(k + '=' + str(self.custom_qs[k])) for k in self.custom_qs])
        qs = '&'.join([qs for qs in qs_list if qs])
        return qs.replace(' ', '+')
