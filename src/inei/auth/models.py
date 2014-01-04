from inei.auth import CommaSeparatedStrField

__author__ = 'holivares'
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)


class EstadoCivil(models.Model):
    codigo = models.AutoField(primary_key=True, db_index=True)
    detalle = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' % self.detalle


class Profesion(models.Model):
    codigo = models.CharField(max_length=3, db_index=True)
    detalle = models.CharField(max_length=70)

    def __unicode__(self):
        return u'%s' % self.detalle


class Instruccion(models.Model):
    codigo = models.AutoField(primary_key=True, db_index=True)
    detalle = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % self.detalle


class Proyectos(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True, db_index=True)
    detalle = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.detalle


class Puesto(models.Model):
    codigo = models.AutoField(primary_key=True, db_index=True)
    detalle = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.detalle


class User(models.Model):
    username = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(default=timezone.now)
    proyecto = models.CharField(max_length=50)
    is_active = True
    name = models.CharField(max_length=150, null=True, blank=True)
    instruccion = models.ForeignKey(Instruccion, null=True, blank=True)
    profesion = models.CharField(max_length=3, null=True, blank=True)
    edad = models.IntegerField(max_length=2, null=True, blank=True)
    civil = models.ForeignKey(EstadoCivil, null=True, blank=True )
    hijos = models.IntegerField(max_length=2, null=True, blank=True)
    edades = models.CommaSeparatedIntegerField(max_length=100, null=True, blank=True)
    vive = models.IntegerField(null=True, blank=True)
    puesto = models.ForeignKey(Puesto, null=True, blank=True)
    proyecto = models.CharField(max_length=100, null=True, blank=True)
    texperiencia = models.IntegerField(null=True, blank=True)
    experiencia_inei = models.IntegerField(null=True, blank=True)
    eproyectos_inei = CommaSeparatedStrField(max_length=500, null=True, blank=True)
    einei = models.BooleanField(default=False)
    tiempo_einei = models.IntegerField(null=True, blank=True)
    eotro = models.BooleanField(default=False)
    tiempo_eotro = models.IntegerField(null=True, blank=True)
    odei = models.CharField(max_length=70, null=True, blank=True)
    ozei = models.CharField(max_length=70, null=True, blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return self.get_username()

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_full_name(self):
        raise NotImplementedError()

    def get_short_name(self):
        raise NotImplementedError()

    def get_full_name(self):
        # The user is identified by their username address
        return self.username

    def get_short_name(self):
        # The user is identified by their username address
        return self.username

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


