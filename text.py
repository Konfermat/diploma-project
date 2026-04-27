#  (OneToOneField), 

# one to many,
# models.ForeignKey(Name, on_delete=CASADE) # Удаление вместе с потомством
# models.ForeignKey(Name, on_delete=PROTECT) # Удаление только если никто не привязан
# models.ForeignKey(Name, on_delete=SET_NULL, null=True) # Установит пустое значение
##########################################################################################

# https://docs.djangoproject.com/en/6.0/topics/db/examples/many_to_many/
# and many to many (ManyToManyField).