# Andika API

## Hacks

1. Show folder tree windows: **Tree /A**
2. Out put folder tree in a txt file `tree /a > TREE-Output.txt``

## Database records that must be seeded include

- Tones
- UseCases
- UseCase Categories

If You Add New use Cases, Tones or UseCase Categories you must update the following file:

[Update Tone List File](./app/api/utilities/tones_list.py)
[Update UseCase List File](./app/usecases/data.py)
Then you must also update the fixture file.

## Running the application

```shell
    python manage.py runserver --settings=core.settings.dev
    python manage.py makemigrations --settings=core.settings.dev
    python manage.py migrate --settings=core.settings.dev
```
