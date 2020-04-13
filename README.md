# Deferred Type

This plugin adds a new [lektor](https://www.getlektor.com/) field type, `deferred`.
This determination of the actual type implementation of the field value is deferred
until template evaluation time.

A motivating use case is to support having a “body” field whose formatting can
be switch between, e.g., `markdown`, and `html` (or some other formatted type,
such as [rst](https://pypi.org/project/lektor-rst/).)

## How the final type is determined

If the field as a `deferred_type` option set, that value is evaluated and the
result is interpreted as the name of the final type for the field.

If no `deferred_type` option is set for the field, then we look for
a field on the current record whose name is name of the current field
with “`_type`” appended.

## Examples

### Simple Example

Here is an example model file for a simple page, with a selectable body format.

    # page.ini

    [model]
    name = Page
    label = {{ this.title }}

    [fields.title]
    label = Title
    type = string

    [fields.body]
    label = Body
    type = deferred

    [fields.body_type]
    label = Body Type
    type = select
    choices = markdown, html, text
    default = markdown


Here, the value of the `body_type` field on a particular page will
determine whether the `body` field is interpreted being `markdown`,
`html` or `text`.

### Contrived Example

Here is a contrived example showing the use of the `deferred_type` option:

    # page.ini

    [model]
    name = Page
    label = {{ this.title }}

    [fields.title]
    label = Title
    type = string

    [fields.body]
    label = Body
    type = deferred
    deferred_type = 'html' if this.body.lstrip().startswith('<') else 'markdown'

In this case, the `body` field will be interpreted as raw HTML if the
content of that field starts with a “`<`”, otherwise it will be
interpreted as _Markdown_ text.
