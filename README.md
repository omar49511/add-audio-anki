# add-audio-anki
Esta aplicación permite descargar audio desde Google Translate y agregarlo a tarjetas de Anki automáticamente.

## Requisitos
> [!IMPORTANT]
> - [Anki](https://apps.ankiweb.net/) (debes tener anki).
> - [AnkiConnect](https://github.com/FooSoft/anki-connect) (instalar el complemento con el código 2055492159 desde el gestor de complementos de Anki).
> - [Python 3](https://www.python.org/downloads/) y la biblioteca `requests` (solo si deseas ejecutar el script y modificar el código en tu computadora).

## Instalación

Puedes descargar el ejecutable [aquí](https://github.com/omar49511/add-audio-anki/releases/download/v1.1.0/DownloadFrasesEnglish.exe), y para usarlo solo tienes que descargar anki connect siguiendo estos pasos:

>[!NOTE]
> #### Abre tu anki y ve a la seccion de Herramientas.
> ![image](https://github.com/user-attachments/assets/2fd48752-348a-4fe8-81b1-0882154becf9)
> #### selecciona complementos.
>   
>![image](https://github.com/user-attachments/assets/c88658ee-99ba-45bb-811f-4aec88f6b02b)
>
> #### selecciona descargar complementos y se abrira una ventana.
>   
>![image](https://github.com/user-attachments/assets/65ede6a7-107c-4a76-a403-751e9cacd5f7)
>
> #### Coloca el siguiente código
> ```
> 2055492159
> ```

## Capturas

![image](https://github.com/user-attachments/assets/43244911-d16c-46e1-aea2-960bfb9f6205)
![image](https://github.com/user-attachments/assets/f55161c4-a6a8-48ba-b52f-423f41429a43)
![image](https://github.com/user-attachments/assets/94e1a08e-39fa-49ab-a9c3-24ef02ee0ca1)
![image](https://github.com/user-attachments/assets/3270d9d3-78d0-480f-88e2-5219693c90e2)

Si eres programador y deseas modificar el código, asegúrate de tener Python instalado y la biblioteca `requests`:

```bash
pip install requests
