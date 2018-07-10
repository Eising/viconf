import pystache
import copy
import re
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
        'reference',
        'node',
        '_link_hostname',
        '_link_ipv4',
        '_link_ipv6'
    ]
    # Here logic to handle inventory

    # Remove unhandled keys
    for defaulttag in default_tags:
        if defaulttag in tags:
            tags.remove(defaulttag)

    return tags

class PystacheHelpers:
    FORM_TAGS =  [
        'customer',
        'location',
        'product',
        'reference'
    ]

    LINK_TAGS = [
        '_link_hostname',
        '_link_ipv4',
        '_link_ipv6'
    ]

    def parse_template_tags(self, template):
        result = {
            'form_tags': set(),
            'link_tags': set(),
            'inventory_tags': set()
        }
        tags = pystache_template_parsekeys(template)
        result['all_tags'] = list(tags)
        for tag in self.FORM_TAGS:
            if tag in tags:
                result['form_tags'].add(tag)
        for tag in self.LINK_TAGS:
            if tag in tags:
                result['link_tags'].add(tag)

        res = re.compile(r'^_i_(.+)$')
        for tag in tags:
            match = res.match(tag)
            if match is not None:
                result['inventory_tags'].add(tuple(match.group(1).split("__")))

        result['user_tags'] = tags

        return result
