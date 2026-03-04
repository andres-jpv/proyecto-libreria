from odoo import api, models, fields
from odoo.exceptions import UserError


class LibraryCategoria(models.Model):
    _name = 'library.categoria'
    _description = 'Categoría de Libro'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    color = fields.Integer(string='Color')
    libro_ids = fields.One2many(
        'library.libro', 'categoria_id', string='Libros',
    )
    libro_count = fields.Integer(
        string='Cantidad de Libros', compute='_compute_libro_count',
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'El nombre de la categoría debe ser único.'),
    ]

    def _compute_libro_count(self):
        for record in self:
            record.libro_count = len(record.libro_ids)

    @api.ondelete(at_uninstall=False)
    def _check_no_predefinida(self):
        for record in self:
            if record.id in self._get_categorias_predefinidas():
                raise UserError(
                    f'No se puede eliminar la categoría "{record.name}" porque es predefinida del sistema.'
                )

    def _get_categorias_predefinidas(self):
        xml_ids = [
            'library.categoria_ficcion',
            'library.categoria_no_ficcion',
            'library.categoria_ciencia',
            'library.categoria_tecnologia',
            'library.categoria_historia',
            'library.categoria_infantil',
            'library.categoria_arte',
            'library.categoria_filosofia',
        ]
        ids = []
        for xml_id in xml_ids:
            record = self.env.ref(xml_id, raise_if_not_found=False)
            if record:
                ids.append(record.id)
        return ids
