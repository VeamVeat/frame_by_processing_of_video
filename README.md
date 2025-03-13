# frame_by_processing_of_video 

---

## Оглавление
* [Техническое задание](#общее)
* [Используемые языки и фреймворки](#используемые-языки-и-фреймворки)
* [Используемые технологии](#используемые-технологие)
* [Используемые базы данных](#используемые-базы-данных)
* [Настройка и запуск проекта](#настройка-и-запуск-проекта)

## Техническое задание
- Взять два любых видео файла (на усмотрение разработчика), имеющих разный динамический FPS (variable framerate), и сохранить их на диск (руками, предварительная подготовка).
Создать RTSP сервер с GStreamer и Python для того, чтобы файлы из пункта №1 отдать на свой же локальный компьютер как стрим. Вот пример того, как это можно сделать (тут).
При получении кадров по RTSP стриму, эти кадры нужно пересобрать в новые такие же файлы и в потоке их записать на локальный MinIO.
Необходимо написать функцию, которая по прошествии определенного количества миллисекунд от начала просмотра видео, сможет сопоставить записанный файл в MinIO с оригинальным файлом. Как следствие ожидаем, что попадем практически кадр-в-кадр, с учетом динамического FPS. Результатом должно быть 2 расположенных сбоку друг от друга картинки, соответствующих кадру выбранной миллисекунды.
Необходимо написать функцию, которая сможет в двух разных видеофайлах с пункта №1 найти одинаковый момент, соответствующий указанной миллисекунде. Результатом работы такой функции должен быть лог, который покажет, сколько именно кадров в каждом файле пришлось пропустить, чтобы попасть в указанную точку на обоих видео. Функция также должна делать снэпшот обоих таких кадров, для валидации.
Реализация должна быть в Docker. К решению должна прилагаться справка о том, какие есть механизмы оптимизации данного подхода, какие есть подводные камни при работе со стримами (исключительно из опыта), а также предложение о том, как можно реализовать параллельную запись стримов на GPU и как найти общую точку сходимости по этим кадрам, то есть, как выровнять видеопотоки (пример - есть поезд, у которого вокруг вагонов расставлены камеры, запись с которых начинается по триггеру на стороне сервера. Как сделать так, чтобы файлы имели общую точку начала записи без задержек).
Рассматриваем кандидатов, которые (исключительно из опыта) умеют работать с динамическими структурами данных, а также имеют опыт работы с удаленным администрированием, деплоем и настройкой сервисов по SSH, которые хорошо понимают сетевую часть и архитектуру веб и серверных приложений.

## Используемые языки и фреймворки
- Python 3.12

## Используемые технологии
- Opencv Python 4.11.0.86

## Используемые базы данных
- Minio 7.1.14

## Настройка и запуск проекта
Для начала склонируйте репозиторий и установить зависимости

`https://github.com/VeamVeat/frame_by_processing_of_video.git`

## данной командой поднимутся все необходимые ресурсы
`make all`

- Результат работы первой функции будет храниться в папке snapshots_video_file_comparison
![20250307140023_1 jpg](https://github.com/user-attachments/assets/02e8f999-1b29-47df-8999-96bb42796e8f)

- Результат работы первой функции будет храниться в папке snapshots_search_same_moment
![20250307140157_1 jpg](https://github.com/user-attachments/assets/117c4290-c0b9-405e-b9f5-768c045b6d94)

-  Результаты работы будут сохранены в логах в папке logs
