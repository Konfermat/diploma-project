from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Lesson, LessonPart, Text, Test, TestOption, UserTestAnswer

# Регистрируем кастомного пользователя, чтобы видеть дату его создания
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'created_at')
    # Добавляем наше поле пройденных уроков в интерфейс админки
    filter_horizontal = ('completed_lessons',)


# --- ИНЛАЙНЫ ДЛЯ СВЯЗАННЫХ ТАБЛИЦ ---

# Позволяет добавлять варианты ответов прямо внутри теста
class TestOptionInline(admin.TabularInline):
    model = TestOption
    extra = 3  # Количество пустых строк для новых ответов по умолчанию
    ordering = ['order']

# Позволяет добавлять тексты прямо внутри части урока
class TextInline(admin.StackedInline): # StackedLayout удобнее для больших полей TextField
    model = Text
    extra = 1
    ordering = ['order']

# Позволяет добавлять тесты прямо внутри части урока
class TestInline(admin.TabularInline):
    model = Test
    extra = 1
    ordering = ['order']


# --- РЕГИСТРАЦИЯ ОСНОВНЫХ МОДЕЛЕЙ ---

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title',)


@admin.register(LessonPart)
class LessonPartAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'order')
    list_filter = ('lesson',)
    ordering = ['lesson', 'order']
    # Включаем тексты и тесты прямо на страницу редактирования Части урока!
    inlines = [TextInline, TestInline]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('question', 'lesson_part', 'order')
    # Включаем варианты ответов на страницу редактирования самого Теста
    inlines = [TestOptionInline]


# Регистрируем историю ответов только для просмотра (read-only)
@admin.register(UserTestAnswer)
class UserTestAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'is_correct', 'created_at')
    readonly_fields = ('user', 'test', 'chosen_option', 'is_correct', 'created_at')
