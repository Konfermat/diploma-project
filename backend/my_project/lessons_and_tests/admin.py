from django.contrib import admin
from django.db.models import Max
from .models import Lesson, LessonPart, Text, Test, TestOption

class LessonPartInline(admin.TabularInline):
    model = LessonPart
    extra = 1
    # Скроем поле из редактирования, чтобы оно не путало в интерфейсе
    exclude = ['order'] 

class TextInline(admin.TabularInline):
    model = Text
    extra = 1
    exclude = ['order']

class TestInline(admin.TabularInline):
    model = Test
    extra = 1
    exclude = ['order']

class TestOptionInline(admin.TabularInline):
    model = TestOption
    extra = 1
    exclude = ['order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonPartInline]

    def save_formset(self, request, form, formset, change):
        # Проверяем, что сохраняются именно части урока
        if formset.model == LessonPart:
            # Получаем текущий максимальный order для этого урока в базе данных
            max_order = LessonPart.objects.filter(lesson=form.instance).aggregate(Max('order'))['order__max'] or 0
            
            # Перебираем все формы в инлайне
            instances = formset.save(commit=False)
            for instance in instances:
                # Если у объекта еще нет id (он новый) и не проставлен order
                if not instance.pk:
                    max_order += 1
                    instance.order = max_order
                instance.save()
            formset.save_m2m()
        else:
            super().save_formset(request, form, formset, change)


@admin.register(LessonPart)
class LessonPartAdmin(admin.ModelAdmin):
    inlines = [TextInline, TestInline]

    def save_formset(self, request, form, formset, change):
        # Автонумерация для текстов внутри части урока
        if formset.model == Text:
            max_order = Text.objects.filter(lesson_part=form.instance).aggregate(Max('order'))['order__max'] or 0
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    max_order += 1
                    instance.order = max_order
                instance.save()
            formset.save_m2m()

        # Автонумерация для тестов внутри части урока
        elif formset.model == Test:
            max_order = Test.objects.filter(lesson_part=form.instance).aggregate(Max('order'))['order__max'] or 0
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    max_order += 1
                    instance.order = max_order
                instance.save()
            formset.save_m2m()
        else:
            super().save_formset(request, form, formset, change)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [TestOptionInline]

    def save_formset(self, request, form, formset, change):
        # Автонумерация для вариантов ответов внутри теста
        if formset.model == TestOption:
            max_order = TestOption.objects.filter(option=form.instance).aggregate(Max('order'))['order__max'] or 0
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.pk:
                    max_order += 1
                    instance.order = max_order
                instance.save()
            formset.save_m2m()
        else:
            super().save_formset(request, form, formset, change)
