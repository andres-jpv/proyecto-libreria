from odoo import fields, models


class LibraryEtiqueta(models.Model):
    _name = 'library.etiqueta'
    _description = 'Etiqueta de Libro'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color')
