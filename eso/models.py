from django.db import models


class TextPresentation(models.Model):
    credentials = models.TextField()

    def __str__(self):
        return "Apresentação"


class TextPresentationParagrapth(models.Model):
    paragraph = models.TextField()

    def __str__(self):
        return "Parágrafo - " + str(self.paragraph)


class TextPresentationSpecialization(models.Model):
    specialization = models.TextField()

    def __str__(self):
        return "Especialização - " + str(self.specialization)


class Opinion(models.Model):
    author = models.TextField(max_length=40)
    post = models.TextField(max_length=300)
    date = models.DateField()
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        presentation_text = "Opinião" + (" (Válida) - " if self.is_valid else " - ") + str(self.post)
        return presentation_text


class OsteopathyAbout(models.Model):
    text_where = models.TextField()
    image_where = models.ImageField(upload_to="eso/static/eso/media/image_about_where")
    text_who = models.TextField()
    image_who = models.ImageField(upload_to="eso/static/eso/media/image_about_who")

    def __str__(self):
        return "Sobre"


class OsteopathyAdvantages(models.Model):
    text = models.TextField()

    def __str__(self):
        return "Vantagem - " + str(self.text)


class OsteopathyCase(models.Model):
    title = models.TextField(max_length=40)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return "Caso - " + str(self.title)


class OsteopathyHistory(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to="eso/static/eso/media/image_history")
    quote_image = models.TextField()

    def __str__(self):
        return "História"


# class Appointment(models.Model):
#     duration_min = models.IntegerField(default=60)
#     name = models.TextField()
#     phone = models.TextField()
#     email = models.TextField()
#     date = models.DateField()
#     time = models.TimeField()
#     description = models.TextField()


class AppointmentsDescription(models.Model):
    text = models.TextField()

    def __str__(self):
        return "Descrição Marcações"


class AccountInformation(models.Model):
    google_account_email = models.EmailField()
    google_account_password = models.TextField()
    email_to = models.EmailField()

    def __str__(self):
        return "Informação Contas"


class PediatricOstepathy(models.Model):
    top_text = models.TextField()
    bottom_text = models.TextField()

    def __str__(self):
        return "Osteopatia Pediátrica"


class PediatricOstepathyReasons(models.Model):
    reason = models.TextField()

    def __str__(self):
        return "Razão Osteopatia Pediátrica - " + str(self.reason)
