from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class PrestamoRenovacionWizard(models.TransientModel):
    _name = 'library.prestamo.renovacion.wizard'
    _description = 'Wizard para Renovar Préstamos'

    dias_extension = fields.Integer(
        string='Días de Extensión',
        default=7,
        required=True,
    )
    prestamo_ids = fields.Many2many(
        'library.prestamo',
        string='Préstamos a Renovar',
    )

    @api.model
    def default_get(self, fields_list):
        """Carga automáticamente los préstamos seleccionados en la lista."""
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['prestamo_ids'] = [(6, 0, active_ids)]
        return res

    def action_renovar(self):
        """Extiende la fecha de devolución de todos los préstamos seleccionados."""
        if not self.prestamo_ids:
            raise UserError('No hay préstamos seleccionados para renovar.')

        if self.dias_extension <= 0:
            raise UserError('Los días de extensión deben ser un número positivo.')

        for prestamo in self.prestamo_ids:
            if prestamo.estado == 'devuelto':
                raise UserError(
                    f'El préstamo "{prestamo.name}" ya fue devuelto y no se puede renovar.'
                )
            nueva_fecha = prestamo.fecha_devolucion_prevista + timedelta(days=self.dias_extension)
            prestamo.write({'fecha_devolucion_prevista': nueva_fecha})

        return {'type': 'ir.actions.act_window_close'}
