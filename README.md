<a href="#">
    <img src="https://raw.githubusercontent.com/paulrozhkin/handcontrol-documentation/master/img/logo.jpg" title="HandControl" alt="HandControl" width="300">
</a>

# Контроллер управления протезом руки человека

## Description

Проект содержит программное обеспечение для Raspberry Pi Zero W, реализующие логику бионического протеза руки человека.
Краткое описание функциональных возможностей:
- Исполнение жестов протеза
- Взаимодействие с внешними системами по Bluetooth (передача данных в protobuf структурах через [самописный протокол](https://github.com/paulrozhkin/handcontrol-documentation/blob/master/bluetooth_api.md))
- Обработка показаний миоэлектрических датчиков и выделение паттернов жестов. Количество распознаваемых паттернов 2.
- Передача управляющих команд для установки положения линейных двигателей по интерфейсу SPI на [контроллер линейных приводов](https://github.com/paulrozhkin/handcontrol-motor-controller)

## Linked Repositories
- [Документация](https://github.com/paulrozhkin/handcontrol-documentation)
- [Контроллер управления линейными приводами на STM32F103C8T6](https://github.com/paulrozhkin/handcontrol-motor-controller)
- [Приложение для конфигурирования протеза для ПК на WPF](https://github.com/paulrozhkin/HandControlApplication)
- [Приложение для управления протезом для Android](https://github.com/ForsaiR/HandControlAndroidAplication)
- [Схемотехника драйвера моторов (Altium Designer)](https://github.com/paulrozhkin/DCDriverShematic)
- [Схемотехника контроллера управления (Altium Designer)](https://github.com/paulrozhkin/ArmProsthesisShematic)
- [Сервер для одновременной работы с несколькими протезами по MQTT на Kotlin](https://github.com/paulrozhkin/hand-control-mqtt)
- [MQTT proxy для контроллера управления протеза для STM32F767ZITX](https://github.com/paulrozhkin/handcontrol-mqtt-proxy)

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="https://github.com/paulrozhkin" target="_blank">Paul Rozhkin</a>.
