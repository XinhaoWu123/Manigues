# Instrucciones para descargar el proyecto QuizzBattle

Este documento explica cómo descargar el proyecto **QuizzBattle** desde GitHub. El proyecto se encuentra dentro del repositorio público **Manigues**, concretamente en la carpeta `quizzbattle` de la rama `main`.[1]

| Dato | Valor |
| --- | --- |
| Nombre del proyecto | **QuizzBattle** |
| Carpeta del proyecto | `quizzbattle` |
| Rama principal | `main` |

## 1. Descargar el proyecto usando Git

La forma más recomendable de descargar el proyecto es clonar el repositorio completo desde GitHub. Para ello, abre una terminal en la carpeta donde quieras guardar el proyecto y ejecuta el siguiente comando:

```bash
git clone https://github.com/XinhaoWu123/Manigues.git
```

Después de clonar el repositorio, entra en la carpeta principal:

```bash
cd Manigues
```

Como **QuizzBattle** está dentro de una subcarpeta del repositorio, accede al proyecto con este comando:

```bash
cd quizzbattle
```

Al terminar, deberías encontrarte dentro de una ruta similar a esta:

```text
Manigues/quizzbattle
```

## 2. Descargar el proyecto como archivo ZIP

Si no quieres usar Git, también puedes descargar el repositorio desde GitHub como archivo comprimido. Para ello, entra en el repositorio desde el navegador, pulsa el botón **Code** y selecciona la opción **Download ZIP**.[1]

Una vez descargado el archivo, descomprímelo en tu equipo. Después, abre la carpeta resultante y entra en:

```text
Manigues-main/quizzbattle
```

Esta opción es más sencilla para una descarga puntual, aunque no permite actualizar el proyecto fácilmente con comandos como `git pull`.

| Método | Ventaja principal | Cuándo usarlo |
| --- | --- | --- |
| `git clone` | Permite actualizar el proyecto fácilmente | Recomendado para desarrollo |
| Download ZIP | No requiere usar comandos de Git | Recomendado para una descarga rápida |

## 3. Resumen rápido de comandos

La descarga básica del proyecto se puede resumir con los siguientes comandos:

```bash
git clone https://github.com/XinhaoWu123/Manigues.git
cd Manigues/quizzbattle
```

En Windows, la navegación de carpetas cambia ligeramente:

```bash
git clone https://github.com/XinhaoWu123/Manigues.git
cd Manigues\quizzbattle
```