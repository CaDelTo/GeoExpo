import pygame
import pygame_gui

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("ThermoSim")

# Crear el manejador de interfaz de pygame_gui sin referencia al archivo 'theme.json'
manager = pygame_gui.UIManager((1000, 800))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Crear fuentes
font = pygame.font.Font(None, 36)

# Estado de la aplicación
pantalla_actual = "menu"

# Parámetros globales para simulaciones
parametros_conveccion = {"temp_superficie": 100.0, "temp_fluido": 25.0, "coef_conveccion": 50.0, "area": 2.0}
parametros_conduccion = {"temp_superficie": 100.0, "temp_base": 25.0, "conductividad": 1.0, "area": 2.0, "grosor": 0.05}
parametros_radiacion = {"temp_objeto": 500.0, "temp_ambiente": 300.0, "emisividad": 0.85, "area": 2.0}

# Elementos de UI para diferentes pantallas
ui_elements = {
    "menu": [],
    "conveccion": [],
    "conduccion": [],
    "radiacion": []
}

# Función para limpiar todos los elementos de la interfaz
def limpiar_elementos():
    for screen_elements in ui_elements.values():
        for element in screen_elements:
            element.kill()
    for key in ui_elements.keys():
        ui_elements[key] = []

# Funciones de conversión de unidades

# Convertir temperatura a °C
def convertir_a_celsius(valor, unidad):
    if unidad == "°C":
        return valor
    elif unidad == "°F":
        return (valor - 32) * 5.0 / 9.0
    elif unidad == "K":
        return valor - 273.15

# Convertir área a m²
def convertir_a_m2(valor, unidad):
    if unidad == "m²":
        return valor
    elif unidad == "cm²":
        return valor / 10000  # 1 m² = 10,000 cm²

# Convertir grosor a metros
def convertir_a_metros(valor, unidad):
    if unidad == "m":
        return valor
    elif unidad == "cm":
        return valor / 100  # 1 m = 100 cm

# Función para crear el menú principal
def mostrar_menu():
    if not ui_elements["menu"]:
        # Crear título
        lbl_titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 100), (300, 50)),
            text="ThermoSim - Menú Principal",
            manager=manager
        )
        ui_elements["menu"].append(lbl_titulo)

        # Crear botones para seleccionar simulaciones
        btn_conveccion = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 250), (200, 50)),
            text="Simulación de Convección",
            manager=manager
        )
        btn_conduccion = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 350), (200, 50)),
            text="Simulación de Conducción",
            manager=manager
        )
        btn_radiacion = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 450), (200, 50)),
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
    # Cálculo del flujo de calor por convección
    delta_T = temp_superficie - temp_fluido
    q = coef_conveccion * area * delta_T  # Transferencia de calor en W
    return q

# Simulación de Conducción
def calcular_conduccion(temp_superficie, temp_base, conductividad, area, grosor):
    # Cálculo del flujo de calor por conducción usando la ley de Fourier
    delta_T = temp_superficie - temp_base
    q = (conductividad * area * delta_T) / grosor  # Transferencia de calor en W
    return q

# Simulación de Radiación
def calcular_radiacion(temp_objeto, temp_ambiente, emisividad, area):
    const_boltzmann = 5.67e-8  # Constante de Stefan-Boltzmann
    # Cálculo del flujo de calor por radiación
    q = emisividad * area * const_boltzmann * ((temp_objeto**4) - (temp_ambiente**4))  # Transferencia de calor en W
    return q

# Función para mostrar la pantalla de simulación de convección
def mostrar_conveccion():
    if not ui_elements["conveccion"]:
        # Crear título
        lbl_titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 50), (300, 50)),
            text="Simulación de Convección",
            manager=manager
        )
        ui_elements["conveccion"].append(lbl_titulo)

        # Crear etiquetas, cajas de texto y dropdowns
        etiquetas = [
            ("Temp Superficie:", (50, 150), ["°C", "°F", "K"], "°C"),
            ("Temp Fluido:", (50, 200), ["°C", "°F", "K"], "°C"),
            ("Coef. Convección:", (50, 250), ["W/m²·K"], "W/m²·K"),
            ("Área:", (50, 300), ["m²", "cm²"], "m²")
        ]

        inputs = []
        dropdowns = []
        for texto, pos, opciones, opcion_inicial in etiquetas:
            # Crear etiqueta
            lbl = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(pos, (200, 30)),
                text=texto,
                manager=manager
            )
            ui_elements["conveccion"].append(lbl)

            # Crear caja de texto
            input_box = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((300, pos[1]), (150, 30)),
                manager=manager
            )
            input_box.text_colour = BLACK  # Color del texto
            input_box.border_colour = GREY   # Color del borde
            ui_elements["conveccion"].append(input_box)
            inputs.append(input_box)

            # Crear dropdown para unidades
            dropdown = pygame_gui.elements.UIDropDownMenu(
                options_list=opciones,
                starting_option=opcion_inicial,
                relative_rect=pygame.Rect((470, pos[1]), (80, 30)),
                manager=manager
            )
            ui_elements["conveccion"].append(dropdown)
            dropdowns.append(dropdown)

        # Crear botón de calcular
        btn_calcular = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 400), (100, 50)),
            text="Calcular",
            manager=manager
        )
        ui_elements["conveccion"].append(btn_calcular)

        # Almacenar referencias a los campos de entrada y dropdowns
        mostrar_conveccion.inputs = inputs
        mostrar_conveccion.dropdowns = dropdowns
        mostrar_conveccion.resultado = None

    # Crear botón de retorno
    crear_boton_retorno()

    # Mostrar resultado si está disponible
    if mostrar_conveccion.resultado is not None:
        lbl_resultado = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 450), (400, 50)),
            text=f"Transferencia de Calor: {mostrar_conveccion.resultado:.2f} W",
            manager=manager
        )
        ui_elements["conveccion"].append(lbl_resultado)
        mostrar_conveccion.resultado = None  # Resetear para evitar múltiples etiquetas

# Función para mostrar la simulación de conducción
def mostrar_conduccion():
    if not ui_elements["conduccion"]:
        # Crear título
        lbl_titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 50), (300, 50)),
            text="Simulación de Conducción",
            manager=manager
        )
        ui_elements["conduccion"].append(lbl_titulo)

        # Crear etiquetas, cajas de texto y dropdowns
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
            # Crear etiqueta
            lbl = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(pos, (200, 30)),
                text=texto,
                manager=manager
            )
            ui_elements["conduccion"].append(lbl)

            # Crear caja de texto
            input_box = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((300, pos[1]), (150, 30)),
                manager=manager
            )
            input_box.text_colour = BLACK  # Color del texto
            input_box.border_colour = GREY   # Color del borde
            ui_elements["conduccion"].append(input_box)
            inputs.append(input_box)

            # Crear dropdown para unidades
            dropdown = pygame_gui.elements.UIDropDownMenu(
                options_list=opciones,
                starting_option=opcion_inicial,
                relative_rect=pygame.Rect((470, pos[1]), (80, 30)),
                manager=manager
            )
            ui_elements["conduccion"].append(dropdown)
            dropdowns.append(dropdown)

        # Crear botón de calcular
        btn_calcular = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 400), (100, 50)),
            text="Calcular",
            manager=manager
        )
        ui_elements["conduccion"].append(btn_calcular)

        # Almacenar referencias a los campos de entrada y dropdowns
        mostrar_conduccion.inputs = inputs
        mostrar_conduccion.dropdowns = dropdowns
        mostrar_conduccion.resultado = None

    # Crear botón de retorno
    crear_boton_retorno()

    # Mostrar resultado si está disponible
    if mostrar_conduccion.resultado is not None:
        lbl_resultado = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 450), (400, 50)),
            text=f"Transferencia de Calor: {mostrar_conduccion.resultado:.2f} W",
            manager=manager
        )
        ui_elements["conduccion"].append(lbl_resultado)
        mostrar_conduccion.resultado = None  # Resetear para evitar múltiples etiquetas

# Función para mostrar la simulación de radiación
def mostrar_radiacion():
    if not ui_elements["radiacion"]:
        # Crear título
        lbl_titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 50), (300, 50)),
            text="Simulación de Radiación",
            manager=manager
        )
        ui_elements["radiacion"].append(lbl_titulo)

        # Crear etiquetas, cajas de texto y dropdowns
        etiquetas = [
            ("Temp Objeto:", (50, 150), ["°C", "°F", "K"], "K"),
            ("Temp Ambiente:", (50, 200), ["°C", "°F", "K"], "K"),
            ("Emisividad:", (50, 250), ["-"], "-"),  # Emisividad es adimensional
            ("Área:", (50, 300), ["m²", "cm²"], "m²")
        ]

        inputs = []
        dropdowns = []
        for texto, pos, opciones, opcion_inicial in etiquetas:
            # Crear etiqueta
            lbl = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(pos, (200, 30)),
                text=texto,
                manager=manager
            )
            ui_elements["radiacion"].append(lbl)

            # Crear caja de texto
            input_box = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((300, pos[1]), (150, 30)),
                manager=manager
            )
            input_box.text_colour = BLACK  # Color del texto
            input_box.border_colour = GREY   # Color del borde
            ui_elements["radiacion"].append(input_box)
            inputs.append(input_box)

            # Crear dropdown para unidades (si aplica)
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
                # Para Emisividad, que es adimensional, no se necesita dropdown
                dropdowns.append(None)

        # Crear botón de calcular
        btn_calcular = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 350), (100, 50)),
            text="Calcular",
            manager=manager
        )
        ui_elements["radiacion"].append(btn_calcular)

        # Almacenar referencias a los campos de entrada y dropdowns
        mostrar_radiacion.inputs = inputs
        mostrar_radiacion.dropdowns = dropdowns
        mostrar_radiacion.resultado = None

    # Crear botón de retorno
    crear_boton_retorno()

    # Mostrar resultado si está disponible
    if mostrar_radiacion.resultado is not None:
        lbl_resultado = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 400), (400, 50)),
            text=f"Transferencia de Calor: {mostrar_radiacion.resultado:.2f} W",
            manager=manager
        )
        ui_elements["radiacion"].append(lbl_resultado)
        mostrar_radiacion.resultado = None  # Resetear para evitar múltiples etiquetas

# Bucle principal
clock = pygame.time.Clock()
ejecutando = True
while ejecutando:
    time_delta = clock.tick(60) / 1000.0  # Tiempo entre frames
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        # Detectar los botones de las simulaciones y otros botones
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
                pantalla_actual = "menu"
                limpiar_elementos()
            elif evento.ui_element.text == "Calcular":
                if pantalla_actual == "conveccion":
                    try:
                        # Obtener los valores de las cajas de texto
                        temp_superficie_text = mostrar_conveccion.inputs[0].get_text()
                        temp_fluido_text = mostrar_conveccion.inputs[1].get_text()
                        coef_conveccion_text = mostrar_conveccion.inputs[2].get_text()
                        area_text = mostrar_conveccion.inputs[3].get_text()

                        # Verificar si las cajas de texto tienen valores válidos
                        if temp_superficie_text and temp_fluido_text and coef_conveccion_text and area_text:
                            temp_superficie = float(temp_superficie_text)
                            temp_fluido = float(temp_fluido_text)
                            coef_conveccion = float(coef_conveccion_text)
                            area = float(area_text)

                            # Obtener las unidades seleccionadas
                            unidad_temp_superficie = mostrar_conveccion.dropdowns[0].selected_option
                            unidad_temp_fluido = mostrar_conveccion.dropdowns[1].selected_option
                            unidad_area = mostrar_conveccion.dropdowns[3].selected_option

                            # Convertir unidades a las unidades base
                            temp_superficie = convertir_a_celsius(temp_superficie, unidad_temp_superficie)
                            temp_fluido = convertir_a_celsius(temp_fluido, unidad_temp_fluido)
                            area = convertir_a_m2(area, unidad_area)

                            # Realizar el cálculo
                            resultado = calcular_conveccion(temp_superficie, temp_fluido, coef_conveccion, area)
                            mostrar_conveccion.resultado = resultado
                        else:
                            mostrar_conveccion.resultado = "Error: Valores inválidos"
                    except ValueError:
                        # Manejar el error apropiadamente (por ejemplo, mostrar un mensaje de error)
                        mostrar_conveccion.resultado = "Error: Entrada no válida"

                elif pantalla_actual == "conduccion":
                    try:
                        # Obtener los valores de las cajas de texto
                        temp_superficie_text = mostrar_conduccion.inputs[0].get_text()
                        temp_base_text = mostrar_conduccion.inputs[1].get_text()
                        conductividad_text = mostrar_conduccion.inputs[2].get_text()
                        area_text = mostrar_conduccion.inputs[3].get_text()
                        grosor_text = mostrar_conduccion.inputs[4].get_text()

                        # Verificar si las cajas de texto tienen valores válidos
                        if temp_superficie_text and temp_base_text and conductividad_text and area_text and grosor_text:
                            temp_superficie = float(temp_superficie_text)
                            temp_base = float(temp_base_text)
                            conductividad = float(conductividad_text)
                            area = float(area_text)
                            grosor = float(grosor_text)

                            # Obtener las unidades seleccionadas
                            unidad_temp_superficie = mostrar_conduccion.dropdowns[0].selected_option
                            unidad_temp_base = mostrar_conduccion.dropdowns[1].selected_option
                            unidad_area = mostrar_conduccion.dropdowns[3].selected_option
                            unidad_grosor = mostrar_conduccion.dropdowns[4].selected_option

                            # Convertir unidades a las unidades base
                            temp_superficie = convertir_a_celsius(temp_superficie, unidad_temp_superficie)
                            temp_base = convertir_a_celsius(temp_base, unidad_temp_base)
                            area = convertir_a_m2(area, unidad_area)
                            grosor = convertir_a_metros(grosor, unidad_grosor)

                            # Realizar el cálculo
                            resultado = calcular_conduccion(temp_superficie, temp_base, conductividad, area, grosor)
                            mostrar_conduccion.resultado = resultado
                        else:
                            mostrar_conduccion.resultado = "Error: Valores inválidos"
                    except ValueError:
                        # Manejar el error apropiadamente
                        mostrar_conduccion.resultado = "Error: Entrada no válida"

                elif pantalla_actual == "radiacion":
                    try:
                        # Obtener los valores de las cajas de texto
                        temp_objeto_text = mostrar_radiacion.inputs[0].get_text()
                        temp_ambiente_text = mostrar_radiacion.inputs[1].get_text()
                        emisividad_text = mostrar_radiacion.inputs[2].get_text()
                        area_text = mostrar_radiacion.inputs[3].get_text()

                        # Verificar si las cajas de texto tienen valores válidos
                        if temp_objeto_text and temp_ambiente_text and emisividad_text and area_text:
                            temp_objeto = float(temp_objeto_text)
                            temp_ambiente = float(temp_ambiente_text)
                            emisividad = float(emisividad_text)
                            area = float(area_text)

                            # Obtener las unidades seleccionadas
                            unidad_temp_objeto = mostrar_radiacion.dropdowns[0].selected_option
                            unidad_temp_ambiente = mostrar_radiacion.dropdowns[1].selected_option
                            unidad_area = mostrar_radiacion.dropdowns[3].selected_option

                            # Convertir unidades a las unidades base
                            temp_objeto = convertir_a_celsius(temp_objeto, unidad_temp_objeto) + 273.15  # Convertir a Kelvin
                            temp_ambiente = convertir_a_celsius(temp_ambiente, unidad_temp_ambiente) + 273.15  # Convertir a Kelvin
                            area = convertir_a_m2(area, unidad_area)

                            # Realizar el cálculo
                            resultado = calcular_radiacion(temp_objeto, temp_ambiente, emisividad, area)
                            mostrar_radiacion.resultado = resultado
                        else:
                            mostrar_radiacion.resultado = "Error: Valores inválidos"
                    except ValueError:
                        # Manejar el error apropiadamente
                        mostrar_radiacion.resultado = "Error: Entrada no válida"

        manager.process_events(evento)

    # Dibujar la pantalla según el estado actual
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

    # Actualizar pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
