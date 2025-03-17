# Generador de Imágenes con Texto

Una aplicación de escritorio que permite crear imágenes personalizadas con texto y patrones de fondo.

## Requisitos Técnicos

- Python 3.7+
- Dependencias:
  ```bash
  pip install wxPython
  pip install Pillow
  ```

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python CREAR-IMAGEN.PY
   ```

## Características

- Interfaz gráfica intuitiva
- Múltiples líneas de texto
- 7 colores de fondo predefinidos
- 6 patrones de fondo:
  - Sólido
  - Líneas horizontales
  - Líneas verticales
  - Cuadrícula
  - Puntos
  - Ondas
- 3 opciones de alineación de texto
- Color de texto automático según el fondo
- Guardado en formato JPEG de alta calidad

## Uso

1. Inicia la aplicación
2. Escribe el texto deseado en el campo de texto
3. Selecciona un color de fondo
4. Elige un patrón de fondo
5. Selecciona la alineación del texto
6. Haz clic en "Generar Imagen"
7. Elige dónde guardar la imagen resultante

## Atajos de Teclado

- `F5`: Generar imagen
- `Alt+G`: Generar imagen
- `Alt+T`: Ir al campo de texto
- `Alt+A`: Mostrar ayuda
- `Alt+S`: Salir

## Estructura del Proyecto

```
imagen/
│
├── CREAR-IMAGEN.PY    # Archivo principal
├── README.md          # Este archivo
└── requirements.txt   # Dependencias del proyecto
```

## Detalles Técnicos

### Componentes Principales

- **wxPython**: Framework GUI
- **PIL (Pillow)**: Procesamiento de imágenes
- **OrderedDict**: Manejo de colecciones ordenadas

### Clases Principales

- `MainFrame`: Ventana principal y lógica de la aplicación
- `HelpDialog`: Diálogo de ayuda
- `ColorComboBox`: Selector de colores
- `PatternComboBox`: Selector de patrones
- `AlignmentComboBox`: Selector de alineación

### Algoritmos Clave

- **Cálculo de color de texto**: Basado en la luminancia del fondo
- **Patrones de fondo**: Generación procedural de patrones
- **Dimensionamiento**: Cálculo automático del tamaño de imagen

## Contribuir

Si deseas contribuir al proyecto:
1. Haz un fork del repositorio
2. Crea una rama para tu función
3. Envía un pull request

## Soporte

- **Web**: [rayoscompany.com](https://rayoscompany.com)
- **Donaciones**: [PayPal](https://paypal.me/rayoalcantar)

## Licencia

Este proyecto está bajo la Licencia MIT.

## Créditos

Desarrollado por Rayoscompany teams.
