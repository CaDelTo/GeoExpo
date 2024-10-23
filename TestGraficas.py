import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Inicializar pygame
pygame.init()
width, height = 800, 600  # Dimensiones de la ventana
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simulación de Transferencia de Calor')

# Fuente para el texto
font = pygame.font.SysFont(None, 24)

# Propiedades del agua
rho = 1000  # kg/m³ (densidad)
c_p = 4186  # J/kg·K (capacidad calorífica)
h = 100     # W/m²·K (coeficiente de convección)
A = 0.5     # m² (área de la superficie)
T_inicial = 20  # °C (temperatura inicial del agua)
T_s = 100  # °C (temperatura de la superficie)
V = 0.05   # m³ (volumen de agua)

# Constantes
dt = 1  # tiempo en segundos
tiempo_total = 100  # total de segundos
num_pasos = int(tiempo_total / dt)

# Arreglos para almacenar resultados
T = np.zeros(num_pasos)
Q_values = np.zeros(num_pasos)  # Arreglo para la transferencia de calor
T[0] = T_inicial

# Función para convertir gráficos de matplotlib a una imagen que pueda usar pygame
def draw_figure(fig, size):
    canvas = FigureCanvas(fig)
    canvas.draw()
    raw_data = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8)  # Convertir a bytes
    raw_data = raw_data.reshape(canvas.get_width_height()[::-1] + (4,))  # Redimensionar el array
    raw_data = np.roll(raw_data, 3, axis=2)  # Cambiar de ARGB a RGBA
    return pygame.image.frombuffer(raw_data.flatten(), size, 'RGBA')

# Función para renderizar texto en pygame
def render_text(text, pos, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Inicializar figuras de matplotlib
fig1, ax1 = plt.subplots(figsize=(4, 3))
line1, = ax1.plot(np.arange(num_pasos) * dt, T, color='b')
ax1.set_xlim(0, tiempo_total)
ax1.set_ylim(0, 110)
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Temperatura (°C)')
ax1.set_title('Cambio de temperatura')
ax1.grid()

fig2, ax2 = plt.subplots(figsize=(4, 3))
line2, = ax2.plot(np.arange(num_pasos) * dt, Q_values, color='g')
ax2.set_xlim(0, tiempo_total)
ax2.set_ylim(0, 10000)
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Transferencia de Calor (W)')
ax2.set_title('Transferencia de Calor')
ax2.grid()

# Loop de simulación y pygame
running = True
for t in range(1, num_pasos):
    if not running:
        break

    # Cálculo del flujo de calor Q
    Q = h * A * (T_s - T[t-1])  # Flujo de calor basado en la diferencia de temperatura
    Q_values[t] = Q  # Almacenar el flujo de calor en el arreglo
    # Cálculo del cambio de temperatura
    dT_dt = Q / (rho * c_p * V)  # Cambio de temperatura por unidad de tiempo
    # Actualizar la temperatura
    T[t] = T[t-1] + dT_dt * dt  # Sumar el cambio a la temperatura anterior
    
    # Actualizar gráficos de matplotlib
    line1.set_ydata(T)  # Actualizar los datos de la línea de temperatura
    line2.set_ydata(Q_values)  # Actualizar los datos de la línea de transferencia de calor
    ax2.set_ylim(0, max(Q_values.max(), 10000))  # Ajustar el límite superior del eje Y si es necesario
    
    # Renderizar gráficos en pygame
    img1 = draw_figure(fig1, (400, 300))  # Gráfico de temperatura
    img2 = draw_figure(fig2, (400, 300))  # Gráfico de transferencia de calor
    
    # Dibujar gráficos en la ventana de pygame
    screen.fill((255, 255, 255))  # Fondo blanco
    screen.blit(img1, (0, 0))     # Dibujar gráfico de temperatura
    screen.blit(img2, (400, 0))   # Dibujar gráfico de transferencia de calor
    
    # Mostrar valores actuales de las gráficas
    render_text(f'Temperatura actual: {T[t]:.2f} °C', (10, 310))
    render_text(f'Transferencia de calor: {Q_values[t]:.2f} W', (410, 310))

    pygame.display.flip()         # Actualizar la pantalla
    
    # Controlar eventos de pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    time.sleep(0.1)  # Pausa para simular el tiempo entre cálculos

# Cerrar pygame
pygame.quit()
