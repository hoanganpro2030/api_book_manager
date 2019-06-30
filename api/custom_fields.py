import re

from datetime import datetime
from flask_restplus.fields import Raw, Nested, List


EMAIL_REGEX = re.compile(r'\S+@\S+\.\S+')
PHONE_REGEX = re.compile(r'[0-9]{10}')
ISBN_REGEX = re.compile(r"^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|"
                        r"(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|"
                        r"(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$")


class CustomField(Raw):
    """
    Custom Field base class with validate feature
    """
    __schema_type__ = 'string'

    def __init__(self, *args, **kwargs):
        super(CustomField, self).__init__(**kwargs)
        # custom params
        self.positive = kwargs.get('positive', True)

    def format(self, value):
        """
        format the text in database for output
        works only for GET requests
        """
        if not self.validate(value):
            print('Validation of field with value \"%s\" (%s) failed' % (
                value, str(self.__class__.__name__)))
            # raise MarshallingError
            # disabling for development purposes as the server crashes when
            # exception is raised. can be enabled when the project is mature
        if self.__schema_type__ == 'string':
            return str(value)
        else:
            return value

    def validate_empty(self):
        """
        Return when value is empty or null
        """
        if self.required:
            return False
        else:
            return True

    def validate(self, value):
        """
        Validate the value. return True if valid
        """
        pass


class Email(CustomField):
    """
    Email field
    """
    __schema_format__ = 'email'
    __schema_example__ = 'email@domain.com'

    def validate(self, value):
        if not value:
            return self.validate_empty()
        if not EMAIL_REGEX.match(value):
            return False
        return True


class Phone(CustomField):
    """
    Phone field
    """
    __schema_example__ = '0986797221'

    def __init__(self, *args, **kwargs):
        self.min_length = kwargs.pop('min_length', None)
        self.max_length = kwargs.pop('max_length', None)
        self.pattern = kwargs.pop('pattern', None)
        super(Phone, self).__init__(*args, **kwargs)

    def validate(self, value):
        if not value:
            return self.validate_empty()
        if not PHONE_REGEX.match(value):
            return False
        if (len(value) < self.min_length) or (len(value) > self.max_length):
            return False
        return True


class Isbn(CustomField):
    """
    Phone field
    """
    __schema_example__ = '978-604-0-00000-2'

    def __init__(self, *args, **kwargs):
        self.min_length = kwargs.pop('min_length', None)
        self.max_length = kwargs.pop('max_length', None)
        self.pattern = kwargs.pop('pattern', None)
        super(Isbn, self).__init__(*args, **kwargs)

    def validate(self, value):
        if not value:
            return self.validate_empty()
        if not ISBN_REGEX.match(value):
            return False
        if (len(value) < self.min_length) or (len(value) > self.max_length):
            return False
        return True