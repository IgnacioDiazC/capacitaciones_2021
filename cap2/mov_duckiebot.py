#!/usr/bin/env python

"""
Este programa permite mover al Duckiebot dentro del simulador
usando el teclado.
"""

import sys
import argparse
import gym
import gym_duckietown
from gym_duckietown.envs import DuckietownEnv
import numpy as np
import cv2

# Se leen los argumentos de entrada
parser = argparse.ArgumentParser()
parser.add_argument('--env-name', default="Duckietown-udem1-v1")
parser.add_argument('--map-name', default='udem1')
parser.add_argument('--distortion', default=False, action='store_true')
parser.add_argument('--draw-curve', action='store_true', help='draw the lane following curve')
parser.add_argument('--draw-bbox', action='store_true', help='draw collision detection bounding boxes')
parser.add_argument('--domain-rand', action='store_true', help='enable domain randomization')
parser.add_argument('--frame-skip', default=1, type=int, help='number of frames to skip')
parser.add_argument('--seed', default=1, type=int, help='seed')
args = parser.parse_args()

# Definición del environment
if args.env_name and args.env_name.find('Duckietown') != -1:
    env = DuckietownEnv(
        seed = args.seed,
        map_name = args.map_name,
        draw_curve = args.draw_curve,
        draw_bbox = args.draw_bbox,
        domain_rand = args.domain_rand,
        frame_skip = args.frame_skip,
        distortion = args.distortion,
    )
else:
    env = gym.make(args.env_name)

# Se reinicia el environment
env.reset()


while True:

    # Captura la tecla que está siendo apretada y almacena su valor en key
    key = cv2.waitKey(30)

    # Si la tecla es Esc, se sale del loop y termina el programa
    if key == 27:
        break

    # La acción de Duckiebot consiste en dos valores:
    # velocidad lineal y velocidad de giro
    # En este caso, ambas velocidades son 0 (acción por defecto)
    action = np.array([0.0, 0.0])

    # Definir acción en base a la tecla apretada

    # Esto es avanzar recto hacia adelante al apretar la tecla w
    if key == ord('w'):
        action = np.array([0.60, 0.0])

    ### AGREGAR MÁS COMPORTAMIENTOS ###

    # Esto es retroceder recto hacia atras al apretar la tecla s
    if key == ord('s'):
        action = np.array([-0.40, 0.0])

    # Esto es rotar hacia la derecha al apretar la tecla d
    if key == ord('d'):
        action = np.array([0.0, -0.5])

    # Esto es rotar hacia la izquierda al apretar la tecla a
    if key == ord('a'):
        action = np.array([0.0, 0.5])

    # Esto es girar hacia la derecha al apretar la tecla e
    if key == ord('e'):
        action = np.array([0.2, -0.5])

    # Esto es girar hacia la izquierda al apretar la tecla q
    if key == ord('q'):
        action = np.array([0.2, 0.5])



    # Se ejecuta la acción definida anteriormente y se retorna la observación (obs),
    # la evaluación (reward), etc
    obs, reward, done, info = env.step(action)
    # obs consiste en un imagen de 640 x 480 x 3

    # done significa que el Duckiebot chocó con un objeto o se salió del camino
    if done:
        print('done!')
        # En ese caso se reinicia el simulador
        env.reset()

    # Se muestra en una ventana llamada "patos" la observación del simulador
    cv2.imshow("patos", cv2.cvtColor(obs, cv2.COLOR_RGB2BGR))


# Se cierra el environment y termina el programa
env.close()
