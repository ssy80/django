from elem import Elem, Text
from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                      Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)


class Page:
    ALLOWED = (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
               Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text)

    def __init__(self, elem):
        if not isinstance(elem, Elem):
            raise TypeError("Page needs an instance of a class inheriting "
                            "from Elem")
        self.elem = elem

    def is_valid(self):
        return self.__is_valid_node(self.elem)

    def __is_valid_node(self, node):
        """Check this node, then every node below it."""
        if type(node) not in self.ALLOWED:
            return False
        if type(node) == Text:
            return True
        if not self.__follows_rule(node):
            return False
        return all(self.__is_valid_node(child) for child in node.content)

    def __follows_rule(self, node):
        """Check the rule for this node's direct children."""
        kind = type(node)
        #print("-",kind)
        types = [type(child) for child in node.content]
        #print(types)

        if kind == Html:
            return types == [Head, Body]
        if kind == Head:
            return types == [Title]
        if kind in (Body, Div):
            return set(types) <= {H1, H2, Div, Table, Ul, Ol, Span, Text}
        if kind in (Title, H1, H2, Li, Th, Td):
            return types == [Text]
        if kind == P:
            return set(types) <= {Text}
        if kind == Span:
            return set(types) <= {Text, P}
        if kind in (Ul, Ol):
            return set(types) == {Li}
        if kind == Tr:
            return set(types) in ({Th}, {Td})
        if kind == Table:
            return set(types) == {Tr}
        return True

    def __str__(self):
        if type(self.elem) == Html:
            return "<!DOCTYPE html>\n" + str(self.elem)
        return str(self.elem)

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(str(self) + "\n")


# tests

def valid_html():
    return Html([
        Head(Title(Text("Hello ground!"))),
        Body([
            H1(Text("Oh no, not again!")),
            Div([
                H2(Text("A list")),
                Ul([Li(Text("one")), Li(Text("two"))]),
                Span([Text("in a span"), P(Text("a paragraph"))]),
            ]),
            Table([
                Tr([Th(Text("name")), Th(Text("age"))]),
                Tr([Td(Text("Mark")), Td(Text("20"))]),
            ]),
            Ol(Li(Text("first"))),
        ]),
    ])


def check(description, elem, expected):
    result = Page(elem).is_valid()
    assert result == expected, f"{description}: got {result}"
    print(f"  {'valid  ' if result else 'invalid'} : {description}")


def test_valid():
    print("Valid pages:")
    check("full page using every rule", valid_html(), True)
    check("Div as root", Div(Text("hi")), True)
    check("empty Body and Div are allowed",
          Html([Head(Title(Text("t"))), Body(Div())]), True)


def test_invalid():
    class Strong(Elem):
        def __init__(self, content=None):
            super().__init__("strong", {}, content)

    head = Head(Title(Text("t")))
    print("Invalid pages:")
    # node types
    check("unknown tag <strong>", Div(Strong()), False)
    check("unknown tag deep in the tree",
          Html([Head(Title(Text("t"))), Body(Div(Div(Strong())))]), False)
    # Html
    check("Html with Body before Head",
          Html([Body(), Head(Title(Text("t")))]), False)
    check("Html without Body", Html(head), False)
    # Head
    check("Head without Title", Html([Head(), Body()]), False)
    check("Head with two Titles",
          Html([Head([Title(Text("a")), Title(Text("b"))]), Body()]), False)
    # Body / Div
    check("Img directly in Body",
          Html([Head(Title(Text("t"))), Body(Img())]), False)
    check("P directly in Div", Div(P(Text("x"))), False)
    # exactly one Text
    check("H1 with no Text", Div(H1()), False)
    check("H2 with two Texts", Div(H2([Text("a"), Text("b")])), False)
    check("Li containing a Span", Ul(Li(Span(Text("x")))), False)
    # P
    check("P containing a Span", Span(P(Span(Text("x")))), False)
    # Span
    check("Span containing a Div", Div(Span(Div())), False)
    # Ul / Ol
    check("empty Ul", Div(Ul()), False)
    check("Ol containing a P", Div(Ol([Li(Text("x")), P(Text("y"))])), False)
    # Tr
    check("empty Tr", Table(Tr()), False)
    check("Tr mixing Th and Td",
          Table(Tr([Th(Text("a")), Td(Text("b"))])), False)
    # Table
    check("empty Table", Div(Table()), False)
    check("Table containing a Td", Div(Table(Td(Text("x")))), False)


def test_doctype():
    assert str(Page(valid_html())).startswith("<!DOCTYPE html>\n<html>")
    assert not str(Page(Div(Text("hi")))).startswith("<!DOCTYPE")
    assert str(Page(Div(Text("hi")))) == "<div>\n  hi\n</div>"
    print("Doctype only when root is Html : OK.")


def test_write_to_file():
    filename = "test_page.html"
    page = Page(valid_html())
    page.write_to_file(filename)
    with open(filename) as f:
        assert f.read() == str(page) + "\n"
    print("write_to_file : OK.")


def test_not_an_elem():
    try:
        Page("not an element")
        raise Exception("incorrect behaviour")
    except TypeError:
        print("Page refuses a non-Elem : OK.")


def main():
    test_valid()
    test_invalid()
    test_doctype()
    test_write_to_file()
    test_not_an_elem()
    print("Tests succeeded!")
    print()
    print(Page(valid_html()))


if __name__ == "__main__":
    main()
