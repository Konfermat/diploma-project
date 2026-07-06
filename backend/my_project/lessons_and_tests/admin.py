from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import Max
from .models import User, Lesson, LessonPart, Text, Test, TestOption, UserTestAnswer

# ==========================================
# 1. ВАЛИДАЦИЯ (ПРОВЕРКА НА ПРАВИЛЬНЫЙ ОТВЕТ)
# ==========================================

class TestOptionInlineFormSet(BaseInlineFormSet):
    """Проверяет, чтобы у теста был выбран СТРОГО ОДИН правильный вариант."""
    def clean(self):
        super().clean()
        
        correct_answers_count = 0
        has_any_options = False

        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE', False):
                continue
            
            has_any_options = True
            if form.cleaned_data.get('is_correct'):
                correct_answers_count += 1

        if has_any_options:
            if correct_answers_count == 0:
                raise ValidationError(
                    "Ошибка: У теста должен быть как минимум один правильный ответ! "
                    "Пожалуйста, отметьте галочкой 'Is correct' один вариант."
                )
            elif correct_answers_count > 1:
                raise ValidationError(
                    f"Ошибка: У теста может быть только ОДИН правильный ответ! "
                    f"Вы отметили {correct_answers_count}. Пожалуйста, оставьте только одну галочку."
                )


# ==========================================
# 2. ИНЛАЙНЫ (ВЛОЖЕННЫЕ ФОРМЫ)
# ==========================================

class TestOptionInline(admin.TabularInline):
    model = TestOption
    formset = TestOptionInlineFormSet
    extra = 3  
    ordering = ['order']


class TextInline(admin.StackedInline): 
    model = Text
    extra = 1
    ordering = ['order']


class TestInline(admin.TabularInline):
    model = Test
    extra = 1
    ordering = ['order']


# ==========================================
# 3. НАСТРОЙКА ОСНОВНЫХ СТРАНИЦ АДМИНКИ
# ==========================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    readonly_fields = ('date_joined',) 


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title',)
    list_select_related = ('created_by',)


@admin.register(LessonPart)
class LessonPartAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'order')
    list_filter = ('lesson',)
    ordering = ['lesson', 'order']
    inlines = [TextInline, TestInline]
    list_select_related = ('lesson',)

    def save_formset(self, request, form, formset, change):
        """Автоматически заполняет order для Text и Test внутри LessonPart"""
        instances = formset.save(commit=False)
        
        # Обрабатываем добавление Текстов
        if formset.model == Text:
            # Ищем максимальный order для текущей части урока
            max_order = Text.objects.filter(lesson_part=form.instance).aggregate(Max('order'))['order__max'] or 0
            for instance in instances:
                if not instance.pk and (instance.order == 0 or instance.order == 1): 
                    # Если запись новая и order равен дефолтному значению, инкрементируем
                    max_order += 1
                    instance.order = max_order
                instance.save()
                
        # Обрабатываем добавление Тестов
        elif formset.model == Test:
            max_order = Test.objects.filter(lesson_part=form.instance).aggregate(Max('order'))['order__max'] or 0
            for instance in instances:
                if not instance.pk and (instance.order == 0 or instance.order == 1):
                    max_order += 1
                    instance.order = max_order
                instance.save()
                
        else:
            formset.save()
        
        formset.save_m2m()


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('question', 'lesson_part', 'order')
    inlines = [TestOptionInline]
    list_select_related = ('lesson_part',)

    def save_formset(self, request, form, formset, change):
        """Автоматически заполняет order для TestOption внутри Test"""
        instances = formset.save(commit=False)
        if formset.model == TestOption:
            max_order = TestOption.objects.filter(option=form.instance).aggregate(Max('order'))['order__max'] or 0
            for instance in instances:
                if not instance.pk and (instance.order == 0 or instance.order == 1):
                    max_order += 1
                    instance.order = max_order
                instance.save()
        else:
            formset.save()
        formset.save_m2m()


@admin.register(UserTestAnswer)
class UserTestAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'is_correct', 'created_at')
    readonly_fields = ('user', 'test', 'chosen_option', 'is_correct', 'created_at')
    list_select_related = ('user', 'test', 'chosen_option')
    
    def has_add_permission(self, request):
        return False
