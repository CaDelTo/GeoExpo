import numpy as np
import matplotlib.pyplot as plt
import time  # Para introducir un pequeño retraso entre las actualizaciones

# Propiedades del agua
rho = 1000  # kg/m³ (densidad)
c_p = 4186  # J/kg·K (capacidad calorífica)
h = 100      # W/m²·K (coeficiente de convección)
A = 1     # m² (área de la superficie)
T_inicial = 20  # °C (temperatura inicial del agua)
T_s = 100  # °C (temperatura de la superficie)
V = 0.05  # m³ (volumen de agua)

# Constantes
dt = 1  # tiempo en segundos
tiempo_total = 10000 # total de segundos
num_pasos = int(tiempo_total / dt)

# Arreglos para almacenar resultados
T = np.zeros(num_pasos)
Q_values = np.zeros(num_pasos)  # Arreglo para la transferencia de calor
T[0] = T_inicial

# Inicializar la figura para la temperatura
plt.ion()  # Activar el modo interactivo
fig1, ax1 = plt.subplots()
line1, = ax1.plot(np.arange(num_pasos) * dt, T, color='b')
ax1.set_xlim(0, tiempo_total)
ax1.set_ylim(0, 110)
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Temperatura (°C)')
ax1.set_title('Cambio de temperatura del agua con el tiempo')
ax1.grid()

# Añadir texto para mostrar la temperatura actual
temp_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes, fontsize=12, color='red')
q_text = ax1.text(0.05, 0.85, '', transform=ax1.transAxes, fontsize=12, color='green')
# Inicializar la figura para la transferencia de calor
fig2, ax2 = plt.subplots()
line2, = ax2.plot(np.arange(num_pasos) * dt, Q_values, color='g')
ax2.set_xlim(0, tiempo_total)
ax2.set_ylim(0, 10000)  # Ajusta este valor según lo que esperas ver
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Transferencia de Calor (W)')
ax2.set_title('Transferencia de Calor a través del Tiempo')
ax2.grid()

# Simulación
for t in range(1, num_pasos):
    # Cálculo del flujo de calor Q
    Q = h * A * (T_s - T[t-1])  # Flujo de calor basado en la diferencia de temperatura
    Q_values[t] = Q  # Almacenar el flujo de calor en el arreglo
    # Cálculo del cambio de temperatura
    dT_dt = Q / (rho * c_p * V)  # Cambio de temperatura por unidad de tiempo
    # Actualizar la temperatura
    T[t] = T[t-1] + dT_dt * dt  # Sumar el cambio a la temperatura anterior
    
    # Actualizar el gráfico de temperatura
    line1.set_ydata(T)  # Actualizar los datos de la línea de temperatura
    plt.draw()  # Redibujar la figura de temperatura
    plt.pause(0.1)  # Pausa para actualizar la visualización de temperatura
    
    # Actualizar el texto de temperatura
    temp_text.set_text(f'Temperatura Actual: {T[t]:.2f} °C')  # Mostrar temperatura con 2 decimales
    
    # Actualizar el gráfico de transferencia de calor
    line2.set_ydata(Q_values)  # Actualizar los datos de la línea de transferencia de calor
    ax2.set_ylim(0, max(Q_values.max(), 10000))  # Ajustar el límite superior del eje Y si es necesario
    q_text.set_text(f'Transferencia de Calor: {Q:.2f} W')  # Mostrar transferencia de calor con 2 decimales
    plt.draw()  # Redibujar la figura de transferencia de calor
    plt.pause(0.0001)  # Pausa para actualizar la visualización de transferencia de calor

plt.ioff()  # Desactivar el modo interactivo
plt.show()  # Mostrar los gráficos finales
