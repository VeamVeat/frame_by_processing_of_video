# frame_by_processing_of_video 

---

## Оглавление
* [Техническое задание](#общее)
* [Используемые языки и фреймворки](#используемые-языки-и-фреймворки)
* [Используемые технологии](#используемые-технологие)
* [Используемые базы данных](#используемые-базы-данных)
* [Настройка и запуск проекта](#настройка-и-запуск-проекта)

## Техническое задание
1 -> Взять два любых видео файла (на усмотрение разработчика), имеющих разный динамический FPS (variable framerate), и сохранить их на диск (руками, предварительная подготовка).

2 -> Создать RTSP сервер с GStreamer и Python для того, чтобы файлы из пункта №1 отдать на свой же локальный компьютер как стрим. Вот пример того, как это можно сделать ([тут](https://stackoverflow.com/questions/59858898/how-to-convert-a-video-on-disk-to-a-rtsp-stream)).

3 -> При получении кадров по RTSP стриму, эти кадры нужно пересобрать в новые такие же файлы и в потоке их записать на локальный MinIO.

4 -> Необходимо написать функцию, которая по прошествии определенного количества миллисекунд от начала просмотра видео, сможет сопоставить записанный файл в MinIO с оригинальным файлом. Как следствие ожидаем, что попадем практически кадр-в-кадр, с учетом динамического FPS. Результатом должно быть 2 расположенных сбоку друг от друга картинки, соответствующих кадру выбранной миллисекунды.

5 -> Необходимо написать функцию, которая сможет в двух разных видеофайлах с пункта №1 найти одинаковый момент, соответствующий указанной миллисекунде. Результатом работы такой функции должен быть лог, который покажет, сколько именно кадров в каждом файле пришлось пропустить, чтобы попасть в указанную точку на обоих видео. Функция также должна делать снэпшот обоих таких кадров, для валидации.

6 -> Реализация должна быть в Docker.

К решению должна прилагаться справка о том, какие есть механизмы оптимизации данного подхода, какие есть подводные камни при работе со стримами (исключительно из опыта), а также предложение о том, как можно реализовать параллельную запись стримов на GPU и как найти общую точку сходимости по этим кадрам, то есть, как выровнять видеопотоки (пример - есть поезд, у которого вокруг вагонов расставлены камеры, запись с которых начинается по триггеру на стороне сервера. Как сделать так, чтобы файлы имели общую точку начала записи без задержек).

Рассматриваем кандидатов, которые (исключительно из опыта) умеют работать с динамическими структурами данных, а также имеют опыт работы с удаленным администрированием, деплоем и настройкой сервисов по SSH, которые хорошо понимают сетевую часть и архитектуру веб и серверных приложений.

## Используемые языки и фреймворки
- Python 3.12
- Gstreamer 1.0

## Используемые технологии
- Opencv 4.11.0.86
- PyGObject 3.52.2
- pycairo 1.27.0
- python-dotenv 1.0.1

## Используемые базы данных
- Minio 7.0.0

## Настройка и запуск проекта
Для начала склонируйте репозиторий и установить зависимости

```Python
`git clone git@github.com:VeamVeat/frame_by_processing_of_video.git`
cd frame_by_processing_of_video
```

##  Поднимаем все необходимые сервисы
`make all`

## Результат работы

- Результат работы первой функции будет храниться в папке snapshots_video_file_comparison

![combined_frame_5000ms](https://github.com/user-attachments/assets/eaabf312-e43d-45cc-b92f-f294c6d2e3e9)

- Результат работы первой функции будет храниться в папке snapshots_search_same_moment

![combined_frame_5000ms](https://github.com/user-attachments/assets/b96c2efa-0287-4fca-afdc-bc11e46a7212)

-  Результаты работы будут сохранены в логах в папке logs
