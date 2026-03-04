{
    'name': 'Library Management',
    'version': '19.0.1.0.0',
    'summary': 'Gestión de biblioteca: libros, autores, categorías y préstamos',
    'description': """
        Módulo de gestión de biblioteca para Odoo 19.
        Funcionalidades:
        - Gestión de libros con ISBN, portada y descripción
        - Catálogo de autores con biografía
        - Categorías para clasificar libros
        - Sistema de préstamos con control de fechas y estados
        - Reportes y estadísticas
    """,
    'author': 'Custom',
    'website': '',
    'category': 'Services/Library',
    'depends': ['base', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/etiqueta_views.xml',
        'views/libro_views.xml',
        'views/autor_views.xml',
        'views/categoria_views.xml',
        'views/prestamo_views.xml',
        'views/prestamo_renovacion_wizard_views.xml',
        'views/menu_views.xml',
        'data/categoria_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
