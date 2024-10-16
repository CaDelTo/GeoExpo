import pygame
import pygame_gui

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("ThermoSim")
pygame.display.set_icon(pygame.image.load("Assets\Logo.png"))
# Crear el manejador de interfaz de pygame_gui sin referencia al archivo 'theme.json'
manager = pygame_gui.UIManager((1000, 800), 'theme.json')

# Colores
WHITE = (255, 254, 229)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Crear fuentes
font = pygame.font.Font(None, 36)
pantalla_actual = "menu"

logo = 'Assets\Logo.png'
estaticaConveccion = "Assets\Conveccion\Agua0.png"
imagenesConveccion = ["Assets\Conveccion\Agua1.png", "Assets\Conveccion\Agua2.png", "Assets\Conveccion\Agua3.png"]
estaticaConduccion = "Assets\Conduccion\Conduccion0.png" 
imagenesConduccion = ["Assets\Conduccion\Conduccion1.png", "Assets\Conduccion\Conduccion2.png", "Assets\Conduccion\Conduccion3.png"]
estaticaRadiacion = "Assets\Radiacion\Radiacion0.png"
imagenesRadiacion = ["Assets\Radiacion\Radiacion1.png", "Assets\Radiacion\Radiacion2.png", "Assets\Radiacion\Radiacion3.png"]

indice_frame = 0
fps_gif = 3
temporizador_gif = 0
estado = "estatica" 

imgLogo = pygame.image.load(logo).convert_alpha()
imgConduccion = pygame.image.load(estaticaConduccion).convert_alpha()
framesConduccion = [pygame.image.load(frame).convert_alpha() for frame in imagenesConduccion]
imgConveccion = pygame.image.load(estaticaConveccion).convert_alpha()
framesConveccion = [pygame.image.load(frame).convert_alpha() for frame in imagenesConveccion]
imgRadiacion = pygame.image.load(estaticaRadiacion).convert_alpha()
framesRadiacion = [pygame.image.load(frame).convert_alpha() for frame in imagenesRadiacion]

parametros_conveccion = {"temp_superficie": 100.0, "temp_fluido": 25.0, "coef_conveccion": 50.0, "area": 2.0}
parametros_conduccion = {"temp_superficie": 100.0, "temp_base": 25.0, "conductividad": 1.0, "area": 2.0, "grosor": 0.05}
parametros_radiacion = {"temp_objeto": 500.0, "temp_ambiente": 300.0, "emisividad": 0.85, "area": 2.0}

ui_elements = {
    "menu": [],
    "conveccion": [],
    "conduccion": [],
    "radiacion": []
}

def mostrar_imagen(imagen, x, y):
    screen.blit(imagen, (x, y))
# Función para limpiar todos los elementos de la interfaz
def limpiar_elementos():
    for screen_elements in ui_elements.values():
        for element in screen_elements:
            element.kill()
    for key in ui_elements.keys():
        ui_elements[key] = []
# Función para limpiar solo el resultado anterior
def limpiar_resultado_anterior():
    # Limpiar solo las etiquetas de resultado en la pantalla actual
    for elemento in ui_elements[pantalla_actual]:
        if isinstance(elemento, pygame_gui.elements.UILabel) and "Transferencia de Calor" in elemento.text:
            elemento.kill()  # Eliminar el elemento de la pantalla
    # Remover de la lista de elementos UI
    ui_elements[pantalla_actual] = [el for el in ui_elements[pantalla_actual] if el.alive()]

def convertir_a_celsius(valor, unidad):
    if unidad == "°C":
        return valor
    elif unidad == "°F":
        return (valor - 32) * 5.0 / 9.0
    elif unidad == "K":
        return valor - 273.15

def convertir_a_m2(valor, unidad):
    if unidad == "m²":
        return valor
    elif unidad == "cm²":
        return valor / 10000  # 1 m² = 10,000 cm²

def convertir_a_metros(valor, unidad):
    if unidad == "m":
        return valor
    elif unidad == "cm":
        return valor / 100  # 1 m = 100 cm
# Función para crear el menú principal
def mostrar_menu():
    if estado == "estatica":
        imgLogo_resized = pygame.transform.scale(imgLogo, (300, 300))  # Cambiar el tamaño de la imagen
        mostrar_imagen(imgLogo_resized, 350, 130)
    if not ui_elements["menu"]:
        lbl_titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 100), (300, 50)),
            text="ThermoSim - Menú Principal",
            manager=manager
        )
        ui_elements["menu"].append(lbl_titulo)
        
        btn_conveccion = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 450), (200, 50)),
            text="Simulación de Convección",
            manager=manager
        )
        btn_conduccion = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 550), (200, 50)),
            text="Simulación de Conducción",
            manager=manager
        )
        btn_radiacion = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 650), (200, 50)),
            text="Simulación de Radiación",
            manager=manager
        )
        ui_elements["menu"].extend([btn_conveccion, btn_conduccion, btn_radiacion])

# Función para crear el botón de retorno al menú
def crear_boton_retorno():
    if not any(isinstance(el, pygame_gui.elements.UIButton) and el.text == "Retornar al Menú" for el in ui_elements[pantalla_actual]):
        btn_retorno = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (150, 50)),
            text="Retornar al Menú",
            manager=manager
        )
        ui_elements[pantalla_actual].append(btn_retorno)

# Simulación de Convección
def calcular_conveccion(temp_superficie, temp_fluido, coef_conveccion, area):
    delta_T = temp_superficie - temp_fluido
    q = coef_conveccion * area * delta_T  # Transferencia de calor en W
    return q

# Simulación de Conducción
def calcular_conduccion(temp_superficie, temp_base, conductividad, area, grosor):
    delta_T = temp_superficie - temp_base
    q = (conductividad * area * delta_T) / grosor  # Transferencia de calor en W
    return q

# Simulación de Radiación
def calcular_radiacion(temp_objeto, temp_ambiente, emisividad, area):
    const_boltzmann = 5.67e-8  # Constante de Stefan-Boltzmann
    q = emisividad * area * const_boltzmann * ((temp_objeto**4) - (temp_ambiente**4))  # Transferencia de calor en W
    return q

# Función para mostrar la simulación de convección
def mostrar_conveccion():
    global indice_frame, temporizador_gif
    # Mostrar imagen estática o GIF
    if estado == "estatica":
        mostrar_imagen(imgConveccion, 700, 200)  # Muestra la imagen de referencia en coordenadas (700, 200)
    elif estado == "animando":
        # Mostrar fotograma del GIF
        mostrar_imagen(framesConveccion[indice_frame], 700, 200)
        # Actualizar el índice del GIF según el temporizador
        if pygame.time.get_ticks() - temporizador_gif > 1000 // fps_gif:
            indice_frame = (indice_frame + 1) % len(framesConveccion)
            temporizador_gif = pygame.time.get_ticks()
    if not ui_elements["conveccion"]:
        lbl_titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 50), (300, 50)),
            text="Simulación de Convección",
            manager=manager
        )
        ui_elements["conveccion"].append(lbl_titulo)

        etiquetas = [
            ("Temp Superficie:", (50, 150), ["°C", "°F", "K"], "°C"),
            ("Temp Fluido:", (50, 200), ["°C", "°F", "K"], "°C"),
            ("Coef. Convección:", (50, 250), ["W/m²·K"], "W/m²·K"),
            ("Área:", (50, 300), ["m²", "cm²"], "m²")
        ]

        inputs = []
        dropdowns = []
        for texto, pos, opciones, opcion_inicial in etiquetas:
            lbl = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(pos, (200, 30)),
                text=texto,
                manager=manager
            )
            ui_elements["conveccion"].append(lbl)

            input_box = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((300, pos[1]), (150, 30)),
                manager=manager
            )
            input_box.text_colour = BLACK
            input_box.border_colour = GREY
            ui_elements["conveccion"].append(input_box)
            inputs.append(input_box)

            dropdown = pygame_gui.elements.UIDropDownMenu(
                options_list=opciones,
                starting_option=opcion_inicial,
                relative_rect=pygame.Rect((470, pos[1]), (80, 30)),
                manager=manager
            )
            ui_elements["conveccion"].append(dropdown)
            dropdowns.append(dropdown)

        btn_calcular = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 400), (100, 50)),
            text="Calcular",
            manager=manager
        )
        ui_elements["conveccion"].append(btn_calcular)
        explicacion1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 500), (900, 100)),
            text="La convección es la transferencia de calor por el movimiento de fluidos (líquidos o gases). Este tipo de transferencia de calor es",
            manager=manager
        )
        explicacion2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 520), (900, 100)),
            text="fundamental en sistemas en los que es necesario el movimiento de fluidos para que el calor se distribuya de manera uniforme",
            manager=manager
        )
        ui_elements["conveccion"].append(explicacion1)
        ui_elements["conveccion"].append(explicacion2)

        mostrar_conveccion.inputs = inputs
        mostrar_conveccion.dropdowns = dropdowns
        mostrar_conveccion.resultado = None

    crear_boton_retorno()

    if mostrar_conveccion.resultado is not None:
        lbl_resultado = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 450), (400, 50)),
            text=f"Transferencia de Calor: {mostrar_conveccion.resultado:.2f} W",
            manager=manager
        )
        ui_elements["conveccion"].append(lbl_resultado)
        mostrar_conveccion.resultado = None

# Función para mostrar la simulación de conducción
def mostrar_conduccion():
    global indice_frame, temporizador_gif
    # Mostrar imagen estática o GIF
    if estado == "estatica":
        mostrar_imagen(imgConduccion, 700, 200)  # Muestra la imagen de referencia en coordenadas (700, 200)
    elif estado == "animando":
        # Mostrar fotograma del GIF
        mostrar_imagen(framesConduccion[indice_frame], 700, 200)
        # Actualizar el índice del GIF según el temporizador
        if pygame.time.get_ticks() - temporizador_gif > 1000 // fps_gif:
            indice_frame = (indice_frame + 1) % len(framesConduccion)
            temporizador_gif = pygame.time.get_ticks()
    if not ui_elements["conduccion"]:
        lbl_titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 50), (300, 50)),
            text="Simulación de Conducción",
            manager=manager
        )
        ui_elements["conduccion"].append(lbl_titulo)

        etiquetas = [
            ("Temp Superficie:", (50, 150), ["°C", "°F", "K"], "°C"),
            ("Temp Base:", (50, 200), ["°C", "°F", "K"], "°C"),
            ("Conductividad:", (50, 250), ["W/m·K"], "W/m·K"),
            ("Área:", (50, 300), ["m²", "cm²"], "m²"),
            ("Grosor:", (50, 350), ["m", "cm"], "m")
        ]

        inputs = []
        dropdowns = []
        for texto, pos, opciones, opcion_inicial in etiquetas:
            lbl = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(pos, (200, 30)),
                text=texto,
                manager=manager
            )
            ui_elements["conduccion"].append(lbl)

            input_box = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((300, pos[1]), (150, 30)),
                manager=manager
            )
            input_box.text_colour = BLACK
            input_box.border_colour = GREY
            ui_elements["conduccion"].append(input_box)
            inputs.append(input_box)

            dropdown = pygame_gui.elements.UIDropDownMenu(
                options_list=opciones,
                starting_option=opcion_inicial,
                relative_rect=pygame.Rect((470, pos[1]), (80, 30)),
                manager=manager
            )
            ui_elements["conduccion"].append(dropdown)
            dropdowns.append(dropdown)

        btn_calcular = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 400), (100, 50)),
            text="Calcular",
            manager=manager
        )
        ui_elements["conduccion"].append(btn_calcular)
        explicacion1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 500), (900, 100)),
            text="La conducción es la transferencia de calor a través de un material sólido. Se produce cuando las moléculas de una sustancia vibran y",
            manager=manager
        )
        explicacion2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 520), (900, 100)),
            text="transfieren energía a las moléculas adyacentes. Es un proceso fundamental en muchas aplicaciones industriales en las que los",
            manager=manager
        )
        explicacion3 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 540), (900, 100)),
            text="materiales sólidos son utilizados como aislantes o conductores de calor.",
            manager=manager
        )
        ui_elements["conveccion"].append(explicacion1)
        ui_elements["conveccion"].append(explicacion2)
        ui_elements["conveccion"].append(explicacion3)
        mostrar_conduccion.inputs = inputs
        mostrar_conduccion.dropdowns = dropdowns
        mostrar_conduccion.resultado = None

    crear_boton_retorno()

    if mostrar_conduccion.resultado is not None:
        lbl_resultado = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 450), (400, 50)),
            text=f"Transferencia de Calor: {mostrar_conduccion.resultado:.2f} W",
            manager=manager
        )
        ui_elements["conduccion"].append(lbl_resultado)
        mostrar_conduccion.resultado = None

# Función para mostrar la simulación de radiación
def mostrar_radiacion():
    global indice_frame, temporizador_gif
    # Mostrar imagen estática o GIF
    if estado == "estatica":
        mostrar_imagen(imgRadiacion, 700, 200)  # Muestra la imagen de referencia en coordenadas (700, 200)
    elif estado == "animando":
        # Mostrar fotograma del GIF
        mostrar_imagen(framesRadiacion[indice_frame], 700, 200)
        # Actualizar el índice del GIF según el temporizador
        if pygame.time.get_ticks() - temporizador_gif > 1000 // fps_gif:
            indice_frame = (indice_frame + 1) % len(framesRadiacion)
            temporizador_gif = pygame.time.get_ticks()
    if not ui_elements["radiacion"]:
        lbl_titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 50), (300, 50)),
            text="Simulación de Radiación",
            manager=manager
        )
        ui_elements["radiacion"].append(lbl_titulo)

        etiquetas = [
            ("Temp Objeto:", (50, 150), ["°C", "°F", "K"], "K"),
            ("Temp Ambiente:", (50, 200), ["°C", "°F", "K"], "K"),
            ("Emisividad:", (50, 250), ["-"], "-"),
            ("Área:", (50, 300), ["m²", "cm²"], "m²")
        ]

        inputs = []
        dropdowns = []
        for texto, pos, opciones, opcion_inicial in etiquetas:
            lbl = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(pos, (200, 30)),
                text=texto,
                manager=manager
            )
            ui_elements["radiacion"].append(lbl)

            input_box = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((300, pos[1]), (150, 30)),
                manager=manager
            )
            input_box.text_colour = BLACK
            input_box.border_colour = GREY
            ui_elements["radiacion"].append(input_box)
            inputs.append(input_box)

            if texto != "Emisividad:":
                dropdown = pygame_gui.elements.UIDropDownMenu(
                    options_list=opciones,
                    starting_option=opcion_inicial,
                    relative_rect=pygame.Rect((470, pos[1]), (80, 30)),
                    manager=manager
                )
                ui_elements["radiacion"].append(dropdown)
                dropdowns.append(dropdown)
            else:
                dropdowns.append(None)

        btn_calcular = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 350), (100, 50)),
            text="Calcular",
            manager=manager
        )
        ui_elements["radiacion"].append(btn_calcular)
        
        explicacion1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 500), (900, 100)),
            text="La radiación es la transferencia de calor a través de ondas electromagnéticas. A diferencia de la conducción y la convección,",
            manager=manager
        )
        explicacion2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 520), (900, 100)),
            text="la radiación no requiere ningún medio y puede producirse en un espacio vacío.",
            manager=manager
        )
        
        ui_elements["conveccion"].append(explicacion1)
        ui_elements["conveccion"].append(explicacion2)

        mostrar_radiacion.inputs = inputs
        mostrar_radiacion.dropdowns = dropdowns
        mostrar_radiacion.resultado = None

    crear_boton_retorno()

    if mostrar_radiacion.resultado is not None:
        lbl_resultado = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 400), (400, 50)),
            text=f"Transferencia de Calor: {mostrar_radiacion.resultado:.2f} W",
            manager=manager
        )
        ui_elements["radiacion"].append(lbl_resultado)
        mostrar_radiacion.resultado = None

# Bucle principal
clock = pygame.time.Clock()
ejecutando = True
while ejecutando:
    time_delta = clock.tick(60) / 1000.0
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element.text == "Simulación de Convección":
                pantalla_actual = "conveccion"
                limpiar_elementos()
            elif evento.ui_element.text == "Simulación de Conducción":
                pantalla_actual = "conduccion"
                limpiar_elementos()
            elif evento.ui_element.text == "Simulación de Radiación":
                pantalla_actual = "radiacion"
                limpiar_elementos()
            elif evento.ui_element.text == "Retornar al Menú":
                estado = "estatica"
                pantalla_actual = "menu"
                limpiar_elementos()
            elif evento.ui_element.text == "Calcular":
                estado = "animando"
                temporizador_gif = pygame.time.get_ticks()
                if pantalla_actual == "conveccion":
                    limpiar_resultado_anterior()  # Limpiar el resultado anterior
                    try:
                        temp_superficie = float(mostrar_conveccion.inputs[0].get_text())
                        temp_fluido = float(mostrar_conveccion.inputs[1].get_text())
                        coef_conveccion = float(mostrar_conveccion.inputs[2].get_text())
                        area = float(mostrar_conveccion.inputs[3].get_text())
                        unidad_temp_superficie = mostrar_conveccion.dropdowns[0].selected_option
                        unidad_temp_fluido = mostrar_conveccion.dropdowns[1].selected_option
                        unidad_area = mostrar_conveccion.dropdowns[3].selected_option
                        temp_superficie = convertir_a_celsius(temp_superficie, unidad_temp_superficie[0])
                        temp_fluido = convertir_a_celsius(temp_fluido, unidad_temp_fluido[0])
                        area = convertir_a_m2(area, unidad_area[0])
                        resultado = calcular_conveccion(temp_superficie, temp_fluido, coef_conveccion, area)
                        mostrar_conveccion.resultado = resultado
                    except ValueError:
                        mostrar_conveccion.resultado = "Error: Entrada no válida"

                elif pantalla_actual == "conduccion":
                    limpiar_resultado_anterior()  # Limpiar el resultado anterior
                    try:
                        temp_superficie = float(mostrar_conduccion.inputs[0].get_text())
                        temp_base = float(mostrar_conduccion.inputs[1].get_text())
                        conductividad = float(mostrar_conduccion.inputs[2].get_text())
                        area = float(mostrar_conduccion.inputs[3].get_text())
                        grosor = float(mostrar_conduccion.inputs[4].get_text())
                        unidad_temp_superficie = mostrar_conduccion.dropdowns[0].selected_option
                        unidad_temp_base = mostrar_conduccion.dropdowns[1].selected_option
                        unidad_area = mostrar_conduccion.dropdowns[3].selected_option
                        unidad_grosor = mostrar_conduccion.dropdowns[4].selected_option
                        temp_superficie = convertir_a_celsius(temp_superficie, unidad_temp_superficie[0])
                        temp_base = convertir_a_celsius(temp_base, unidad_temp_base[0])
                        area = convertir_a_m2(area, unidad_area[0])
                        grosor = convertir_a_metros(grosor, unidad_grosor[0])
                        resultado = calcular_conduccion(temp_superficie, temp_base, conductividad, area, grosor)
                        mostrar_conduccion.resultado = resultado
                    except ValueError:
                        mostrar_conduccion.resultado = "Error: Entrada no válida"

                elif pantalla_actual == "radiacion":
                    limpiar_resultado_anterior()  # Limpiar el resultado anterior
                    try:
                        temp_objeto = float(mostrar_radiacion.inputs[0].get_text())
                        temp_ambiente = float(mostrar_radiacion.inputs[1].get_text())
                        emisividad = float(mostrar_radiacion.inputs[2].get_text())
                        area = float(mostrar_radiacion.inputs[3].get_text())
                        unidad_temp_objeto = mostrar_radiacion.dropdowns[0].selected_option
                        unidad_temp_ambiente = mostrar_radiacion.dropdowns[1].selected_option
                        unidad_area = mostrar_radiacion.dropdowns[3].selected_option
                        temp_objeto = convertir_a_celsius(temp_objeto, unidad_temp_objeto[0]) + 273.15
                        temp_ambiente = convertir_a_celsius(temp_ambiente, unidad_temp_ambiente[0]) + 273.15
                        area = convertir_a_m2(area, unidad_area[0])
                        resultado = calcular_radiacion(temp_objeto, temp_ambiente, emisividad, area)
                        mostrar_radiacion.resultado = resultado
                    except ValueError:
                        mostrar_radiacion.resultado = "Error: Entrada no válida"

        manager.process_events(evento)

    screen.fill(WHITE)
    if pantalla_actual == "menu":
        mostrar_menu()
    elif pantalla_actual == "conveccion":
        mostrar_conveccion()
    elif pantalla_actual == "conduccion":
        mostrar_conduccion()
    elif pantalla_actual == "radiacion":
        mostrar_radiacion()

    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
