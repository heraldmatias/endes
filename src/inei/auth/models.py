# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from inei.auth import CommaSeparatedStrField

__author__ = 'holivares'
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)


def validate_edad(value):
    if value < 18:
        raise ValidationError('Su edad debe ser mayor a 18')


def validate_meses(value):
    if value > 11:
        raise ValidationError('Los meses deben ser menores a 12')


def validate_anos(value):
    if value > 60:
        raise ValidationError(u'Los años deben ser menores a 60')


class Region(models.Model):
    codigo = models.CharField(max_length=2, primary_key=True, db_index=True)
    descripcion = models.CharField(max_length=40, db_index=True)


class Odei(models.Model):
    region = models.ForeignKey(Region)
    provincia = models.CharField(max_length=2, db_index=True)
    descripcion = models.CharField(max_length=70)
    odei = models.CharField(max_length=70, db_index=True)

    class Meta:
        unique_together = ('region', 'provincia')

    def __unicode__(self):
        return u'%s' % self.odei


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


class Usuario(models.Model):
    username = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = True
    nombres = models.CharField(max_length=70, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=30, null=True, blank=True)
    apellido_materno = models.CharField(max_length=30, null=True, blank=True)
    instruccion = models.ForeignKey(Instruccion, null=True, blank=True)
    profesion = models.CharField(max_length=3, null=True, blank=True)
    edad = models.IntegerField(max_length=2, validators=[validate_edad],
                               null=True, blank=True)
    civil = models.ForeignKey(EstadoCivil, null=True, blank=True )
    hijos = models.IntegerField(max_length=2, null=True, blank=True)
    edades = models.CommaSeparatedIntegerField(max_length=100, null=True, blank=True)
    vive = models.IntegerField(null=True, blank=True)
    vive_otro = models.CharField(max_length=30, null=True, blank=True)
    puesto = models.ForeignKey(Puesto, null=True, blank=True)
    proyecto = models.CharField(max_length=100, null=True, blank=True)
    anos_experiencia = models.IntegerField(u'Años de experiencia laboral',
                                           null=True, blank=True, validators=[validate_anos])
    meses_experiencia = models.IntegerField(u'Meses de experiencia laboral',
                                            null=True, blank=True, validators=[validate_meses])
    experiencia_inei = models.IntegerField(null=True, blank=True)
    eproyectos_inei = models.CharField(max_length=500, null=True, blank=True)
    einei = models.BooleanField(default=False)
    anos_einei = models.IntegerField(null=True, blank=True, validators=[validate_anos])
    meses_einei = models.IntegerField(null=True, blank=True, validators=[validate_meses])
    eotro = models.BooleanField(default=False)
    institucion_eotro = models.CharField(max_length=100, null=True, blank=True)
    anos_eotro = models.IntegerField(null=True, blank=True, validators=[validate_anos])
    meses_eotro = models.IntegerField(null=True, blank=True, validators=[validate_meses])
    odei = models.ForeignKey(Odei, verbose_name=u'Region',
                             null=True, blank=True)
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
        # The user is identified by their username address
        return u'%s %s %s' % (self.nombres, self.apellido_paterno, self.apellido_materno)

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


