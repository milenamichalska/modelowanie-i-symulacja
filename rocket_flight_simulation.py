#symulator lotu rakiety modelarskiej
import math
import numpy as np
import matplotlib.pyplot as plt

#parametry symulacji
time_interval = 0.1 #interwal dla kalkulacji w sekundach
time = 100.0 #czas symulacji

#parametry wejsciowe
empty_rocket_mass = 0.1 #kg
propellant_mass = 0.014 #kg
motor_impulse = 10.0 #Ns
motor_thrust = 6.0 #N
drag_coefficent = 0.75 #wspolczynnik oporu powietrza
rocket_diameter = 0.1 #m
parachute_diameter = 0.6 #m
parachute_deployment_delay = 3 #s

#wyliczenia i zmienne poczatkowe
burn_time = float(motor_impulse / motor_thrust)
mass_decrement = propellant_mass / burn_time #predkosc spalania paliwa
rocket_area = math.pi * (rocket_diameter / 2)**2

mass = empty_rocket_mass + propellant_mass
rho = 1.22 #gestosc powietrza
g = 9.8 #przyciaganie ziemskie

flight_data = [[0, 0, 0]] #wysokosc, predkosc, przyspieszenie
i = 0

#petla symulacji
for t in np.arange(0, time, time_interval):
    i += 1
    v0 = flight_data[i - 1][1]
    h0 = flight_data[i - 1][0]

    rho = 1.22 * (0.9**(h0/1000))
    t = i * time_interval

    if (t < burn_time):
        mass -= mass_decrement * time_interval #rakieta zmniejsza masę podczas spalania paliwa

    if (t >= burn_time + parachute_deployment_delay):
        rocket_area = math.pi * (parachute_diameter / 2)**2 #po rozłożeniu spadochronu 'powierzchnia' rakiety zwieksza sie
    
    if (v0 != 0): drag_force = 0.5 * rho * drag_coefficent * rocket_area * v0**2 * (v0 / abs(v0))  #sila oporu powietrza
    else: drag_force = 0

    rocket_force = - drag_force - mass * g
    if (t < burn_time): rocket_force += motor_thrust #w czasie dzialania silnika na rakiete dziala sila ciągu silnika

    acceleration = rocket_force / mass #druga zasada dynamiki Newtona
    velocity = v0 + acceleration * time_interval
    altitude = h0 + velocity * time_interval

    if (altitude <= 0): break #przerwanie symulacji gdy rakieta wyladuje
    flight_data.append([altitude, velocity, acceleration])

    plt.scatter(t, altitude, marker='o', color = 'hotpink')
    plt.pause(0.05)

#print(flight_data)
print(t)
plt.show()
