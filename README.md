# 📚 Library App — Módulo Odoo de Gestión Bibliotecaria

Módulo personalizado de Odoo para la administración integral de una biblioteca: préstamos, autores, libros y socios. Desarrollado como proyecto de certificación, cubre las áreas más importantes del desarrollo Odoo backend y frontend.

---

## ✨ Características

### Modelos y Relaciones
- Modelado relacional completo con **Many2one**, **One2many** y **Many2many**
- Validaciones SQL (ISBN único) y constraints Python para integridad de datos
- Herencia de `res.partner` para agregar el campo "Socio de Biblioteca" al módulo de Contactos

### Lógica de Negocio
- Decoradores ORM: `@api.depends`, `@api.constrains`, `@api.onchange`, `@api.ondelete`
- Métodos ORM: `search`, `create`, `write`, `unlink`
- **Wizard** (`TransientModel`) para renovación masiva de préstamos con cálculo automático de fechas y validación de estados

### Vistas
- Vistas **Kanban**, **Formulario**, **Lista** y **Búsqueda** con filtros y agrupaciones
- **Smart Buttons** con campos computados y filtrado por dominio

### Seguridad
- Control de acceso por roles: **Lector**, **Usuario**, **Bibliotecario**
- Herencia de grupos y reglas de registro dinámicas

### Reportes
- Reporte PDF de **Carnet de Préstamo** con QWeb, Bootstrap y lógica condicional (`t-if`, `t-foreach`)

---

## 🛠️ Stack

| Tecnología | Uso |
|---|---|
| Python 3 | Modelos, decoradores ORM, wizards |
| XML / XPath | Vistas, herencia de vistas, menús |
| QWeb | Reportes PDF |
| PostgreSQL | Base de datos relacional |
| Docker / DevContainers | Entorno de desarrollo reproducible |
| Odoo 18.0 | Framework base |

---

## 🚀 Instalación con DevContainers

> Requiere Docker Desktop y VS Code con la extensión Dev Containers.

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/andres-jpv/proyecto-libreria.git
   ```
2. Abrir en VS Code → **Reopen in Container**
3. Copiar la carpeta del módulo al directorio `addons` de tu instancia Odoo
4. En Odoo: Activar modo desarrollador → **Aplicaciones** → Buscar `library` → Instalar

---

## 👤 Autor

**Jordan Pincay** — [linkedin.com/in/jpincayvinces](https://linkedin.com/in/jpincayvinces) · [j.pincayvinces@gmail.com](mailto:j.pincayvinces@gmail.com)
