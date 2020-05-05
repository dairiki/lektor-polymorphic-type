# -*- coding: utf-8 -*-

import pytest

import jinja2
from lektor.environment import PRIMARY_ALT
from lektor.types import RawValue
from markupsafe import escape

from lektor_polymorphic_type import (
    PolymorphicTypeDescriptor,
    PolymorphicType,
    PolymorphicTypePlugin,
    TypeResolutionFailed,
    )


@pytest.fixture
def options():
    return {}


@pytest.fixture
def field_name():
    return 'myfield'


@pytest.fixture
def raw_value(field_name):
    return RawValue(field_name, 'my value')


@pytest.fixture
def model_data():
    return {
        '_alt': PRIMARY_ALT,
        'myfield_type': 'text',
        }


class TestPolymorphicTypeDescriptor(object):
    @pytest.fixture
    def desc(self, env, options, raw_value):
        return PolymorphicTypeDescriptor(env, options, raw_value)

    @pytest.mark.parametrize("options, type_name", [
        ({}, 'text'),
        ({'polymorphic_type': '"mark" ~ "down"'}, 'markdown'),
        ])
    def test_get_type_name(self, desc, page, type_name):
        assert desc.get_type_name(page) == type_name

    @pytest.mark.parametrize("options, field_name, match", [
        ({}, 'notmyfield', r"field 'notmyfield_type' does not exist"),
        ({'polymorphic_type': 'missing'}, 'myfield', r"undefined"),
        ])
    def test_get_type_name_raises(self, desc, page, match):
        with pytest.raises(TypeResolutionFailed, match=match):
            desc.get_type_name(page)

    @pytest.mark.parametrize("options", [{'polymorphic_type': '"text"'}])
    def test_get_type_impl(self, desc, page):
        type = desc.get_type_impl(page)
        assert type.name == 'text'

    @pytest.mark.parametrize("options", [{'polymorphic_type': '"badtype"'}])
    def test_get_type_impl_raises(self, desc, page):
        with pytest.raises(TypeResolutionFailed, match=r"unknown type"):
            desc.get_type_impl(page)

    @pytest.mark.parametrize("model_data", [
        {'myfield_type': 'text'},
        {'myfield_type': 'markdown'},
        ])
    @pytest.mark.usefixtures('ctx')
    def test_get(self, desc, page, model_data):
        value = desc.__get__(page)
        assert 'my value' in escape(value)

    @pytest.mark.parametrize("model_data", [
        {'myfield_type': 'badtype'},
        ])
    @pytest.mark.usefixtures('ctx')
    def test_get_returns_undefined(self, desc, page, model_data):
        value = desc.__get__(page)
        assert jinja2.is_undefined(value)


class TestPolymorphicType(object):
    @pytest.fixture
    def polymorphic_type(self, env, options):
        return PolymorphicType(env, options)

    def test_value_from_raw(self, polymorphic_type, raw_value):
        value = polymorphic_type.value_from_raw(raw_value)
        assert isinstance(value, PolymorphicTypeDescriptor)
        assert value.raw_value is raw_value


class TestPolymorphicTypePlugin(object):

    @pytest.fixture
    def plugin(self, env):
        id_ = 'polymorphic-type'
        return PolymorphicTypePlugin(env, id_)

    def test(self, plugin, env):
        plugin.on_setup_env()
        assert env.types['polymorphic'] is PolymorphicType
