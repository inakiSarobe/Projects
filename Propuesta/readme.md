# Propuesta a ...!

Pequeña app en Python que muestra una ventana con la pregunta romántica: **"¿Quieres ser mi novia?"**. Tiene un botón **Sí** que muestra un mensaje tierno y una animación de corazones, y un botón **No** que evade el cursor teletransportándose a otra posición (sin animaciones) para que no pueda clicarse fácilmente.

---

## Requisitos

- Python 3.x (recomendado 3.8+).
- `tkinter` (viene incluido en la mayoría de instalaciones de Python). En algunas distros Linux puede requerir instalar `python3-tk` o paquete equivalente.

---

## Cómo ejecutar

1. Clona o descarga el repositorio en tu máquina.
2. Abre una terminal en la carpeta donde está `Propuesta.py`.
3. Ejecuta:

```bash
python3 Propuesta.py
```

> En Windows puede que solo necesites `python Propuesta.py`.

La ventana abrirá con tamaño fijo y no redimensionable. Pasa el cursor por el botón **No** para ver cómo evade, y presiona **Sí** para ver la animación final.

---

## Cómo modificar el nombre (personalizar a quien se la proponés)

Dentro del archivo `Propuesta.py` hay una variable fácilmente editable:

```python
# Cambia este valor por el nombre que quieras
person_name = "Yera"
```

Cambia `"Yera"` por el nombre deseado y guarda el archivo. Vuelve a ejecutar `python3 Propuesta.py` para ver el cambio reflejado en los mensajes.

---

## Variables útiles que podés ajustar

- `WINDOW_WIDTH`, `WINDOW_HEIGHT` — tamaño de la ventana (por defecto 520×340). Si cambiás estos valores, tené en cuenta mantener proporciones para que los elementos no queden desalineados.
- `MIN_DISTANCE` — distancia mínima (en píxeles) que el botón **No** debe alejarse del cursor al teletransportarse. Valor por defecto: `120`. Aumentalo si querés que sea más difícil pillarlo.

---

## Personalizaciones rápidas (ideas)

- Cambiar colores (variables `BG_COLOR`, `PANEL_COLOR`, `ACCENT`, `TEXT_COLOR`).
- Ajustar textos (título, subtítulo, mensaje final) dentro del archivo para hacerlo más personal.
- Agregar un contador visible de intentos, o un _easter egg_ que se active con una secuencia de teclas.

---

## Problemas comunes

- **No se abre la app / error de Tkinter**: en Linux instala `python3-tk` o el paquete equivalente para tu distro.
- **Texto cortado en pantallas con escalado (DPI alto)**: podés reducir `FONT_TITLE` o ajustar `WINDOW_WIDTH`/`WINDOW_HEIGHT`.

---

## Buenas prácticas y un mensaje importante

Esta app fue creada con una intención **romántica y divertida**. Cuando programamos, tenemos la responsabilidad de escribir código que respete y cuide a los demás. Algunas recomendaciones:

- Escribe código legible y bien comentado para que otros (y tu yo del futuro) entiendan lo que hiciste.
- No uses técnicas engañosas o maliciosas para manipular a las personas. Esta aplicación es un juego inocente y afectuoso; evita usar programación para causar daño, invadir privacidad o engañar.

> **Crear buen código es también crear con empatía.**

---

## Un cierre cariñoso

Si estás compartiendo este momento con ...: ¡muchas felicidades! ❤️

El propósito de esta app es expresar amor y cariño de una manera creativa. El código puede ser pequeño, pero la intención es grande: que lo que crees haga feliz a alguien.

---

## Licencia

Usa y modifica este proyecto libremente para fines personales o educativos. Si lo compartes públicamente, agradecería una mención a quien lo creó.

---
