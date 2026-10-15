#!/usr/bin/env python3
"""Ask a Rhizome MCP server whether it answers and offers sign-in.

    probe.py https://api.get-rhizome.app/mcp

Sends one MCP `ping` without any credentials and prints the HTTP status, and
whether the server named its sign-in metadata (`resource_metadata` in
`WWW-Authenticate`). Reads nothing and changes nothing; the only address it
contacts is the one given.

    status: 401
    sign-in offered: yes
"""

import json
import ssl
import sys
import urllib.error
import urllib.request

TIMEOUT = 10
CERTIFICATES = (
    'This Python has no CA certificates, so it trusts no HTTPS server. With '
    'Python from python.org on macOS, run "Install Certificates.command" in '
    'its folder under /Applications, or use /usr/bin/python3.'
)


def probe(address: str) -> tuple[str, bool]:
    """Send the ping and read the answer's status and sign-in header.

    :param address: The server's `/mcp` address.
    :return: The HTTP status, `000` when nothing answered, or `certificates`
        when this Python cannot check any HTTPS certificate; and whether the
        answer offers sign-in.
    """
    try:
        request = urllib.request.Request(
            address,
            method='POST',
            data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'ping'}).encode(),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/event-stream',
            },
        )
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return str(response.status), False
    except urllib.error.HTTPError as error:
        challenge = error.headers.get('WWW-Authenticate', '')
        return str(error.code), 'resource_metadata' in challenge
    except urllib.error.URLError as error:
        if isinstance(error.reason, ssl.SSLCertVerificationError):
            print(CERTIFICATES, file=sys.stderr)
            return 'certificates', False
        print(f'no answer: {error}', file=sys.stderr)
        return '000', False
    except (TimeoutError, ValueError) as error:
        print(f'no answer: {error}', file=sys.stderr)
        return '000', False


def main() -> None:
    """Probe the address given on the command line and print the result."""
    if len(sys.argv) != 2:
        sys.exit('usage: probe.py <the server address, ending in /mcp>')
    status, offered = probe(sys.argv[1])
    print(f'status: {status}')
    print(f'sign-in offered: {"yes" if offered else "no"}')


if __name__ == '__main__':
    main()
