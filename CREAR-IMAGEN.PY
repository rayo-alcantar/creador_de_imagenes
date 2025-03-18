import wx
import os
from PIL import Image, ImageDraw, ImageFont
from collections import OrderedDict
import math

COLORES = OrderedDict([
	('Blanco', (255, 255, 255)),
	('Negro', (0, 0, 0)),
	('Rojo', (255, 0, 0)),
	('Rojo Oscuro', (139, 0, 0)),
	('Verde', (0, 128, 0)),
	('Verde Claro', (144, 238, 144)),
	('Verde Oscuro', (0, 100, 0)),
	('Azul', (0, 0, 255)),
	('Azul Claro', (135, 206, 235)),
	('Azul Oscuro', (0, 0, 139)),
	('Amarillo', (255, 255, 0)),
	('Naranja', (255, 165, 0)),
	('Naranja Oscuro', (255, 140, 0)),
	('Rosa', (255, 192, 203)),
	('Rosa Fuerte', (255, 20, 147)),
	('Morado', (128, 0, 128)),
	('Morado Claro', (216, 191, 216)),
	('Gris', (128, 128, 128)),
	('Gris Claro', (211, 211, 211)),
])

PATRONES = OrderedDict([
	('Sólido', 'solid'),
	('Líneas horizontales', 'h_lines'),
	('Líneas verticales', 'v_lines'),
	('Cuadrícula', 'grid'),
	('Puntos', 'dots'),
	('Ondas', 'waves'),
])

ALINEACIONES = OrderedDict([
	('Centrado', 'center'),
	('Izquierda', 'left'),
	('Derecha', 'right'),
])

class ColorComboBox(wx.ComboBox):
	def __init__(self, parent):
		super().__init__(parent, choices=list(COLORES.keys()), style=wx.CB_READONLY)
		self.SetSelection(0)
		self.SetMinSize((200, -1))

class PatternComboBox(wx.ComboBox):
	def __init__(self, parent):
		super().__init__(parent, choices=list(PATRONES.keys()), style=wx.CB_READONLY)
		self.SetSelection(0)
		self.SetMinSize((200, -1))

class AlignmentComboBox(wx.ComboBox):
	def __init__(self, parent):
		super().__init__(parent, choices=list(ALINEACIONES.keys()), style=wx.CB_READONLY)
		self.SetSelection(0)
		self.SetMinSize((200, -1))

class TextColorComboBox(wx.ComboBox):
	def __init__(self, parent):
		choices = ['Auto'] + list(COLORES.keys())
		super().__init__(parent, choices=choices, style=wx.CB_READONLY)
		self.SetSelection(0)
		self.SetMinSize((200, -1))

class HelpDialog(wx.Dialog):
	def __init__(self, parent):
		super().__init__(parent, title="Ayuda", size=(500, 400))
		
		# Crear contenido
		content = """
Generador de Imágenes con Texto v1.0
-----------------------------------
Esta aplicación te permite crear imágenes personalizadas con texto.
Perfecta para hacer carteles, anuncios, memes o cualquier imagen
que necesite texto sobre un fondo personalizado.

¿Cómo funciona?
--------------
1. Escribe el texto que deseas convertir en imagen
2. Selecciona el color de fondo
3. Elige un patrón de fondo (sólido, líneas, etc.)
4. Selecciona la alineación del texto
5. Haz clic en 'Generar Imagen'

Atajos de teclado:
-----------------
F5: Generar imagen
Alt+G: Generar imagen
Alt+T: Ir al campo de texto
Alt+A: Mostrar ayuda
Alt+S: Salir

Características:
--------------
• Múltiples líneas de texto
• 7 colores de fondo predefinidos
• 6 patrones de fondo diferentes
• 3 opciones de alineación
• Color de texto automático según el fondo
• Guardado en formato JPEG de alta calidad

Tips:
----
• Puedes usar múltiples líneas de texto
• Los colores de texto se ajustan automáticamente
• Las imágenes se guardan por defecto en Descargas
• El texto se ajusta automáticamente al tamaño de la imagen

Desarrollado por Rayoscompany teams. 
"""
		text = wx.TextCtrl(self, value=content, 
						  style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_CENTER)
		
		# Botón cerrar
		close_btn = wx.Button(self, wx.ID_CLOSE, "Cerrar")
		close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		
		# Layout
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(text, 1, wx.ALL|wx.EXPAND, 10)
		sizer.Add(close_btn, 0, wx.ALL|wx.CENTER, 10)
		self.SetSizer(sizer)

class MainFrame(wx.Frame):
	def __init__(self):
		super().__init__(None, title="Generador de Imágenes Texto", size=(800, 500))
		self.panel = wx.Panel(self)
		# Establecer la carpeta de descargas como ubicación predeterminada
		self.downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
		
		# Crear menú principal
		menubar = wx.MenuBar()
		file_menu = wx.Menu()
		help_menu = wx.Menu()
		
		# Elementos del menú Archivo
		gen_item = file_menu.Append(wx.ID_ANY, "&Generar\tF5", "Generar imagen")
		file_menu.AppendSeparator()
		web_item = file_menu.Append(wx.ID_ANY, "Visitar &Web", "Visitar la web del desarrollador")
		donate_item = file_menu.Append(wx.ID_ANY, "&Donar", "Hacer una donación al desarrollador")
		file_menu.AppendSeparator()
		exit_item = file_menu.Append(wx.ID_EXIT, "&Salir", "Salir de la aplicación")
		
		# Elementos del menú Ayuda
		help_item = help_menu.Append(wx.ID_HELP, "&Ayuda\tAlt+A", "Mostrar ayuda")
		
		menubar.Append(file_menu, "&Archivo")
		menubar.Append(help_menu, "A&yuda")
		self.SetMenuBar(menubar)
		
		self.Bind(wx.EVT_MENU, self.on_generate, gen_item)
		self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
		self.Bind(wx.EVT_MENU, self.on_help, help_item)
		self.Bind(wx.EVT_MENU, self.on_web, web_item)
		self.Bind(wx.EVT_MENU, self.on_donate, donate_item)
		
		# Configurar elementos de la interfaz
		texto_label = wx.StaticText(self.panel, label="&Texto:")
		# Se aumenta el tamaño del campo de texto para que entren más palabras en un renglón
		self.text_ctrl = wx.TextCtrl(self.panel, size=(600, -1), style=wx.TE_MULTILINE|wx.TE_RICH2)
		
		color_label = wx.StaticText(self.panel, label="Color de &fondo:")
		self.color_combo = ColorComboBox(self.panel)
		
		pattern_label = wx.StaticText(self.panel, label="&Patrón de fondo:")
		self.pattern_combo = PatternComboBox(self.panel)
		
		align_label = wx.StaticText(self.panel, label="&Alineación:")
		self.align_combo = AlignmentComboBox(self.panel)
		
		# Agregar selector de color de texto
		text_color_label = wx.StaticText(self.panel, label="Color de &texto:")
		self.text_color_combo = TextColorComboBox(self.panel)
		
		self.generate_btn = wx.Button(self.panel, label="&Generar Imagen")
		self.generate_btn.Bind(wx.EVT_BUTTON, self.on_generate)
		
		# Configurar layout principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Agregar campo de texto
		sizer.Add(texto_label, 0, wx.ALL, 5)
		sizer.Add(self.text_ctrl, 1, wx.EXPAND|wx.ALL, 5)
		
		# Crear grid sizer con 4 filas y 2 columnas para los controles
		ctrl_sizer = wx.FlexGridSizer(rows=4, cols=2, vgap=5, hgap=5)
		ctrl_sizer.AddGrowableCol(1)  # La segunda columna puede crecer
		
		# Agregar controles al grid sizer
		controls = [
			(color_label, self.color_combo),
			(pattern_label, self.pattern_combo),
			(align_label, self.align_combo),
			(text_color_label, self.text_color_combo)
		]
		
		for label, control in controls:
			ctrl_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
			ctrl_sizer.Add(control, 1, wx.EXPAND)
		
		sizer.Add(ctrl_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		# Agregar botón de ayuda, generar, donar y salir
		button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.help_btn = wx.Button(self.panel, label="A&yuda")
		self.donate_btn = wx.Button(self.panel, label="&Donar")
		self.exit_btn = wx.Button(self.panel, label="&Salir")
		
		self.help_btn.Bind(wx.EVT_BUTTON, self.on_help)
		self.donate_btn.Bind(wx.EVT_BUTTON, self.on_donate)
		self.exit_btn.Bind(wx.EVT_BUTTON, self.on_exit)
		
		button_sizer.Add(self.help_btn, 0, wx.RIGHT, 5)
		button_sizer.Add(self.generate_btn, 0, wx.RIGHT, 5)
		button_sizer.Add(self.donate_btn, 0, wx.RIGHT, 5)
		button_sizer.Add(self.exit_btn, 0)
		
		sizer.Add(button_sizer, 0, wx.ALL|wx.CENTER, 10)
		
		self.panel.SetSizer(sizer)
		self.Centre()
		
		# Configurar atajos de teclado
		self.SetAcceleratorTable(wx.AcceleratorTable([
			(wx.ACCEL_NORMAL, wx.WXK_F5, gen_item.GetId()),
			(wx.ACCEL_ALT, ord('A'), help_item.GetId())
		]))
		
		self.Show()
	
	def on_exit(self, event):
		"""Confirmar salida y cerrar aplicación"""
		dlg = wx.MessageDialog(self, 
							 "¿Estás seguro que deseas salir?",
							 "Confirmar salida",
							 wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)
		
		if dlg.ShowModal() == wx.ID_YES:
			self.Destroy()
		dlg.Destroy()
	
	def on_help(self, event):
		"""Mostrar diálogo de ayuda"""
		dlg = HelpDialog(self)
		dlg.ShowModal()
		dlg.Destroy()
	
	def on_web(self, event):
		"""Abrir la web del desarrollador"""
		import webbrowser
		webbrowser.open('https://rayoscompany.com')
	
	def on_donate(self, event):
		"""Abrir la página de donación"""
		import webbrowser
		webbrowser.open('https://paypal.me/rayoalcantar?country.x=MX&locale.x=es_XC')
	
	def get_text_color(self, bg_color, requested_color='Auto'):
		"""Determina el color del texto basado en el color solicitado o el fondo"""
		if requested_color != 'Auto':
			return COLORES[requested_color]
		
		r, g, b = bg_color
		luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
		return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)
	
	def draw_pattern(self, img, pattern, color):
		draw = ImageDraw.Draw(img)
		width, height = img.size
		
		if pattern == 'h_lines':
			for y in range(0, height, 20):
				draw.line([(0, y), (width, y)], fill=self.get_text_color(color), width=1)
		elif pattern == 'v_lines':
			for x in range(0, width, 20):
				draw.line([(x, 0), (x, height)], fill=self.get_text_color(color), width=1)
		elif pattern == 'grid':
			self.draw_pattern(img, 'h_lines', color)
			self.draw_pattern(img, 'v_lines', color)
		elif pattern == 'dots':
			for x in range(0, width, 20):
				for y in range(0, height, 20):
					draw.ellipse([x-2, y-2, x+2, y+2], fill=self.get_text_color(color))
		elif pattern == 'waves':
			for y in range(0, height, 20):
				points = []
				for x in range(0, width, 5):
					points.append((x, y + math.sin(x/30.0) * 10))
				draw.line(points, fill=self.get_text_color(color), width=1)
	
	def crear_imagen(self, texto, bg_color, pattern, alignment, text_color='Auto'):
		# Intentar cargar una fuente que soporte emojis
		try:
			font = ImageFont.truetype("seguiemj.ttf", 40)
		except IOError:
			try:
				font = ImageFont.truetype("arial.ttf", 40)
			except IOError:
				font = ImageFont.load_default()
		
		padding = 40
		lines = texto.split('\n')
		
		# Calcular dimensiones
		line_widths = []
		line_heights = []
		for line in lines:
			bbox = font.getbbox(line)
			line_widths.append(bbox[2] - bbox[0])
			line_heights.append(bbox[3] - bbox[1])
		
		image_width = max(line_widths) + padding * 2
		image_height = sum(line_heights) + padding * 2
		
		# Crear imagen
		img = Image.new('RGB', (image_width, image_height), color=bg_color)
		if pattern != 'solid':
			self.draw_pattern(img, pattern, bg_color)
		
		draw = ImageDraw.Draw(img)
		text_color = self.get_text_color(bg_color, text_color)
		
		# Dibujar texto
		y = padding
		for line, lh in zip(lines, line_heights):
			bbox = font.getbbox(line)
			line_width = bbox[2] - bbox[0]
			
			if alignment == 'center':
				x = (image_width - line_width) // 2
			elif alignment == 'right':
				x = image_width - line_width - padding
			else:  # left
				x = padding
				
			draw.text((x, y), line, font=font, fill=text_color)
			y += lh
		
		return img
	
	def on_generate(self, event):
		texto = self.text_ctrl.GetValue().strip()
		if not texto:
			wx.MessageBox("Por favor ingresa un texto.", "Error", wx.OK | wx.ICON_ERROR)
			return
		
		color_nombre = self.color_combo.GetValue()
		bg_color = COLORES[color_nombre]
		pattern = PATRONES[self.pattern_combo.GetValue()]
		alignment = ALINEACIONES[self.align_combo.GetValue()]
		text_color = self.text_color_combo.GetValue()
		
		try:
			imagen = self.crear_imagen(texto, bg_color, pattern, alignment, text_color)
		except Exception as e:
			wx.MessageBox(f"Error al generar imagen: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
			return
		
		# Guardar archivo
		default_file = os.path.join(self.downloads_path, "texto_generado.jpg")
		with wx.FileDialog(self, "Guardar imagen", defaultDir=self.downloads_path,
						  defaultFile=default_file, wildcard="JPEG files (*.jpg)|*.jpg",
						  style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as fileDialog:
			
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			
			path = fileDialog.GetPath()
			try:
				imagen.save(path, 'JPEG', quality=95)
				wx.MessageBox(f"Imagen guardada en:\n{path}", "Éxito", wx.OK|wx.ICON_INFORMATION)
				# Limpiar y enfocar el campo de texto
				self.text_ctrl.SetValue("")
				self.text_ctrl.SetFocus()
			except Exception as e:
				wx.MessageBox(f"Error al guardar: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)

if __name__ == "__main__":
	app = wx.App()
	MainFrame()
	app.MainLoop()
