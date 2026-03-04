from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryLibro(models.Model):
    _name = 'library.libro'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Libro'
    _order = 'name'

    name = fields.Char(string='Título', required=True, tracking=True)
    isbn = fields.Char(string='ISBN', tracking=True)
    portada = fields.Image(string='Portada', max_width=512, max_height=512)
    descripcion = fields.Text(string='Descripción')
    fecha_publicacion = fields.Date(string='Fecha de Publicación')
    num_paginas = fields.Integer(string='Número de Páginas')
    editorial = fields.Char(string='Editorial')
    idioma = fields.Selection([
        ('es', 'Español'),
        ('en', 'Inglés'),
        ('fr', 'Francés'),
        ('de', 'Alemán'),
        ('pt', 'Portugués'),
        ('it', 'Italiano'),
        ('otro', 'Otro'),
    ], string='Idioma', default='es')
    precio = fields.Float(string='Precio', digits=(10, 2))
    cantidad_total = fields.Integer(string='Cantidad Total', default=1)
    cantidad_disponible = fields.Integer(
        string='Cantidad Disponible', compute='_compute_cantidad_disponible',
        store=True,
    )
    autor_id = fields.Many2one(
        'library.autor', string='Autor', required=True,
        ondelete='restrict', tracking=True,
    )
    categoria_id = fields.Many2one(
        'library.categoria', string='Categoría',
        ondelete='set null',
    )
    prestamo_ids = fields.One2many(
        'library.prestamo', 'libro_id', string='Préstamos',
    )
    etiqueta_ids = fields.Many2many(
        'library.etiqueta', string='Etiquetas',
    )
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('no_disponible', 'No Disponible'),
    ], string='Estado', compute='_compute_estado', store=True)
    active = fields.Boolean(string='Activo', default=True)

    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)',
         'El ISBN debe ser único para cada libro.'),
        ('num_paginas_positive', 'CHECK(num_paginas >= 0)',
         'El número de páginas debe ser positivo.'),
        ('cantidad_total_positive', 'CHECK(cantidad_total >= 0)',
         'La cantidad total debe ser positiva.'),
    ]

    @api.depends('cantidad_total', 'prestamo_ids', 'prestamo_ids.estado')
    def _compute_cantidad_disponible(self):
        for record in self:
            prestamos_activos = record.prestamo_ids.filtered(
                lambda p: p.estado == 'prestado'
            )
            record.cantidad_disponible = record.cantidad_total - len(prestamos_activos)

    @api.depends('cantidad_disponible')
    def _compute_estado(self):
        for record in self:
            if record.cantidad_disponible > 0:
                record.estado = 'disponible'
            elif record.cantidad_total > 0:
                record.estado = 'prestado'
            else:
                record.estado = 'no_disponible'

    @api.constrains('isbn')
    def _check_isbn(self):
        for record in self:
            if record.isbn and len(record.isbn.replace('-', '')) not in (10, 13):
                raise ValidationError(
                    'El ISBN debe tener 10 o 13 dígitos.'
                )

    @api.model
    def get_estadisticas_por_categoria(self):
        """_read_group: cuenta libros agrupados por categoría"""
        return self._read_group(
            domain=[('active', '=', True)],
            groupby=['categoria_id'],
            aggregates=['__count'],
        )
