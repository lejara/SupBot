#!/usr/bin/python
from bs4 import BeautifulSoup
from mitmproxy import ctx
import os
import sys

content_js = None

def load(l):
    l.add_option("path", str, "", "Path for bypass.js")


def configure(updated):
    if "path" in updated:
        ctx.log.info('[Bypass] Successfully added path')
        global content_js
        # load in the javascript to inject
        with open(ctx.options.path, 'r') as f:
            content_js = f.read()


def response(flow):
    # only process 200 responses of html content
    if not flow.response.status_code == 200:
        return
    BypassCSP(flow)
    if not 'text/html' in flow.response.headers['Content-Type']:
        return

    # inject the script tag
    html = BeautifulSoup(flow.response.text, 'lxml')
    container = html.head or html.body
    if container:
        script = html.new_tag('script', type='text/javascript')
        script.string = content_js
        container.insert(0, script)
        flow.response.text = str(html)

        ctx.log.info('[Bypass] Successfully injected the bypass')

def BypassCSP(flow):
    for head in flow.response.headers:
        if "content-security-policy" in head.lower():
            flow.response.headers[head] = ''
            ctx.log.info('[Bypass] CPS Successfully Removed')
