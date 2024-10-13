import pygame
import pygame_gui

# Inicializar Pygame
pygame.init()

# Crear ventana
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("ThermoSim")

# Crear el manejador de interfaz de pygame_gui
manager = pygame_gui.UIManager((800, 600))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Crear fuentes
font = pygame.font.Font(None, 36)

# Escenarios predefinidos con área y grosor
escenarios = {
    "Edificio": {'temp_interna': 20, 'temp_externa': -5, 'conductividad': 1.0, 'area': 10.0, 'grosor': 0.1},  # Área en m² y grosor en m
    "Ciudad": {'temp_ambiente': 30, 'velocidad_viento': 5, 'conductividad': 0.5, 'area': 10.0, 'grosor': 0.1},
    "Invernadero": {'temp_objetivo': 25, 'humedad': 60, 'conductividad': 1.5, 'area': 10.0, 'grosor': 0.1}
}

escenario_seleccionado = None
pantalla_actual = "menu"
input_boxes = []

# Función para limpiar elementos de la interfaz
def limpiar_elementos():
    global input_boxes
    input_boxes.clear()  # Limpiar cajas previas
    manager.clear_and_reset()  # Limpiar todos los elementos de pygame_gui

# Función para dibujar el menú
def mostrar_menu():
    screen.fill(WHITE)
    texto_titulo = font.render("Selecciona un Escenario", True, BLACK)
    screen.blit(texto_titulo, (250, 50))

    for i, escenario in enumerate(escenarios.keys()):
        texto = font.render(escenario, True, BLACK)
        screen.blit(texto, (300, 150 + i * 50))

# Función para detectar selección de escenario
def detectar_seleccion(posicion_mouse):
    global escenario_seleccionado, pantalla_actual
    for i, nombre in enumerate(escenarios.keys()):
        if 300 <= posicion_mouse[0] <= 500 and 150 + i * 50 <= posicion_mouse[1] <= 190 + i * 50:
            escenario_seleccionado = nombre
            pantalla_actual = "parametros"
            limpiar_elementos()  # Limpiar el menú anterior
            crear_input_boxes()

# Función para crear las cajas de texto para ingresar valores manualmente
def crear_input_boxes():
    global input_boxes
    parametros = escenarios[escenario_seleccionado]

    for i, (parametro, valor) in enumerate(parametros.items()):
        input_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((300, 200 + i * 60), (200, 30)),  # Ajustamos la posición vertical
            manager=manager
        )
        input_box.set_text(str(valor))  # Mostrar el valor por defecto
        input_boxes.append((parametro, input_box))

# Función para capturar los valores de los inputs y actualizar los parámetros
def actualizar_parametros():
    for parametro, input_box in input_boxes:
        try:
            valor = float(input_box.get_text())  # Convertir a número
            escenarios[escenario_seleccionado][parametro] = valor
        except ValueError:
            print(f"Valor no válido para {parametro}, usando el valor por defecto.")

# Función para mostrar la pantalla de parámetros
def mostrar_parametros():
    screen.fill(WHITE)
    texto_titulo = font.render(f"Parámetros de {escenario_seleccionado}", True, BLACK)
    screen.blit(texto_titulo, (250, 50))

    for i, (parametro, _) in enumerate(escenarios[escenario_seleccionado].items()):
        texto = font.render(f"{parametro}: {escenarios[escenario_seleccionado][parametro]:.2f}", True, BLACK)
        screen.blit(texto, (100, 200 + i * 60))  # Ajustamos la posición vertical

    # Actualizar y mostrar resultado de la simulación
    resultado = calcular_transferencia_calor()
    texto_resultado = font.render(resultado, True, BLACK)
    screen.blit(texto_resultado, (100, 200 + len(escenarios[escenario_seleccionado]) * 60))

# Función para calcular la transferencia de calor
def calcular_transferencia_calor():
    actualizar_parametros()  # Asegúrate de que los parámetros estén actualizados
    if escenario_seleccionado == "Edificio":
        k = escenarios[escenario_seleccionado]['conductividad']  # Conductividad
        A = escenarios[escenario_seleccionado]['area']  # Área
        d = escenarios[escenario_seleccionado]['grosor']  # Grosor
        delta_T = escenarios[escenario_seleccionado]['temp_interna'] - escenarios[escenario_seleccionado]['temp_externa']  # Diferencia de temperatura
        
        # Aplicar la fórmula de transferencia de calor
        q = (k * A * delta_T) / d
        return f"Transferencia de calor: {q:.2f} W"
    else:
        return "Simulación en desarrollo..."

# Bucle principal
clock = pygame.time.Clock()
ejecutando = True
while ejecutando:
    time_delta = clock.tick(60) / 1000.0  # Tiempo entre frames
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and pantalla_actual == "menu":
            detectar_seleccion(pygame.mouse.get_pos())

        if evento.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            # Actualizar automáticamente los parámetros cuando se termina de editar
            actualizar_parametros()

        manager.process_events(evento)

    # Dibujar la pantalla según el estado actual
    if pantalla_actual == "menu":
        mostrar_menu()
    elif pantalla_actual == "parametros":
        mostrar_parametros()

    manager.update(time_delta)
    manager.draw_ui(screen)

    # Actualizar pantalla
    pygame.display.flip()

# Salir
pygame.quit()
