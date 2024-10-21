# add-audio-anki
Esta aplicación permite descargar audio desde Google Translate y agregarlo a tarjetas de Anki automáticamente.

## Requisitos
> [!IMPORTANT]
> - [Anki](https://apps.ankiweb.net/) (debes tener anki).
> - [AnkiConnect](https://github.com/FooSoft/anki-connect) (instalar el complemento con el código 2055492159 desde el gestor de complementos de Anki).
> - [Python 3](https://www.python.org/downloads/) y la biblioteca `requests` (solo si deseas ejecutar el script y modificar el código en tu computadora).

## Instalación

Si no eres programador, puedes descargar el ejecutable [aquí](https://github.com/omar49511/add-audio-anki/releases/download/v1.0-beta/DownloadFrasesEnglish.exe) y usarlo solo sigue los siguientes pasos.
>[!NOTE]
> <span style="font-size:20px;">Abre tu anki y ve a la seccion de Herramientas.</span>
> ![image](https://github.com/user-attachments/assets/2fd48752-348a-4fe8-81b1-0882154becf9)
> - selecciona complementos.
>   
>![image](https://github.com/user-attachments/assets/c88658ee-99ba-45bb-811f-4aec88f6b02b)
>
> - selecciona descargar complementos y se abrira una ventana como esta.
>   
>![image](https://github.com/user-attachments/assets/65ede6a7-107c-4a76-a403-751e9cacd5f7)
>
> - Coloca el siguiente código
> ```
> 2055492159
> ```




Si eres programador y deseas modificar el código, asegúrate de tener Python instalado y la biblioteca `requests`:

```bash
pip install requests
