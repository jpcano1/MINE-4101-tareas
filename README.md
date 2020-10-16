# MINE-4101-tareas
## Repositorio de la materia Applied Data Science
***
- Abra el Notebook que desea ejecutar, ya sea desde su PC o en [GitHub](https://github.com/jpcano1/MINE-4101-tareas.git)
- Haga click donde dice **Run in Google Colab**
- Click en **File >> Save a copy in Drive...** para salvar su progreso en drive
- Ejecute el siguiente código sobre la primera celda del notebook

```python
!shred -u setup_colab.py
!wget -q "https://raw.githubusercontent.com/jpcano1/MINE-4101-tareas/master/setup_colab.py" -O setup_colab.py
import setup_colab as setup
setup.setup_general()
```