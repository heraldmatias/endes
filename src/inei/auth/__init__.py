from django.db.models import CharField
from inei.auth import validators

__author__ = 'holivares'

# TODO: Maybe move this into contrib, because it's specialized.


class CommaSeparatedStrField(CharField):
    default_validators = [validators.validate_comma_separated_str_list]
    description = "Comma-separated integers"

    def formfield(self, **kwargs):
        defaults = {
            'error_messages': {
                'invalid': u'Ingrese los proyectos separados por comas.',
            }
        }
        defaults.update(kwargs)
        return super(CommaSeparatedStrField, self).formfield(**defaults)