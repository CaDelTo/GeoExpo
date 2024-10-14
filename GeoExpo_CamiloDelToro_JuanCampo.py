import pygame
import pygame_gui

# Inicializar Pygame
pygame.init()

# Crear ventana
screen = pygame.display.set_mode((1000, 800))  # Pantalla grande
pygame.display.set_caption("ThermoSim")

# Crear el manejador de interfaz de pygame_gui
manager = pygame_gui.UIManager((1000, 800))  # Ajustar tamaño del manejador

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)  # Color para el borde de las cajas de texto

# Crear fuentes
font = pygame.font.Font(None, 36)

# Estado de la aplicación
pantalla_actual = "menu"

# Parámetros globales para simulaciones
parametros_conveccion = {"temp_superficie": 100.0, "temp_fluido": 25.0, "coef_conveccion": 50.0, "area": 2.0}
parametros_conduccion = {"temp_superficie": 100.0, "temp_base": 25.0, "conductividad": 1.0, "area": 2.0, "grosor": 0.05}
parametros_radiacion = {"temp_objeto": 500.0, "temp_ambiente": 300.0, "emisividad": 0.85, "area": 2.0}

# Función para limpiar elementos de la interfaz
def limpiar_elementos():
    manager.clear_and_reset()  # Limpiar todos los elementos de pygame_gui

# Función para crear el menú principal
def mostrar_menu():
    screen.fill(WHITE)
    texto_titulo = font.render("ThermoSim - Menú Principal", True, BLACK)
    screen.blit(texto_titulo, (350, 100))

    # Botones para seleccionar simulaciones
    boton_conveccion = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 250), (200, 50)),
        text="Simulación de Convección",
        manager=manager
    )
    
    boton_conduccion = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 350), (200, 50)),
        text="Simulación de Conducción",
        manager=manager
    )
    
    boton_radiacion = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((400, 450), (200, 50)),
        text="Simulación de Radiación",
        manager=manager
    )

# Función para crear el botón de retorno
def crear_boton_retorno():
    boton_retorno = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((20, 20), (150, 50)),  # Posición superior izquierda
        text="Retornar al Menú",
        manager=manager
    )
    return boton_retorno

# Simulación de Convección
def calcular_conveccion():
    temp_superficie = parametros_conveccion['temp_superficie']
    temp_fluido = parametros_conveccion['temp_fluido']
    coef_conveccion = parametros_conveccion['coef_conveccion']
    area = parametros_conveccion['area']
    
    # Cálculo del flujo de calor por convección
    delta_T = temp_superficie - temp_fluido
    q = coef_conveccion * area * delta_T  # Transferencia de calor en W
    return q

# Simulación de Conducción
def calcular_conduccion():
    temp_superficie = parametros_conduccion['temp_superficie']
    temp_base = parametros_conduccion['temp_base']
    conductividad = parametros_conduccion['conductividad']
    area = parametros_conduccion['area']
    grosor = parametros_conduccion['grosor']
    
    # Cálculo del flujo de calor por conducción usando la ley de Fourier
    delta_T = temp_superficie - temp_base
    q = (conductividad * area * delta_T) / grosor  # Transferencia de calor en W
    return q

# Simulación de Radiación
def calcular_radiacion():
    temp_objeto = parametros_radiacion['temp_objeto']
    temp_ambiente = parametros_radiacion['temp_ambiente']
    emisividad = parametros_radiacion['emisividad']
    area = parametros_radiacion['area']
    const_boltzmann = 5.67e-8  # Constante de Stefan-Boltzmann

    # Cálculo del flujo de calor por radiación
    q = emisividad * area * const_boltzmann * ((temp_objeto**4) - (temp_ambiente**4))  # Transferencia de calor en W
    return q

# Función para mostrar la pantalla de simulación de convección
def mostrar_conveccion():
    screen.fill(WHITE)
    texto_titulo = font.render("Simulación de Convección", True, BLACK)
    screen.blit(texto_titulo, (350, 50))

    # Crear cuadros de texto para ingresar manualmente los datos
    input_temp_superficie = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 150), (100, 30)),
        manager=manager
    )
    input_temp_fluido = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 200), (100, 30)),
        manager=manager
    )
    input_coef_conveccion = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 250), (100, 30)),
        manager=manager
    )
    input_area = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 300), (100, 30)),
        manager=manager
    )

    # Personalizar las cajas de texto
    input_temp_superficie.text_colour = BLACK  # Color del texto
    input_temp_fluido.text_colour = BLACK
    input_coef_conveccion.text_colour = BLACK
    input_area.text_colour = BLACK

    input_temp_superficie.border_colour = WHITE
    input_temp_fluido.border_colour = WHITE
    input_coef_conveccion.border_colour = WHITE
    input_area.border_colour = WHITE

    # Mostrar resultados de la simulación
    resultado = calcular_conveccion()
    texto_resultado = font.render(f"Transferencia de Calor: {resultado:.2f} W", True, BLACK)
    screen.blit(texto_resultado, (300, 400))

    # Mostrar etiquetas para las variables alineadas a la izquierda
    screen.blit(font.render("Temp Superficie (°C):", True, BLACK), (50, 150))
    screen.blit(font.render("Temp Fluido (°C):", True, BLACK), (50, 200))
    screen.blit(font.render("Coef. Convección (W/m²·K):", True, BLACK), (50, 250))
    screen.blit(font.render("Área (m²):", True, BLACK), (50, 300))

    return crear_boton_retorno()

# Función para mostrar la simulación de conducción
def mostrar_conduccion():
    screen.fill(WHITE)
    texto_titulo = font.render("Simulación de Conducción", True, BLACK)
    screen.blit(texto_titulo, (350, 50))

    # Crear cuadros de texto para ingresar manualmente los datos
    input_temp_superficie = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 150), (100, 30)),
        manager=manager
    )
    input_temp_base = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 200), (100, 30)),
        manager=manager
    )
    input_conductividad = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 250), (100, 30)),
        manager=manager
    )
    input_area = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 300), (100, 30)),
        manager=manager
    )
    input_grosor = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 350), (100, 30)),
        manager=manager
    )

    # Personalizar las cajas de texto
    input_temp_superficie.text_colour = BLACK
    input_temp_base.text_colour = BLACK
    input_conductividad.text_colour = BLACK
    input_area.text_colour = BLACK
    input_grosor.text_colour = BLACK

    input_temp_superficie.border_colour = WHITE
    input_temp_base.border_colour = WHITE
    input_conductividad.border_colour = WHITE
    input_area.border_colour = WHITE
    input_grosor.border_colour = WHITE

    # Mostrar resultados de la simulación
    resultado = calcular_conduccion()
    texto_resultado = font.render(f"Transferencia de Calor: {resultado:.2f} W", True, BLACK)
    screen.blit(texto_resultado, (300, 400))

    # Mostrar etiquetas para las variables alineadas a la izquierda
    screen.blit(font.render("Temp Superficie (°C):", True, BLACK), (50, 150))
    screen.blit(font.render("Temp Base (°C):", True, BLACK), (50, 200))
    screen.blit(font.render("Conductividad (W/m·K):", True, BLACK), (50, 250))
    screen.blit(font.render("Área (m²):", True, BLACK), (50, 300))
    screen.blit(font.render("Grosor (m):", True, BLACK), (50, 350))

    return crear_boton_retorno()

# Función para mostrar la simulación de radiación
def mostrar_radiacion():
    screen.fill(WHITE)
    texto_titulo = font.render("Simulación de Radiación", True, BLACK)
    screen.blit(texto_titulo, (350, 50))

    # Crear cuadros de texto para ingresar manualmente los datos
    input_temp_objeto = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 150), (100, 30)),
        manager=manager
    )
    input_temp_ambiente = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 200), (100, 30)),
        manager=manager
    )
    input_emisividad = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 250), (100, 30)),
        manager=manager
    )
    input_area = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((500, 300), (100, 30)),
        manager=manager
    )

    # Personalizar las cajas de texto
    input_temp_objeto.text_colour = BLACK
    input_temp_ambiente.text_colour = BLACK
    input_emisividad.text_colour = BLACK
    input_area.text_colour = BLACK

    input_temp_objeto.border_colour = WHITE
    input_temp_ambiente.border_colour = WHITE
    input_emisividad.border_colour = WHITE
    input_area.border_colour = WHITE

    # Mostrar resultados de la simulación
    resultado = calcular_radiacion()
    texto_resultado = font.render(f"Transferencia de Calor: {resultado:.2f} W", True, BLACK)
    screen.blit(texto_resultado, (300, 400))

    # Mostrar etiquetas para las variables alineadas a la izquierda
    screen.blit(font.render("Temp Objeto (K):", True, BLACK), (50, 150))
    screen.blit(font.render("Temp Ambiente (K):", True, BLACK), (50, 200))
    screen.blit(font.render("Emisividad:", True, BLACK), (50, 250))
    screen.blit(font.render("Área (m²):", True, BLACK), (50, 300))

    return crear_boton_retorno()

# Bucle principal
clock = pygame.time.Clock()
ejecutando = True
while ejecutando:
    time_delta = clock.tick(60) / 1000.0  # Tiempo entre frames
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        # Detectar los botones de las simulaciones
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

        manager.process_events(evento)

    # Dibujar la pantalla según el estado actual
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

# Salir
pygame.quit()
