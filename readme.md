
| Library Used | Description  |
| ------ | ------ |
|Python 3.8.5 | Python main programming language |
| Django==2.2.17 | Used Django LTS for as web framework in project|
| pandas | Used pandas for processing data. |
| djangorestframework==3.12.2 | Django restframework for REST API. |
| plotly | Creating visual graph based in data. |
| MySQL | Database back-end. |

Installation
This Application required django. 
Run application using below command.
```sh
python manage.py runserver 

```
Apply fixures before running application. 
```
python manage.py loaddata  api/fixtures/seed_countries.json
```
## API Documentation 


- API Can be accessible by Swagger Open API 
- {host}/swagger/
- Authentication Header Token <Token genreated by signup API>

rabbitmq  
- [rabbitmq] - HTML enhanced for web apps.
- [celery] - Bacground taks

    [rabbitmq]: <https://www.rabbitmq.com/download.html>
    [celery]:<https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html>