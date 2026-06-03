# TODO удали неправильный lorem 
# python manage.py shell

Course.objects.all().delete()  # Удалит все старые курсы перед созданием новых

from api.models import Course

# Находим курс по названию и обновляем его описание
Course.objects.filter(title='Поколение Python').update(
    description='Ваш новый правильный текст описания курса.'
)
