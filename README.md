<h1 align="center">AGROPLANT</h1>

<p align="center"><strong>Un simulador de agricultura que se juega entre el tablero y el móvil.</strong></p>

<p align="center">
  <img alt="NASA Space Apps 2025" src="https://img.shields.io/badge/NASA%20Space%20Apps-2025-0B3D91?style=flat-square">
  <img alt="Space Apps Zaragoza, premio local 2025" src="https://img.shields.io/badge/Space%20Apps%20Zaragoza-premio%20local-2E7D32?style=flat-square">
</p>

<p align="center">
  <img src="assets/hero.jpg" alt="AGROPLANT: campo de cultivo al atardecer" width="100%">
</p>

## ¿Qué es AGROPLANT?

**AGROPLANT** es un simulador de agricultura para jugar con las manos y con el móvil al mismo tiempo. Te pone en la piel de un agricultor que tiene que sacar adelante una cosecha en sitios donde nada es fácil: el desierto de Arabia Saudí, en medio de la selva amazónica o junto a una central nuclear en Kazajistán.

Cada partida es una misión. Tienes que cultivar tomates, patatas o alfalfa, decidir cuándo regar y cuándo abonar, y llegar al final con la cosecha adelante, algo de dinero en el bolsillo y la tierra en condiciones. El reto no es solo producir más: es hacerlo sin pasarte con los fertilizantes, porque cada decisión tiene un precio para el bolsillo y para el planeta.

## Cómo funciona el juguete

<p align="center">
  <img src="assets/como-funciona.jpg" alt="Esquema de AGROPLANT: datos de NASA, tablero con ESP32, app y juego físico" width="100%">
</p>

El juego tiene dos mitades que se hablan entre sí: un tablero físico con fichas y sensores, y una app que se abre en el navegador del móvil.

1. **El tablero es la finca.** Nueve parcelas, de la A1 a la C3, con su hueco para cada cultivo. El tablero está conectado: lleva sensores de suelo y un lector de fichas.
2. **Las fichas son los cultivos.** Tomate, patata y alfalfa. Cada ficha lleva un chip RFID, como un llavero de portal.
3. **Acerca la ficha al lector.** La app reconoce el cultivo y actualiza esa parcela en el móvil. No hay que instalar nada: el móvil se conecta al Wi-Fi del tablero y abre la app en el navegador.
4. **Mira el parte de la parcela.** Tipo de cultivo, estado, riego, nutrientes, puntos eco y edad.
5. **Toma una decisión.** Regar, abonar o nitrogenar. Cada acción gasta parte del presupuesto y tiene consecuencias.
6. **Pasa el turno.** El tiempo avanza, el cultivo envejece y el clima del escenario pasa factura.
7. **Cumple la misión.** Cosecha, vende y termina con la cosecha adelante, dinero en el bolsillo y la tierra en condiciones.

<p align="center">
  <img src="assets/juego-en-mesa.jpg" alt="El tablero, las fichas, el presupuesto y la app de AGROPLANT" width="80%"><br>
  <sub>El tablero, las fichas, el presupuesto y la app: así se juega.</sub>
</p>

## La app

La app es el cuaderno de campo del jugador. En la pantalla principal ves las nueve parcelas y el turno; al abrir una, aparece su ficha.

| Parcelas | Detalle del cultivo |
| :---: | :---: |
| <img src="assets/app-parcelas.png" width="270" alt="Pantalla de parcelas de la app"> | <img src="assets/app-cultivo.png" width="270" alt="Detalle de un cultivo en la app"> |
| La finca de un vistazo | Riego, nutrientes, puntos eco y edad |

| En la app | Qué te cuenta |
| --- | --- |
| **TIPO** | Tomate, patata o alfalfa. |
| **ESTADO** | Cómo está el cultivo. |
| **RIEGO** | De 0 a 100 %. |
| **NUTRIENTES** | De 0 a 100 %. |
| **PUNTOS ECO** | Lo respetuosa que es la cosecha con la tierra. |
| **EDAD** | Turnos desde que se plantó. |

Y estas acciones:

- **Regar** — repone el agua de la parcela.
- **Abonar** — sube los nutrientes.
- **Nitrogenar** — usa fertilizante nitrogenado: empuja la producción, pero baja los puntos eco y el valor de la cosecha.
- **Cambio de turno** — avanza el tiempo.

## Tres sitios, tres problemas

Los escenarios no son decorados: cada uno tiene su clima, su suelo y su dificultad.

- **Arabia Saudí** — calor, sol y muy poca agua. Aquí cada gota cuenta.
- **Amazonas** — humedad, lluvia y una vegetación que no perdona. El exceso también es un problema.
- **Kazajistán** — un entorno industrial, junto a una central nuclear, donde cultivar no es lo primero que uno esperaría.

Y no son climas inventados: salen de datos reales de la NASA.

## Vídeos

Si quieres verlo en movimiento:

| | Vídeo | Qué se ve |
| :---: | --- | --- |
| ▶ | **[Demo (31 s)](media/agroplant-demo.mp4)** | Del diseño del tablero a una partida en tiempo real. |
| ▶ | **[Explicación (1 min 10 s)](media/agroplant-explicacion.mp4)** | El equipo cuenta qué es AGROPLANT y cómo se juega. |

Los dos vídeos están en el repositorio, en `media/`, en formato MP4.

## Por qué lo hicimos

Porque la agricultura suele explicarse con titulares: sequía, precios, fertilizantes, emisiones. Nosotros queríamos que se entendiera con las manos. Que te duela gastar el presupuesto, que te tiente el nitrógeno, que veas que una cosecha no sale sola.

AGROPLANT no busca dar la razón a nadie: busca que el jugador se ponga un rato en la piel de quien tiene que decidir con el clima en contra, el dinero justo y la tierra en juego.

## Datos reales de NASA

Para que los escenarios no sean ciencia ficción, el juego se apoya en datos públicos de la NASA. El extractor [`data/clima_json_microclimas.py`](data/clima_json_microclimas.py) descarga series diarias de **NASA POWER** —temperatura, precipitación, humedad y radiación solar— para un área y las resume en variables de microclima. Esa es la materia prima con la que se construyen las condiciones de cada nivel. El proyecto también explora datos de **NASA AppEEARS** para caracterizar distintos ecosistemas.

[Instrucciones del extractor →](data/README.md)

## Equipo y premio

**Diego López Esteban · Martín Rincón Gálvez · Sergio Toro Codo**

AGROPLANT se presentó al reto **NASA Farm Navigators** de la **NASA Space Apps Challenge 2025**, en **Space Apps Zaragoza** (12ª edición, 4–5 de octubre de 2025). El proyecto recibió el **premio local** de la edición.

<p align="center">
  <img src="assets/premio.jpg" alt="Entrega de premios de Space Apps Zaragoza 2025" width="80%"><br>
  <sub>Entrega de premios de Space Apps Zaragoza 2025.</sub>
</p>

<details>
<summary><strong>English summary</strong></summary>

<br>

AGROPLANT is a hybrid physical-digital farming game created for the 2025 NASA Space Apps Challenge. Players grow tomatoes, potatoes and alfalfa across three climate-driven scenarios — Saudi Arabia, the Amazon and Kazakhstan — using a board with RFID crop tiles and soil sensors that talks to a phone app. Real NASA climate data (POWER and AppEEARS) sets the conditions for each mission. The project received a local award at Space Apps Zaragoza 2025.

</details>

<p align="center">
  <sub>© 2025 Diego López Esteban · Martín Rincón Gálvez · Sergio Toro Codo · Zaragoza</sub><br>
  <sub>Datos: <a href="https://power.larc.nasa.gov/">NASA POWER</a> · <a href="https://appeears.earthdatacloud.nasa.gov/">NASA AppEEARS</a> · Evento: <a href="https://www.spaceappschallenge.org/">NASA Space Apps Challenge</a></sub><br>
  <sub>Más proyectos en <a href="https://github.com/sejotta">github.com/sejotta</a></sub>
</p>
