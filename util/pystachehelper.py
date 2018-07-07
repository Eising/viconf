import pystache

def pystache_template_parsekeys(template):
    # fragile, relies on pystache internals
    parsed_template = pystache.parse(template)
    keys = []
    parse_tree = parsed_template._parse_tree
    keyed_classes = ( pystache.parser._EscapeNode,
                      pystache.parser._LiteralNode,
                      pystache.parser._InvertedNode,
                      pystache.parser._SectionNode )
    for token in parse_tree:
        if isinstance(token, keyed_classes):
            keys.append(token.key)
    # return list of unique items
    # (json does not like sets)
    return list(set(keys))

def get_configurable_tags(template):
    tags = pystache_template_parsekeys(template)
    # The following tags should be filtered out
    default_tags = [
        'customer',
        'location',
        'product',
        'reference'
    ]
    # Here logic to handle inventory

    # Remove unhandled keys
    for defaulttag in default_tags:
        if defaulttag in tags:
            tags.remove(defaulttag)

    return tags
