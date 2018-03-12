from django.core.paginator import Paginator

MARGIN_PAGES_DISPLAYED = 2
PAGE_RANGE_DISPLAYED = 2

class MyPaginator(Paginator):
    
    def my_range(self, number):
        if self.num_pages <= PAGE_RANGE_DISPLAYED:
            return range(1, self.num_pages + 1)
        if number == 1:
            return range(1, number + PAGE_RANGE_DISPLAYED + 1)
        if number == self.num_pages:
            return range(number - PAGE_RANGE_DISPLAYED, number + 1)
           
        left_side = int(PAGE_RANGE_DISPLAYED / 2)
        right_side = PAGE_RANGE_DISPLAYED - left_side

        if number - left_side <= 0:
            return range(1, 2 + PAGE_RANGE_DISPLAYED)

        if abs(number - self.num_pages) < right_side:
            return range(self.num_pages - PAGE_RANGE_DISPLAYED ,self.num_pages + 1)    

        return range(number - left_side, number + 1 + right_side)

    

            


                                
