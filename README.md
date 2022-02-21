# Huelsse Vertretungsplan Bot

english: _Huelsse substitution plan bot_

This is a bot to collect data about the substitution plan of the <a href="https://cms.sachsen.schule/huelsse/home">
Julius Ambrosius Hülße Gymnasium</a>.

The bot transforms a table from a <a href="https://github.com/SoWieMarkus/HuelsseVertretungsplanBot/blob/main/examples/Di-2022-02-01.pdf">PDF</a> into a JSON object:

```json
{
  "id": "Mo-2022-02-28",
  "year": 2022,
  "month": 2,
  "day": 28,
  "timestamp": 1646006400,
  "weekday": "Mo",
  "substitutions": [
    {
      "id": "Mo-2022-02-28_0",
      "lesson": "1",
      "course": "VGB",
      "subject": "VERT",
      "teacher": "",
      "room": "",
      "info": "Testzentrum - Vorraum Aula (Schüleraufenthaltsraum)"
    },
    ...
  ]
}
```

## Used technologies

- <a href="https://github.com/tabulapdf/tabula-java">Tabula</a>: to convert PDF document to CSV

## Setup

### Install required pip packages

```pip install -r requirements.txt```

The bot isn't useful for others to use directly. If you want to use to get data for your own API edit the POST-request
in the ```main``` function.

