<br />
<p align="center">
  <a href="https://github.com/bladhl/nlp-pl-transparency">
    <img src="https://static.dw.com/image/50684147_303.jpg" alt="Logo" width="500" height="300">
  </a>
  <h2 align="center">Proyecto - Transparencia Leyes - Segunda unidad</h2>
</p>

- **Universidad Nacional de San Antonio Abad del Cusco**
- **Escuela Profesional de Ingeniería Informática y de Sistemas**
- **Procesamiento de Lenguaje Natural - Grupo 4**
### Docente:
- **Roxana Lisette Quintanilla Portugal** - [Concytec](http://dina.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do;jsessionid=f564431f36070c2b4a0e4a590b74?id_investigador=40930).

## Descripción 
  Durante esta unidad nuestro trabajo consistió en la aplicación de nuevas estrategias de Procesamiento de Lenguaje Natural en el trabajo de reconocimiento de transparencia de las propuestas de ley del congreso de nuestro país. Haciendo uso de Clustering, LDA, Postagging y NER, con una vista a futuro de análisis de sentimientos en base a la opinión de la población sobre estas propuestas de ley.

## Proceso de Ejecución 
- En primer lugar, buscamos la manera de mejorar el corpus con el que trabajar para filtrar mejor el trabajo relacionado con la transparencia, para esto, se hizo un filtrado de términos utilizados en el argot de la abogacía.
- En segundo lugar, aplicamos las técnicas de Clustering y LDA para poder definir nuestra manera de agrupar los expedientes, siguiendo el ejemplo del paper mostrado por la docente, pero el resultado era insuficiente. Así que optamos por seguir el modelo de clusters propuesto en el paper, pero el resultado no fue tan satisfactorio como se esperaba dada la diferencia de leyes entre el nuestro país y el del ejemplo, Brasil.
- En tercer lugar, hicimos uso de Postagging y NER. en este caso, el contexto era fundamental, así que reestructuramos el corpus sin un preprocesamiento para que las oraciones se mantengan en forma y fondo. La limitante en este caso estuvo dada por las librerías usadas, ya que estas originalmente son usadas para el idioma inglés y tienen ciertas adaptaciones para el español.
- En cuarto lugar, se hizo la investigación de librerías con las que poder realizar análisis de sentimiento.

## Instalaciones necesarias 📝
La mayoría de instalaciones para hacer uso del código de este repositorio están dadas en los cuadernos jupyter.
Para hacer uso del corpus builder se requiere la instalación de las librerías BeautifulSoup, Selenium, nltk y sklearn.
Se debe contar con el chromedriver.exe, el cual está incluído en el repositorio.

## Autores ✒️
* **Manuel Humberto Velarde Flores** - [ManuelVelarde2212](https://github.com/ManuelVelarde2212)
* **Mileydy Ninantay Diaz** - [mile1107](https://github.com/mile1107)
* **Bladimir Huaraya Chara** - [bladhl](https://github.com/bladhl)
