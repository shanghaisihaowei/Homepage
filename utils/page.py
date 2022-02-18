from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import remove_query_param, replace_query_param

class MyPageNumberPagination(PageNumberPagination):
    page_size = 20

    page_query_param = 'page'

    page_size_query_param = 'size'

    max_page_size = 20

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        # ssl = self.request.META.get('HTTP_REFERER') # Referer
        url_check = url.split('/', 3)
        # ssl_check = ssl.split(':', 1)
        # res_url = ssl_check[0] + url_check[1]
        page_number = self.page.next_page_number()
        return replace_query_param(url_check[-1], self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        # ssl = self.request.META.get('HTTP_REFERER')
        url_check = url.split('/', 3)
        # ssl_check = ssl.split(':', 1)
        # res_url = ssl_check[0] + url_check[1]
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url_check[-1], self.page_query_param)
        return replace_query_param(url_check[-1], self.page_query_param, page_number)