from odoo import models, fields, api


class LibraryAutor(models.Model):
    _name = 'library.autor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Autor'
    _order = 'name'

    name = fields.Char(string='Nombre Completo', required=True, tracking=True)
    foto = fields.Image(string='Foto', max_width=256, max_height=256)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    nacionalidad = fields.Char(string='Nacionalidad')
    biografia = fields.Html(string='Biografía')
    email = fields.Char(string='Email')
    website = fields.Char(string='Sitio Web')
    libro_ids = fields.One2many(
        'library.libro', 'autor_id', string='Libros',
    )
    libro_count = fields.Integer(
        string='Cantidad de Libros', compute='_compute_libro_count',
    )
    active = fields.Boolean(string='Activo', default=True)

    @api.depends('libro_ids')
    def _compute_libro_count(self):
        for record in self:
            record.libro_count = len(record.libro_ids)

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name or ''
