from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        # В form.cleaned_data будет словарь с данными
        # каждой отдельной формы, которые вы можете проверить
        for form in self.forms:
            if form.cleaned_data['is_main']:
                count += 1

        # вызовом исключения ValidationError можно указать админке о наличие ошибки
        # таким образом объект не будет сохранен,
        # а пользователю выведется соответствующее сообщение об ошибке
        # raise ValidationError('Тут всегда ошибка')

        if count == 0:
            raise ValidationError('Не указан основной раздел (тэг)')
        elif count > 1:
            raise ValidationError('Должен быть только один основной раздел (тэг)')



        return super().clean()  # вызываем базовый код переопределяемого метода



class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'published_at']


@admin.register((Tag))
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']



