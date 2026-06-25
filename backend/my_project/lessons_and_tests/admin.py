from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Lesson, LessonPart, Text, Test, TestOption, UserTestAnswer

# Регистрируем кастомного пользователя
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'created_at')
    
    # ИСПРАВЛЕНО: Так как создано через auto_now_add, это поле должно быть read-only
    readonly_fields = ('created_at',) 
    
    # Добавляем поле пройденных уроков в интерфейс админки
    filter_horizontal = ('completed_lessons',)
    
    # ИСПРАВЛЕНО: Внедряем кастомные поля в стандартную структуру UserAdmin
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('completed_lessons', 'created_at')
        }),
    )
    
    # ИСПРАВЛЕНО: Добавляем поля в форму создания нового пользователя, если это необходимо
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('completed_lessons',)
        }),
    )


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
    list_display = ('title', 'created_by', 'is_published', 'created_at')
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
    list_display = ('created_by', 'test', 'is_correct', 'created_at')
    readonly_fields = ('created_by', 'test', 'chosen_option', 'is_correct', 'created_at')
    
    # РЕКОМЕНДАЦИЯ: Запрещаем создавать записи вручную через админку, 
    # так как это чисто лог/история действий пользователя
    def has_add_permission(self, request):
        return False
