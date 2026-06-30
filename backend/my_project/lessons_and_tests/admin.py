from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Lesson, LessonPart, Text, Test, TestOption, UserTestAnswer

# Регистрируем кастомного пользователя
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # ИСПРАВЛЕНО: date_joined вместо data_joined (стандартное поле Django)
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    
    # ИСПРАВЛЕНО: date_joined вместо data_joined
    readonly_fields = ('date_joined',) 
    

# --- ИНЛАЙНЫ ДЛЯ СВЯЗАННЫХ ТАБЛИЦ ---

# Позволяет добавлять варианты ответов прямо внутри теста
class TestOptionInline(admin.TabularInline):
    model = TestOption
    fk_name = 'option'  # ИСПРАВЛЕНО: Явно указываем Django, какое поле является ForeignKey к модели Test
    extra = 3  
    ordering = ['order']

# Позволяет добавлять тексты прямо внутри части урока
class TextInline(admin.StackedInline): 
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
    # ИСПРАВЛЕНО: 'created_by' вместо 'username'
    list_display = ('title', 'created_by', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title',)


@admin.register(LessonPart)
class LessonPartAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'order')
    list_filter = ('lesson',)
    ordering = ['lesson', 'order']
    inlines = [TextInline, TestInline]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('question', 'lesson_part', 'order')
    inlines = [TestOptionInline]


# Регистрируем историю ответов только для просмотра (read-only)
@admin.register(UserTestAnswer)
class UserTestAnswerAdmin(admin.ModelAdmin):
    # ИСПРАВЛЕНО: 'user' вместо 'username'
    list_display = ('user', 'test', 'is_correct', 'created_at')
    readonly_fields = ('user', 'test', 'chosen_option', 'is_correct', 'created_at')
    
    def has_add_permission(self, request):
        return False
