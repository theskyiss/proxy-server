from aiohttp import web, ClientSession
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re

URL = 'https://news.ycombinator.com/'
PORT = 8232
PATTERN = re.compile(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\-\d\'\"\\]')
WORD_LENGHT = 6


async def handle(request):
    url = urljoin(URL, request.path_qs)
    async with ClientSession() as session:
        async with session.get(url) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'text' not in content_type:
                return web.Response(body=await response.read(), content_type=content_type)

            text = await response.text()

    if urlparse(url).path.endswith('.css'):
        return web.Response(text=text, content_type='text/css')
    
    soup = scan_text(text)
    return web.Response(text=str(soup), content_type='text/html')


def scan_text(text):
    soup = BeautifulSoup(text, 'lxml')
    text_nodes = soup.find_all(string=True)

    for text_node in text_nodes:
        parts = re.split(r'(\s+)', text_node)

        for i, part in enumerate(parts):
            if len(part) == WORD_LENGHT and not re.findall(PATTERN, part):
                parts[i] = f"{part}™"

        text_node.replace_with(''.join(parts))
    return soup


app = web.Application()
app.router.add_get('/{tail:.*}', handle)

web.run_app(app, port=PORT)
