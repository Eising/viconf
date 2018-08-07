import re


class ViconfValidators:
    VALIDATORS = {
        'none': {'description': 'No validation',
                 'type': 'novalidation'},
        'string': {
            'description': "Basic String Validation",
            'css_class': 'validatestring',
            'type': 'regex',
            'regex': '^\S+$',
            'error': 'Invalid string'
        },
        'asn': {'css_class': 'validateasn',
                'description': 'Validates AS-numbers',
                'end': 4294967296,
                'start': 1,
                'type': 'range'},
        'bundle': {'css_class': 'validatexrbundle',
                   'description': 'Validates IOS-XR Bundle '
                   'range',
                   'end': 65535,
                   'start': 1,
                   'type': 'range'},
        'cidrv4': {'css_class': 'validatecidrv4',
                   'description': 'Validates IPv4 CIDR '
                   'prefixes',
                   'error': 'Invalid IPv4 Prefix',
                   'regex':
                   '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/[0-9]+$',
                   'type': 'regex'},
        'digits': {'css_class': 'validatedigits',
                   'description': 'Validates numbers',
                   'error': 'Must be numbers only',
                   'regex': '^[0-9]+$',
                   'type': 'regex'},
        'ioxif': {'css_class': 'validatesxriface',
                  'description': 'Validates IOS-XR Interface',
                  'regex': '^(GigabitEthernet|TenGigE|HundredGigE)([0-9+]\/)+([0-9])$',
                  'type': 'regex'},
        'ipv4': {'css_class': 'validateipv4',
                 'description': 'Validates IPv4 addresses',
                 'error': 'Invalid IPv4 Address',
                 'regex': '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                 'type': 'regex'},
        'ipv6': {'css_class': 'validateipv6',
                 'description': 'Validates IPv6 addresses',
                 'error': 'Invalid IPv6 address',
                 'regex': '^([A-f0-9:]+:+)+[A-f0-9]+$',
                 'type': 'regex'},
        'cidrv6': {'css_class': 'validatecidr6',
                   'description': 'Validates IPv6 addresses with /prefix',
                   'error': 'Invalid IPv6 address',
                   'regex': '^([A-f0-9:]+:+)+[A-f0-9]+\/[0-9]+$',
                   'type': 'regex'},

        'vlan': {'css_class': 'validatevlan',
                 'description': 'Validates Vlan',
                 'end': 4094,
                 'start': 1,
                 'type': 'range'}
    }

    def validate(self, validator, tester):
        if validator not in self.VALIDATORS:
            raise "Unknown validator"
        validator = self.VALIDATORS[validator]
        if validator['type'] == 'regex':
            regex = re.compile(validator['regex'])
            if regex.match(tester):
                return True
            else:
                return False
        elif validator['type'] == 'range':
            number = int(tester)
            ran = range(validator['start'], validator['end'])
            if number in ran:
                return True
            else:
                return False
        else:
            return True
