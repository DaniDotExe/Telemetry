# Cansat Laika

_CanSat autónomo que mide un perfil atmosférico y transmite las variables e imágenes desde la estratosfera._

## Mockup y maquetación 🚀

_En este repositorio se presentan los dos mockups y su respectiva maquetación en python._

**Laika GUI:**
<a>
<img width="850" src="https://github.com/DaniSTexe/Telemetry/blob/main/sources/laika_final.jpg">
</a>



### Pre-requisitos 📋

_1) Python 3.7.9_

_**Para Windows**: Anaconda_
    
_2) Entorno virtual_

_En el terminal de anaconda lo puede crear usando_

```
conda create -n laika python=3.7.9
```

### Instalación 🔧

_Despues de tener el entorno virtual listo_

_En el powershell de anaconda ingrese_

```
activate laika
cd {$path}
conda install pip
```

_Ahora instale los requerimientos_

```
pip install -r requirements.txt
```

_Compruebe la instalación codificando_
```
python diseno.py 
```
_Debería aparecer la interfaz sin funcionalidad._

_Y una vez se encuentre creado el enlace de comunicación ejecute_

```
python MAIN.py
```




## Construido con 🛠️

* [Python](https://docs.python.org/3/) - Lenguaje principal
* [Qt-Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html) - Herramienta para la creación de la interfaz

## Documentación del proyecto 📖

* [Documento](https://github.com/DaniSTexe/laika/blob/main/Documento.pdf)

## Autores ✒️

* **Oscar Olejua** - *Diseño y maquetación* - [Daniexe](https://github.com/DaniSTexe)
* **Juan Suarez** - *Recepción de datos* - [MrSuaqui](https://github.com/jpsuarezq)
