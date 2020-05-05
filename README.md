# Lektor Polymorphic Type

This plugin adds a new polymorphic [lektor][] field type, `polymorphic`.
The determination of the actual type implementation of the field value
is deferred until evaluation time.

A motivating use case is to support having a “body” field whose
formatting can be switched between, e.g., `markdown`, and `html` (or
some other formatted type, such as [reStructuredText][rst].)

[lektor]: <https://www.getlektor.com/> "Lektor Static Content Management System"
[rst]: <https://pypi.org/project/lektor-rst/> "The lektor-rst plugin"

## Installation

Add lektor-polymorphic-type to your project from command line:

```
lektor plugins add lektor-polymorphic-type
```

See [the Lektor plugin documentation][plugins] for more information.

[plugins]: <https://www.getlektor.com/docs/plugins/>

## How It Works

If the field has a `polymorphic_type` option set, that value is evaluated
and the result is interpreted as the name of the final type for the
field.

If no `polymorphic_type` option is set for the field, then we look for a
field on the current record whose name is name of the current field
with “`_type`” appended.

## Examples

### Simple Example

Here is an example model file for a simple page, with a selectable body format:

```ini
# page.ini

[model]
name = Page
label = {{ this.title }}

[fields.title]
label = Title
type = string

[fields.body]
label = Body
type = polymorphic

[fields.body_type]
label = Body Type
type = select
choices = markdown, html, text
default = markdown
```

Here, the value of the `body_type` field on a particular page will
determine whether the `body` field is interpreted as being `markdown`,
`html` or `text`.

### Contrived Example

Here is a contrived example showing the use of the `polymorphic_type` option:

```ini
# page.ini

[model]
name = Page
label = {{ this.title }}

[fields.title]
label = Title
type = string

[fields.body]
label = Body
type = polymorphic
polymorphic_type = 'html' if this.body.lstrip().startswith('<') else 'markdown'
```

In this case, the `body` field will be interpreted as raw HTML if the
content of that field starts with a “`<`”, otherwise it will be
interpreted as _Markdown_ text.


## Author

Jeff Dairiki <dairiki@dairiki.org>
