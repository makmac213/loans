from django.db import models


class Question(models.Model):
    TYPE_PLAIN_TEXT = 1             # expects text as answer
    TYPE_BOOLEAN = 2                # answerable by true or false
    TYPE_SELECT = 3                 # question must have a list of options
    TYPE_MULTIPLE_SELECT = 4        # question must have a list of options
    TYPE_FILE = 5                   # answerable by uploading a file
    TYPE_TEXT_FIELD = 6             # Textfield
    TYPE_IMAGE = 7                      # image field
    TYPE_CHOICES = (
            (TYPE_PLAIN_TEXT, 'Plain text'),
            (TYPE_BOOLEAN, 'Boolean'),
            (TYPE_SELECT, 'Select'),
            (TYPE_MULTIPLE_SELECT, 'Multiple Select'),
            (TYPE_FILE, 'File'),
            (TYPE_TEXT_FIELD, 'Textarea'),
            (TYPE_IMAGE, 'Image'),
        )

    text = models.TextField()       # required
    question_type = models.IntegerField(default=TYPE_PLAIN_TEXT, 
                                            choices=TYPE_CHOICES)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField (default=False)
    is_deleted = models.BooleanField(default=False)
    is_sensitive = models.BooleanField(default=False)
    is_ignored = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'questions_questions'

    def __unicode__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices")
    content = models.TextField()
    is_answer = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'questions_choices'
