
Keyseq
==========

Описание
--------

Проект `keyseq` предназначен для замены последовательностей клавиш на основе заданных правил. Он поддерживает платформы с графическими интерфейсами Wayland и Xorg.

Запуск
------

### Аргументы

* `--yaml_path`: путь к YAML файлу с последовательностями клавиш.
* `--delay`: задержка между нажатиями клавиш для эмуляции ввода человеком.
* `--device_name`: имя устройства ввода.

### Пример использования

Создайте скрипты для запуска и остановки `keyseq`.

#### start_keyseq.sh

```bash

# Путь к исполняемому файлу

EXECUTABLE=""

# Аргументы
YAML_PATH=""
DELAY=0.05
DEVICE_NAME="AT Translated Set 2 keyboard"

# Файл для хранения PID
PID_FILE="/tmp/keyseq_pid"

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "Скрипт уже запущен с PID $PID."
            exit 1
        else
            echo "PID файл существует, но процесс не работает. Удаляю старый PID файл."
            rm "$PID_FILE"
        fi
    fi

    echo "Запуск скрипта в фоне..."
    "$EXECUTABLE" --yaml_path "$YAML_PATH" --delay "$DELAY" --device_name "$DEVICE_NAME" &
    echo $! > "$PID_FILE"
    echo "Скрипт запущен с PID $(cat $PID_FILE)"
}

start

#### stop_keyseq.sh

# Файл для хранения PID

PID\_FILE="/tmp/keyseq\_pid"

stop() {
    if \[ -f "$PID_FILE" \]; then
        PID=$(cat "$PID_FILE")
        echo "Остановка скрипта с PID $PID..."
        kill "$PID"
        rm "$PID_FILE"
        echo "Скрипт остановлен."
    else
        echo "PID файл не найден. Скрипт, возможно, не запущен."
    fi
}

stop

```

Пример конфигурации

```yaml

# YAML файл для замены последовательностей клавиш
replacements:
  # Замена 
  - keys: ["1", "l", "1"]
    replace: "YAML"  


  # Замена на многострочный текст
  - keys: ["1", "p", "1"]
    replace: |
      it is work
      it is work
      it is work
      it is work
      

  # Общая замена для последовательностей
  - keys: 
      - ["s", "_", "r"]
      - ["s", "-, "r"]
    replace: "shared replacement"



```

------

Обнаружение устройства ввода evdev
----------------------------------

Для обнаружения устройства ввода evdev выполните следующие шаги:

1. Запустите команду: `sudo evtest`
2. Выберите нужное устройство из списка.
3. Запомните путь к устройству, который выглядит как `/dev/input/eventX`, где X - номер устройства.

Пример:

$ sudo evtest
No device specified, trying to scan all of /dev/input/event\*
Available devices:
/dev/input/event0:    Power Button
/dev/input/event1:    Power Button
/dev/input/event2:    AT Translated Set 2 keyboard
/dev/input/event3:    Logitech USB Optical Mouse
Select the device event number \[0-3\]:
