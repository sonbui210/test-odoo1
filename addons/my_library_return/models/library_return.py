from odoo import fields, api, models
from datetime import timedelta

class LibraryBook(models.Model):
    _inherit = "library.book"

    date_return = fields.Date("Date to return")

    def make_borrerd(self):
        day_to_borrow = self.categort_id.max_borrow_days or 10
        self.date_return = fields.Date.today() + timedelta(days=day_to_borrow)
        return super(LibraryBook, self).make_borrerd()
    def make_available(self):
        self.date_return=False
        return super(LibraryBook, self).make_available()


class LibraryBookCategory(models.Model):
    _inherit = "library.book.category"

    max_borrow_days=fields.Integer(
        "Max borrow days",
        help="For how many day can be borrwed",
        default=10
    )
