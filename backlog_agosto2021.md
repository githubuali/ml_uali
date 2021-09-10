## Backlog

* Armar una API en flask con darknet desde OpenCV (agosto2021).
* Entrenar nuevo modelo usando el dataset Visdrone (agosto2021).
* Armar script para evaluar, filtrar y medir las categorias del dataset (como lo hace roboflow).

> **Nota:** todos los branchs de "feature" se prueban localmente. Solo se prueba en server el branch develop.

## New feature
* Definir estructura de la API.
* Entrenamiento con Visdrone.

## Branchs

- Master
- Develop
    - str_API
        - medium
        - pyimage
    - visdroneToYolo

### Definir estructura de la API (branch - str_API)

**Roadmap**
* Definir la la referencia a utilizar 
    - [x] Prueba medium (branch - medium).
        [Referencia](https://medium.com/analytics-vidhya/object-detection-using-yolo-v3-and-deploying-it-on-docker-and-minikube-c1192e81ae7a)
    - [x] Prueba pyimage (branch - pyimage).
        [Referencia](https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/)
        
## Entrenamiento con Visdrone (branch - visdroneToYolo)

**Roadmap**
- [x] Modificar el formato del dataset. De Visdrone a Yolo.
	* [Formato Visdrone - Object Detection in Images](http://aiskyeye.com/evaluate/results-format/)
    * [Dataset download - Task 1: Object Detection in Images](https://github.com/VisDrone/VisDrone-Dataset)
    * [Documentacón de datasets](https://docs.google.com/spreadsheets/d/1atzYZL8IrZ4RDQQDC8rHAR0ydo9VwBXqHv8p4fDXsVo/edit#gid=968418162&range=B8)

- [x] Pasar todo al formato definido.
- [x] Agregar docstring.
- [x] Visualizar algunos ejemplos para corroborrar que son correctos.
- [x] Descargar dataset para "obj" y "test" (desde https://github.com/VisDrone/VisDrone-Dataset), modificar formato usando el script `visdroneToYolo.py`
- [x] Pasar etiquetas e imagenes en una misma carpeta.
- [x] Armar readme de dataset.
- [x] Subir material al GDrive.
- [x] armar "data_training.zip"

