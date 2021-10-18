# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

logger = logging.getLogger(__name__)

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'


    name = fields.Char('Title', required= True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner', string='Authors')
    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        'State', default="draft")

    category_id = fields.Many2one("library.book.category", string="Category")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                msg = _("Moving from %s to %s is not allowed") %(book.state, new_state)
                raise UserError(msg)

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    def make_draft(self):
        self.change_state('draft')

    def log_all_library_member(self):
        #this is an empty recordset of model
        library_member_model = self.env['library.member']

        all_member = library_member_model.search([])
        print("ALL MEMBERS: ", all_member)
        return True

    def create_categories(self):
        categ1 = {
            "name": "Child category 1",
            "description": "Description for child 1"
        }
        categ2 = {
            "name": "Child category 2",
            "description": " Description for child 2"
        }

        parent_category_val = {
            "name": "Parent category",
            "description": "Description for parent category",
            "child_ids": [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        record = self.env['library.book.category'].create([categ1,categ2])
        return True


    def change_release_date(self):
        self.ensure_one()
        self.update({
            "date_release": fields.Datetime.now(),
        })
        return  True

    def find_book(self):
        domain = [
            '|',
                '&',    ("name", "ilike", "Book Name"),
                        ("category_id.name", "=", "Category Name"),
                '&',    ("name", "ilike", "Book Name 2"),
                        ("category_id.name", "=", "Category Name 2")
        ]
        books = self.search(domain)
        print(books)
        logger.info("Books found: %s", books)
        return True

    def filter_books(self):
        all_book = self.search([])
        filtered_books = self.books_with_multiple_authors(all_book)
        logger.info("Filter Books: %s", filtered_books)
        print(filtered_books)
        return True

    @api.model
    def books_with_multiple_authors(self, all_book):
        def predicate(book):
            if len(book.author_ids) == 1:
                print(book.author_ids)
                return True
        return all_book.filtered(predicate)

    @api.model
    def get_author_names(self, books):
        return books.mapped("author_ids.name")

    def mapped_book(self):
        all_books = self.search([])
        books_authors = self.get_author_names(all_books)
        logger.info("Book authors: %s", books_authors)
        print(books_authors)
        return True


    @api.model
    def sort_books_by_date(self, books):
        return books.sorted(key="date_release")

    def sort_date_release(self):
        all_books = self.search([])
        book_date_release = self.sort_books_by_date(all_books)
        logger.info("Sort book: %s", book_date_release)
        print(book_date_release)
        return True



class LibraryMember(models.Model):
    _name = "library.member"
    _inherits = {"res.partner": "partner_id"}
    _description = "Library member"

    partner_id = fields.Many2one("res.partner", ondelete="cascade")
    date_start = fields.Date("Member Since")
    date_end = fields.Date("Member End")
    member_number = fields.Char()
    date_of_birth = fields.Date("Date of birth")

