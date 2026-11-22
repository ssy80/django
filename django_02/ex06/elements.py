from elem import Elem, Text


# double tags: <tag>content</tag>

class Html(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('html', attr, content)


class Head(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('head', attr, content)


class Body(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('body', attr, content)


class Title(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('title', attr, content)


class Table(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('table', attr, content)


class Th(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('th', attr, content)


class Tr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('tr', attr, content)


class Td(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('td', attr, content)


class Ul(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('ul', attr, content)


class Ol(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('ol', attr, content)


class Li(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('li', attr, content)


class H1(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('h1', attr, content)


class H2(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('h2', attr, content)


class P(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('p', attr, content)


class Div(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('div', attr, content)


class Span(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('span', attr, content)


#simple tags: <tag />

class Meta(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('meta', attr, content, 'simple')


class Img(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('img', attr, content, 'simple')


class Hr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('hr', attr, content, 'simple')


class Br(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('br', attr, content, 'simple')


# tests

def test_subject_example():
    assert str(Html([Head(), Body()])) == \
        '<html>\n  <head></head>\n  <body></body>\n</html>'
    print('Subject example : OK.')


def test_inheritance():
    for cls in (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br):
        assert issubclass(cls, Elem)
        assert isinstance(cls(), Elem)
    print('All classes inherit from Elem : OK.')


def test_double_tags():
    for cls, tag in ((Html, 'html'), (Head, 'head'), (Body, 'body'),
                     (Title, 'title'), (Table, 'table'), (Th, 'th'),
                     (Tr, 'tr'), (Td, 'td'), (Ul, 'ul'), (Ol, 'ol'),
                     (Li, 'li'), (H1, 'h1'), (H2, 'h2'), (P, 'p'),
                     (Div, 'div'), (Span, 'span')):
        assert str(cls()) == f'<{tag}></{tag}>'
    print('Double tags : OK.')


def test_simple_tags():
    for cls, tag in ((Meta, 'meta'), (Img, 'img'), (Hr, 'hr'), (Br, 'br')):
        assert str(cls()) == f'<{tag} />'
    print('Simple tags : OK.')


def test_attributes():
    assert str(Img(attr={'src': 'cat.jpg', 'alt': 'cat'})) == \
        '<img alt="cat" src="cat.jpg" />'
    assert str(Meta(attr={'charset': 'utf-8'})) == '<meta charset="utf-8" />'
    assert str(Div(Text('hi'), {'class': 'box'})) == \
        '<div class="box">\n  hi\n</div>'
    print('Attributes : OK.')


def test_content():
    # Text content (escaped by Text)
    assert str(P(Text('a < b'))) == '<p>\n  a &lt; b\n</p>'
    #assert str(P(Text('a < b'))) == '<p>\n  a < b\n</p>'   
    # List content
    assert str(Ul([Li(Text('one')), Li(Text('two'))])) == \
        '<ul>\n  <li>\n    one\n  </li>\n  <li>\n    two\n  </li>\n</ul>'
    # add_content() is inherited
    table = Table()
    table.add_content(Tr([Th(Text('name')), Th(Text('age'))]))
    table.add_content(Tr([Td(Text('Mark')), Td(Text('20'))]))
    assert str(table).count('<tr>') == 2
    assert str(table).count('<td>') == 2
    # Mixing classes: Span and Br inside an H2, Hr inside a Div
    assert str(H2([Span(Text('x')), Br()])) == \
        '<h2>\n  <span>\n    x\n  </span>\n  <br />\n</h2>'
    assert str(Div(Hr())) == '<div>\n  <hr />\n</div>'
    print('Content and nesting : OK.')


def test_errors():
    for bad in (1, 'plain str', [Text('ok'), 1]):
        try:
            P(bad)
            raise Exception('incorrect behaviour')
        except Exception as e:
            assert isinstance(e, Elem.ValidationError)
    try:
        Div().add_content('plain str')
        raise Exception('incorrect behaviour')
    except Exception as e:
        assert isinstance(e, Elem.ValidationError)
    print('Error cases : OK.')


def page():
    """The structure from the previous exercise, with the new classes."""
    return Html([
        Head(Title(Text('"Hello ground!"'))),
        Body([
            H1(Text('"Oh no, not again!"')),
            Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'}),
        ]),
    ])


def main():
    test_subject_example()
    test_inheritance()
    test_double_tags()
    test_simple_tags()
    test_attributes()
    test_content()
    test_errors()
    print('Tests succeeded!')
    print()
    print(page())


if __name__ == '__main__':
    main()
