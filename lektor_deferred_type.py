# -*- coding: utf-8 -*-

import jinja2
from lektor.environment import Expression
from lektor.pluginsystem import Plugin
from lektor.types import Type


class TypeResolutionFailed(Exception):
    pass


class DeferredTypeDescriptor(object):
    def __init__(self, env, options, raw_value):
        self.env = env
        self.options = options
        self.raw_value = raw_value

    def get_type_name(self, this):
        deferred_type_expr = self.options.get('deferred_type')
        if deferred_type_expr:
            expr = Expression(this.pad.env, deferred_type_expr)
            type_name = expr.evaluate(this.pad, this, alt=this.alt)
            if jinja2.is_undefined(type_name):
                raise TypeResolutionFailed(type_name._undefined_message)
            return type_name

        field_name = self.raw_value.name
        selector_field = field_name + "_type"
        try:
            return this[selector_field]
        except KeyError:
            raise TypeResolutionFailed(
                "field %r does not exist" % selector_field)

    def get_type_impl(self, obj):
        type_name = self.get_type_name(obj)
        type_class = self.env.types.get(type_name)
        if type_class is None:
            raise TypeResolutionFailed("unknown type %r" % type_name)
        return type_class(self.env, self.options)

    def __get__(self, obj, type=None):
        try:
            type_impl = self.get_type_impl(obj)
        except TypeResolutionFailed as exc:
            return self.env.jinja_env.undefined(str(exc))

        value = type_impl.value_from_raw(self.raw_value)
        if hasattr(value, '__get__'):
            value = value.__get__(obj)
        return value


class DeferredType(Type):
    widget = 'multiline-text'

    def value_from_raw(self, raw):
        return DeferredTypeDescriptor(self.env, self.options, raw)


class DeferredTypePlugin(Plugin):
    name = "Deferred Type"
    description = "Defer determination of a field's type until evaluation time"

    def on_setup_env(self, **extra):
        self.env.types['deferred'] = DeferredType
