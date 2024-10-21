from django.db import models


class Picture(models.Model):
    title = models.CharField(verbose_name="Название картины", max_length=255, null=True)
    public_date = models.DateField(
        verbose_name="Дата публикации картины",null=True,auto_now_add=True
    )

    AVAILABILITY_CHOICES = [
        (True, "В наличии"),
        (False, "Нет в наличии"),
    ]
    IS_ORIGINAL_CHOICES = [
        (True, "Оригинал"),
        (False, "Копия"),
    ]
    availability = models.BooleanField(
        default=True, verbose_name="Наличие", choices=AVAILABILITY_CHOICES
    )
    is_original = models.BooleanField(
        verbose_name="Оригинал", choices=IS_ORIGINAL_CHOICES
    )
    history = models.CharField(
        verbose_name="История картины", max_length=1024, blank=True
    )
    price = models.DecimalField (
        verbose_name="Стоимость", max_digits=12, decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    cover_picture = models. ImageField(verbose_name="Картина", upload_to="", unique=True,null=True)
    category = models.ForeignKey(
        "Category",
        verbose_name="Жанр",
        blank=True,
        null=True,
        related_name="Categories",
        on_delete=models.SET_NULL,
    )
    author = models.ForeignKey(
        "Painter",
        verbose_name="Автор",
        blank=True,
        null=True,
        related_name="pictures",
        on_delete=models.SET_NULL,
    )
    style = models.ManyToManyField(
        "Style",
        verbose_name="Стиль",
        blank=True,
        related_name="Styles",
    )

    class Meta:
        verbose_name = "Картина"
        verbose_name_plural = "Картины"
        ordering = ["-title"]

    def __str__(self):
        return f"{self.title}"


class Painter(models.Model):
    last_name = models.CharField(verbose_name="Фамилия", max_length=255)
    first_name = models.CharField(verbose_name="Имя", max_length=255)
    patronymic = models.CharField(verbose_name="Отчество", max_length=255, blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["-first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"


class Biography(models.Model):
    painter = models.OneToOneField(
        Painter,
        verbose_name="Painter",
        blank=True,
        null=True,
        related_name="biography",
        on_delete=models.SET_NULL,
    )
    biography_text = models.TextField(
        verbose_name="Текст биографии", blank=True, unique=True
    )
    contact_info = models.CharField(
        verbose_name="Контактная информация",
        max_length=255,
        blank=True,
    )
    painter_picture = models.ImageField(
        verbose_name="Фотография автора", upload_to="", blank=True,null=True
    )

    class Meta:
        verbose_name = "Биография"
        verbose_name_plural = "Биографии"
        ordering = ["-biography_text"]

    def __str__(self):
        return self.biography_text


class Style(models.Model):
    style_name = models.CharField(verbose_name="Стиль", max_length=255)
    style_description = models.CharField(
        verbose_name="Описание стиля", max_length=255, blank=True
    )

    class Meta:
        verbose_name = "Стиль"
        verbose_name_plural = "Стили"
        ordering = ["-style_name"]

    def __str__(self):
        return self.style_name


class Category(models.Model):
    category_name = models.CharField(
        verbose_name="Категория",
        max_length=255,
        unique=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"
        ordering = ["-category_name"]

    def __str__(self):
        return self.category_name
