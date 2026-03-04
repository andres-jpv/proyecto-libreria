from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class LibraryPrestamo(models.Model):
    _name = 'library.prestamo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Préstamo de Libro'
    _order = 'fecha_prestamo desc'

    name = fields.Char(
        string='Referencia', required=True, readonly=True,
        default='Nuevo', copy=False,
    )
    libro_id = fields.Many2one(
        'library.libro', string='Libro', required=True,
        ondelete='restrict', tracking=True,
    )
    autor_id = fields.Many2one(
        'library.autor', string='Autor',
        related='libro_id.autor_id',
    )
    socio_id = fields.Many2one(
        'res.partner', string='Socio/Cliente',
        required=True,
        ondelete='restrict', tracking=True,
    )
    fecha_prestamo = fields.Date(
        string='Fecha de Préstamo', default=fields.Date.context_today,
        required=True, tracking=True,
    )
    fecha_devolucion_prevista = fields.Date(
        string='Fecha de Devolución Prevista', required=True, tracking=True,
    )
    fecha_devolucion_real = fields.Date(
        string='Fecha de Devolución Real', tracking=True,
    )
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    ], string='Estado', default='borrador', tracking=True, required=True)
    notas = fields.Text(string='Notas')
    dias_retraso = fields.Integer(
        string='Días de Retraso', compute='_compute_dias_retraso',
    )
    is_reader = fields.Boolean(
        compute='_compute_is_reader',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'library.prestamo'
                ) or 'Nuevo'
        return super().create(vals_list)

    @api.onchange('libro_id')
    def _onchange_libro_id(self):
        if self.libro_id and self.libro_id.cantidad_disponible <= 0:
            return {
                'warning': {
                    'title': 'Sin ejemplares disponibles',
                    'message': 'El libro "{}" no tiene ejemplares disponibles.'.format(self.libro_id.name),
                    'type': 'notification',
                },
            }

    @api.onchange('fecha_prestamo')
    def _onchange_fecha_prestamo(self):
        if self.fecha_prestamo:
            self.fecha_devolucion_prevista = self.fecha_prestamo + timedelta(days=14)

    def _compute_is_reader(self):
        is_user = self.env.user.has_group('library.library_group_user')
        for record in self:
            record.is_reader = not is_user

    def _compute_dias_retraso(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.estado == 'prestado' and record.fecha_devolucion_prevista:
                delta = today - record.fecha_devolucion_prevista
                record.dias_retraso = max(delta.days, 0)
            else:
                record.dias_retraso = 0

    def action_prestar(self):
        for record in self:
            if record.libro_id.cantidad_disponible <= 0:
                raise UserError(
                    f'No hay ejemplares disponibles del libro "{record.libro_id.name}".'
                )
            record.estado = 'prestado'

    def action_devolver(self):
        for record in self:
            record.write({
                'estado': 'devuelto',
                'fecha_devolucion_real': fields.Date.context_today(self),
            })

    def action_borrador(self):
        for record in self:
            record.estado = 'borrador'

    @api.model
    def get_prestamos_de_socio(self, partner_id):
        """browse: convierte un ID entero a un recordset y busca sus préstamos"""
        socio = self.env['res.partner'].browse(partner_id)
        return self.search([('socio_id', '=', socio.id)])

    @api.model
    def _cron_verificar_vencidos(self):
        today = fields.Date.context_today(self)
        prestamos_vencidos = self.search([
            ('estado', '=', 'prestado'),
            ('fecha_devolucion_prevista', '<', today),
        ])
        prestamos_vencidos.write({'estado': 'vencido'})
