Периодически натыкаясь на https://iknow.jp/content/japanese я наконец подумал, может есть способ как-то эти **открытые данные** превратить в колоду для Анки, чтобы побыстрее запомнить часто встречающиеся слова? В итоге, как это часто бывает, я сделал всё сам.   

Представляю вашему вниманию скрипт для скачивания этих данных и превращения их в cloze type карточки. Я решил, что удобнее оставить их разделение по тысяче, но при помощи несложных телодвижений, можно их объединить любым способом.

## Первичное разделение пользователей

### Для совсем ленивых

Вот ссылка на все колоды (по три варианта дизайна, об этом ниже)

https://mega.nz/#F!qH52gYrR!TBSEeXO3M2ygLbR5erRnRA

### Для средней ленивости

Для того чтобы скачать всё в первый раз и без особых модификаций нужно оставить следующие настройки в файле ```iknow_fetcher.py``` :
```
isfetched = False 
download_bool = True 
```

Таким образом будет скачаны все json файлы, будут созданы csv и xlsx файлы, а также будут скачаны медиа файлы и ресайзнуты картинки (```final_size```).   

### Для малой ленивости

На деле он позволяет стянуть любой курс с этого сайта, возможно даже без каких-либо модификаций, например эти - https://iknow.jp/user_courses    
Достаточно заменить листы ```links_1``` в файле ```iknow_fetcher.py``` и т.д. на списки соответствующих json. Для этого (для примера) https://iknow.jp/courses/566921 просто заменяется на https://iknow.jp/api/v2/goals/566921 и для каждой колоды делается лист (или оставить количество и названия листов или поменять собиратель ```all_cores```).   

Помимо прочего там могут быть другие название у элементов в json и вообще иной их набор (нужно будет изменить ```desereal``` функцию из ```tools.py``` и в ```iknow_fetcher.py``` основной цикл.

При желании можно вручную тип карточек (склонировав предварительно cloze type), список полей в ```fields.txt```, различные стили в css файлах, html передней стороны в ```card.front.html```, задней - в ```card.back.html```. 

## Работа с Anki

В случае если вы средней или малой ленивости, то для импорта каждой колоды необходимо импортировать микро-колоду с встроенным необходимым типом карточек (после её можно удалить) - ```delete_this.apkg```.   
Далее создаётся пустая колода с нужным названием, диалогом File -> Import импортируется соответствующий csv файл. Необходимо выбрать нужны тип карточки, если он сам не поставился.   

<!--
Добавить скриншоты? 

<img src="https://i.imgur.com/nGYpMqX.png" alt="alt text" width="whatever" height=200>
-->

Помимо этого следует переместить все медиа файлы из папки files в директории скрипта в папку (в случае Windows)  ```%appdata%/Anki2/"profile_name"/collection.media``` и добавить туда специальный файл ```None``` - фактически это просто изображение с одним прозрачным пикселем в формате png, необходимо дабы ничего не ломалось если у предложения нет изображения.   

Далее, если нужен конкретный дизайн - необходимо скопировать содержимое желаемого css файла, в браузере Анки выбрать любую из карточек и нажать на кнопку ```Cards…```, после вставить в среднее поле (Styling) содержимое.


Вот так выглядят карточки на десктопном Anki (Windows)
black.css   
<br>
<img src="https://i.imgur.com/4MMcKF4.png" alt="alt text" height=200>
<img src="https://i.imgur.com/qBBVwvz.png" alt="alt text" height=200>
<br>
<br>
dark.css   
<br>
<img src="https://i.imgur.com/YRTMpi1.png" alt="alt text" height=200>
<img src="https://i.imgur.com/bdaHNHD.png" alt="alt text" height=200>
<br>
<br>
light.css   
<br>
<img src="https://i.imgur.com/CbqGGnq.png" alt="alt text" height=200>
<img src="https://i.imgur.com/oX93vML.png" alt="alt text" height=200>
<br>
<br>

К сожалению, красивость в виде js-рандомного списка не особо работает на обратной стороне карточек на AnkiDroid (что не мешает им быть рабочими)

black.css   
<br>
<img src="https://i.imgur.com/nGYpMqX.png" alt="alt text" height=200>
<img src="https://i.imgur.com/A5H5I6f.png" alt="alt text" height=200>
<br>
<br>
dark.css   
<br>
<img src="https://i.imgur.com/AwFaBs1.png" alt="alt text" height=200>
<img src="https://i.imgur.com/ki4JJsb.png" alt="alt text" height=200>
<br>
<br>
light.css   
<br>
<img src="https://i.imgur.com/VAf6GLL.png" alt="alt text" height=200>
<img src="https://i.imgur.com/V4fSkE6.png" alt="alt text" height=200>
<br>
<br>
#### Модули, необходимые для работы
```
Pillow   
openpyxl   
requests   
```



