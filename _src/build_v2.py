"""Avibra site, third pass: one dark 'editing room' system for all three pages."""
import os

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
B = '/v2/'  # page links; static files always live in /v2/
ROBOTS = ''
V = '16'
I = f'/v2/icons.svg?v={V}'
A = '/assets'


def ic(n):
    return f'<svg aria-hidden="true"><use href="{I}#{n}"/></svg>'


TG = 'https://t.me/theavibra'
IG = 'https://www.instagram.com/theavibra/'
WA = 'https://wa.me/79332156471'
CH = 'https://t.me/avibralog'
EXT = 'target="_blank" rel="noopener"'


def words(text, start=0):
    """Headline split into word masks so the load sequence can cut them in one by one."""
    out = []
    for i, w in enumerate(text.split()):
        out.append(f'<span class="w" style="--i:{start + i}"><span>{w}</span></span>')
    return ' '.join(out)


def head(title, desc, page):
    return f'''<!doctype html>
<html lang="ru" data-page="{page}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#F3F4F6"><meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0E1115">
<meta name="color-scheme" content="light dark">
{ROBOTS}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://avibnr.github.io/assets/radar-og.jpg">
<link rel="icon" href="/v2/avibra-favicon.svg" type="image/svg+xml">
<link rel="preload" href="/v2/fonts/unbounded.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/v2/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/v2/style.css?v={V}">
<script>(function(d){{d.classList.add('js');var t;try{{t=localStorage.getItem('theme')}}catch(e){{}}d.dataset.theme=t||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');if(t)d.dataset.themeFixed='1'}})(document.documentElement)</script>
</head>
<body>
<div class="progress" aria-hidden="true"></div>
'''


def bar(cur):
    def a(href, label, key):
        if cur == key:
            return f'<a href="{href}" aria-current="page"><span class="pill"></span><span class="t">{label}</span></a>'
        return f'<a href="{href}"><span class="t">{label}</span></a>'
    return f'''<header class="bar">
  <div class="bar-in">
    <a class="logo" href="{B}" aria-label="Avibra, на главную">{ic('mark')}<span>Avibra</span></a>
    <nav class="switch" aria-label="Направления">
      {a(B + 'montazh/', 'Монтаж', 'm')}
      {a(B + 'proekty/', 'Проекты', 'p')}
    </nav>
    <button class="theme" type="button" aria-label="Сменить тему" title="Сменить тему">{ic('sun')}{ic('moon')}</button>
    <button class="bar-cta" type="button" data-write>{ic('msg')}<span>Написать</span></button>
  </div>
</header>
'''


CONTACT_LINKS = [
    (TG, 'tg', 'Telegram', '@theavibra'),
    (WA, 'wa', 'WhatsApp', '+7 933 215-64-71'),
    (IG, 'ig', 'Instagram', '@theavibra'),
    (CH, 'ch', 'Канал в Telegram', 'Работы и процесс'),
]


def contact(title, sub):
    links = '\n'.join(
        f'      <a href="{u}" {EXT}>{ic(i)}<b>{n}</b><span>{s}</span></a>' for u, i, n, s in CONTACT_LINKS)
    return f'''<section class="contact" id="contact">
  <div class="wrap">
    <h2>{title}</h2>
    <p>{sub}</p>
    <div class="links">
{links}
    </div>
  </div>
</section>
'''


def foot():
    sheet = '\n'.join(
        f'  <a href="{u}" {EXT}>{ic(i)}<b>{n}</b><span>{s}</span></a>' for u, i, n, s in CONTACT_LINKS)
    return f'''<footer class="foot">
  <div class="wrap">
    <span>Avibra, 2026</span>
    <a href="/radar/">Avibra Radar, бот с заказами для фрилансеров</a>
  </div>
</footer>

<button class="fab" type="button" data-write>{ic('msg')}Написать</button>
<div class="sheet-bg"></div>
<div class="sheet" role="dialog" aria-label="Как связаться">
  <div class="grab"></div>
  <h3>Где вам удобнее?</h3>
{sheet}
</div>

<dialog class="lb" aria-label="Просмотр видео">
  <button class="lb-x" type="button" aria-label="Закрыть">{ic('x')}</button>
  <div class="lb-box"></div>
</dialog>
<script src="/v2/main.js?v={V}" defer></script>
</body>
</html>
'''


# ---------- the editor: a phone playing the reel over a live timeline ----------
# word timings are real (whisper on reel-cafe.mp4, first 10 s); cuts sit in the pauses
SUBS = [(0.0, 1.92, 'А меню можете скинуть?'), (2.3, 3.22, 'А сколько ждать?'), (3.66, 4.58, 'А доставка есть?'),
        (4.9, 5.7, 'Знакомая ситуация'), (5.7, 7.12, 'для многих заведений,'), (7.22, 8.87, 'причём на каждое такое сообщение'),
        (8.87, 9.86, 'нужно отвечать.')]
CUTS = [0.45, 2.1, 3.45, 4.75, 7.17, 8.87]
PEAKS = [0.0, 0.0, 0.0, 0.35, 0.93, 0.73, 0.51, 0.53, 0.98, 0.94, 1.0, 0.99, 0.53, 0.5, 0.96, 0.14, 0.41, 0.54, 0.36, 0.12, 0.0, 0.0, 0.36, 0.58, 0.14, 0.56, 0.51, 0.77, 0.42, 0.97, 0.74, 0.15, 0.08, 0.0, 0.0, 0.0, 0.34, 0.66, 0.69, 0.8, 0.7, 0.49, 0.66, 0.39, 0.42, 0.12, 0.1, 0.01, 0.03, 0.25, 0.66, 0.58, 0.89, 0.61, 0.69, 0.44, 0.33, 0.67, 0.66, 0.59, 0.57, 0.6, 0.36, 0.51, 0.42, 0.48, 0.58, 0.46, 0.31, 0.48, 0.37, 0.4, 0.28, 0.45, 0.55, 0.49, 0.94, 0.9, 0.57, 0.73, 0.55, 0.68, 0.66, 0.28, 0.57, 0.44, 0.31, 0.33, 0.38, 0.38, 0.35, 0.32, 0.46, 0.44, 0.34, 0.5, 0.81, 0.54, 0.1, 0.19]
LEN = 10.0


def wave():
    bars = []
    for i, p in enumerate(PEAKS):
        h = max(0.04, p) * 18
        bars.append(f'<rect x="{i * 2 + 0.3:.1f}" y="{20 - h:.1f}" width="1.4" height="{h * 2:.1f}" rx=".7"/>')
    return f'<svg class="wave" viewBox="0 0 200 40" preserveAspectRatio="none" aria-hidden="true">{"".join(bars)}</svg>'


def editor():
    pct = lambda t: f'{t / LEN * 100:.2f}%'
    cuts = ''.join(f'<i style="left:{pct(c)}"></i>' for c in CUTS)
    subs = ''.join(
        f'<span class="sub" data-a="{a}" data-b="{b}" style="left:{pct(a)};width:{pct(b - a)}">{t}</span>' for a, b, t in SUBS)
    ticks = ''.join(f'<span style="left:{pct(s)}">00:{s:02d}</span>' for s in range(0, 10, 2))
    return f'''<div class="editor" data-len="{LEN}">
  <div class="phone">
    <video src="{A}/video/hero-loop.mp4" poster="{A}/video/hero-poster.jpg" muted loop playsinline autoplay preload="auto" aria-label="Фрагмент Reels, смонтированного в Avibra"></video>
    <span class="cap" aria-hidden="true"></span>
  </div>
  <div class="tl" aria-hidden="true">
    <div class="tl-top"><span class="rec"></span><span class="tc">00:00:00</span><span class="tl-name">reels_cafe_final.mp4</span></div>
    <div class="ruler">{ticks}</div>
    <div class="track t"><b>T</b><div class="lane">{subs}</div></div>
    <div class="track v"><b>V</b><div class="lane"><div class="film" style="background-image:url({A}/video/hero-strip.jpg)"></div>{cuts}</div></div>
    <div class="track a"><b>A</b><div class="lane">{wave()}</div></div>
    <div class="head"><span></span></div>
  </div>
</div>
'''


FAN = [('zapis-home.webp', 'Онлайн-запись', 'страница автосервиса'),
       ('qayd-home.webp', 'Qayd', 'учёт для магазина в Telegram'),
       ('sushi-menu.webp', 'Приём заказов', 'меню кафе по QR-коду'),
       ('sushi-cart.webp', 'Приём заказов', 'корзина и доставка')]


def fan():
    imgs = ''.join(
        f'<figure style="--k:{i}"><img src="{A}/{f}" alt="{n}: {d}" width="778" height="1688" loading="lazy" decoding="async"></figure>' for i, (f, n, d) in enumerate(FAN))
    return f'''<div class="fan" aria-label="Экраны моих проектов">
  <div class="fan-in">{imgs}</div>
  <p class="fan-cap"><b>{FAN[0][1]}</b><span>{FAN[0][2]}</span></p>
</div>
'''


def work(kind, src, poster, title, note, length, extra=''):
    return f'''<figure class="work {kind}"{extra}>
  <button class="work-play" type="button" data-src="{src}" data-kind="{kind}" aria-label="Смотреть со звуком: {title}">
    <img src="{poster}" alt="" loading="lazy" decoding="async">
    <span class="dur">{length}</span>
    <span class="play">{ic('play')}</span>
  </button>
  <figcaption><b>{title}</b><span>{note}</span></figcaption>
</figure>
'''


WORKS = [
    ('tall', f'{A}/video/reel-cafe.mp4', f'{A}/video/reel-poster-916.jpg', 'Reels с ведущим', 'Вырезка пауз, субтитры, анимация интерфейса', '0:40'),
    ('tall', f'{A}/video/short-cafe.mp4', f'{A}/video/short-cover.jpg', 'Реклама без съёмки', 'Моушн, 3D-телефон, текст по ритму', '0:29'),
    ('wide', f'{A}/video/guide-demo.mp4', f'{A}/video/guide-poster.jpg', 'Видеоинструкция по сайту', 'Скриншоты, курсор, зумы, английская озвучка', '0:40'),
    ('wide', f'{A}/video/neon-loop.mp4', f'{A}/video/neon-poster.jpg', 'Задник для сцены', '3D в Blender, бесшовная петля для экрана', '0:16'),
]


def works_grid(order):
    """order: indexes into WORKS, '|' starts a new row"""
    out = ['<span class="works-break"></span>' if k == '|' else work(*WORKS[k]) for k in order]
    return '<div class="works">\n' + ''.join(out) + '</div>\n'


# ---------------- pages ----------------

def home():
    h = head('Avibra: монтаж Reels, сайты и боты',
             'Монтирую Reels и короткие ролики, делаю сайты, веб-приложения и Telegram-ботов. Цена и срок до начала работы.', 'home')
    h += bar('')
    h += f'''<main>
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-text">
      <h1>{words('Монтирую ролики и делаю сайты')}</h1>
      <p class="lede">Студия Avibra. Ролики, которые досматривают до конца, и сайты, которыми пользуются настоящие люди.</p>
      <div class="tabs" role="tablist" aria-label="Что вам нужно">
        <button role="tab" id="tab-m" aria-controls="pane-m" aria-selected="true" type="button">Монтаж</button>
        <button role="tab" id="tab-p" aria-controls="pane-p" aria-selected="false" type="button" tabindex="-1">Проекты</button>
        <span class="tabs-pill" aria-hidden="true"></span>
      </div>
      <div class="pane-text" id="pane-m" role="tabpanel" aria-labelledby="tab-m">
        <p>Reels, Shorts и TikTok из сырого видео с телефона: без пауз, с субтитрами, зумами и звуком.</p>
        <div class="row"><a class="btn btn-main" href="{B}montazh/">Смотреть работы и цены</a><span class="from">от 1 000 ₽ за ролик</span></div>
      </div>
      <div class="pane-text" id="pane-p" role="tabpanel" aria-labelledby="tab-p" hidden>
        <p>Сайты, веб-приложения, Telegram-боты и Mini Apps. Мои продукты работают у реальных людей, их можно открыть.</p>
        <div class="row"><a class="btn btn-main" href="{B}proekty/">Смотреть проекты и цены</a><span class="from">лендинг от 3 500 ₽</span></div>
      </div>
    </div>
    <div class="stage" data-show="m">
      <div class="stage-m">{editor()}</div>
      <div class="stage-p">{fan()}</div>
    </div>
  </div>
</section>
{marquee(['Reels и Shorts', 'Субтитры', 'Монтаж говорящей головы', 'Реклама для кафе и салонов', 'Сайты и лендинги', 'Telegram-боты', 'Mini Apps', 'Дизайн'])}

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Последние работы</h2><a class="more" href="{B}montazh/#works">Все ролики</a></div>
    {works_grid([0, 2, 1])}
  </div>
</section>
</main>
'''
    h += contact('Есть задача?', 'Напишите пару фраз о том, что нужно. Отвечу, уточню детали и назову цену и срок до начала работы.')
    h += foot()
    return h


INSIDE = [
    ('Паузы', 'Вырезаю «эээ», дубли и долгие вдохи. Остаётся живая речь в хорошем темпе.'),
    ('Субтитры', 'Крупные и читаются без звука. Простые или с подсветкой каждого слова.'),
    ('Ритм', 'Зумы, смена планов и перебивки, чтобы глазу всегда было за что зацепиться.'),
    ('Звук', 'Чищу голос от шума и эха, выравниваю громкость, ставлю звуковые акценты.'),
    ('Графика', 'Заголовок в первые секунды, стрелки, цены, интерфейсы и 3D-телефон.'),
    ('Форматы', 'Reels, Shorts, TikTok и VK Клипы в 9:16, горизонтальные ролики в 16:9.'),
]

TIERS = [
    ('Простой', 'Говорящая голова, сторис, ролик-ответ', '1 000–1 500 ₽', 'до 60 секунд',
     ['Вырезка пауз и оговорок', 'Субтитры', 'Чистка звука', 'Обложка из кадра'], 'Заказать', False),
    ('Динамичный', 'Экспертный Reels, обзор, реклама услуги', '2 000–3 000 ₽', 'до 90 секунд',
     ['Всё из простого', 'Субтитры с подсветкой слов', 'Зумы, смена планов, ритм', 'Вставки, текст и звуки'], 'Заказать', True),
    ('С графикой', 'Реклама, презентация, моушн', 'от 4 000 ₽', 'до 3 минут',
     ['Моушн-дизайн и инфографика', 'Анимация интерфейсов и 3D', 'Ролик без съёмки из фото и скриншотов', 'Стиль под ваш бренд'], 'Обсудить', False),
]


def tiers():
    out = []
    for name, note, price, unit, items, cta, pick in TIERS:
        li = ''.join(f'<li>{x}</li>' for x in items)
        badge = '<span class="badge">Берут чаще всего</span>' if pick else ''
        out.append(f'''  <div class="tier{' pick' if pick else ''}">
    {badge}<h3>{name}</h3><p class="note">{note}</p>
    <p class="price">{price}</p><p class="unit">ролик {unit}</p>
    <ul>{li}</ul>
    <button class="btn{' btn-main' if pick else ''}" type="button" data-write>{cta}</button>
  </div>''')
    return '<div class="tiers">\n' + '\n'.join(out) + '\n</div>\n'


def marquee(items):
    # Two identical halves so the strip loops without a seam; screen readers get the list once.
    half = ''.join(f'<span>{t}</span>' for t in items)
    return f'<div class="marquee" aria-label="{", ".join(items)}"><div class="marquee-track" aria-hidden="true">{half}{half}</div></div>'


def deals(items):
    return '<div class="deals">' + ''.join(f'<p><b>{a}</b><span>{b}</span></p>' for a, b in items) + '</div>\n'


def steps(items):
    li = ''.join(f'<li><span class="when">{w}</span><b>{t}</b><p>{d}</p></li>' for w, t, d in items)
    return f'<ol class="steps">{li}</ol>\n'


def montazh():
    h = head('Монтаж Reels и коротких роликов, Avibra',
             'Монтирую Reels, Shorts и TikTok: вырезка пауз, субтитры, динамика и звук. От 1 000 ₽, готово за 1 день.', 'm')
    h += bar('m')
    inside = ''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a, b in INSIDE)
    h += f'''<main>
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-text">
      <h1>{words('Монтаж Reels, которые досматривают')}</h1>
      <p class="lede">Присылаете сырое видео с телефона, через день получаете готовый ролик: без пауз и оговорок, с субтитрами, динамикой и звуком.</p>
      <div class="row">
        <button class="btn btn-main" type="button" data-write>{ic('msg')}Прислать видео</button>
        <a class="btn" href="#price">Цены</a>
      </div>
      <p class="facts"><span>Готово за 1 день</span><span>Пробные 10 секунд бесплатно</span><span>−20% на первый ролик</span></p>
    </div>
    <div class="stage" data-show="m"><div class="stage-m">{editor()}</div></div>
  </div>
</section>
{marquee(['Reels', 'Shorts', 'TikTok', 'Субтитры', 'Вырезаю паузы и оговорки', 'Цветокоррекция', 'Обложки', 'Рекламные ролики'])}

<section class="sec" id="works">
  <div class="wrap">
    <div class="sec-head"><h2>Работы</h2><p>Нажмите на ролик, чтобы посмотреть со звуком.</p></div>
    {works_grid([0, 2, '|', 3, 1])}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Что происходит с видео</h2><p>Всё, чтобы ролик не пролистали в первые три секунды.</p></div>
    <div class="inside">{inside}</div>
  </div>
</section>

<section class="sec" id="price">
  <div class="wrap">
    <div class="sec-head"><h2>Цены</h2><p>За один ролик. Точную цену назову, когда посмотрю исходник, и она не изменится по ходу работы. Скидки не суммируются.</p></div>
    {tiers()}
    {deals([('−20%', 'на первый ролик'), ('−15%', 'на пакет от 8 роликов в месяц'), ('2 правки', 'включены, каждая следующая 300 ₽')])}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Как работаем</h2></div>
    {steps([('Сегодня', 'Присылаете видео', 'Файлы в Telegram, WhatsApp или ссылкой на диск, плюс пример того, что нравится.'),
            ('Через час', 'Цена и пробный фрагмент', 'Фиксирую стоимость. Если хотите, бесплатно смонтирую 10 секунд, чтобы вы оценили стиль.'),
            ('Завтра', 'Предоплата и ролик', 'После предоплаты 50% делаю ролик целиком. Пакет роликов по графику, который удобен вам.'),
            ('После', 'Правки и остаток', 'Две правки включены, каждая следующая 300 ₽. Остаток оплаты, когда ролик вам понравился.')])}
  </div>
</section>
</main>
'''
    h += contact('Пришлите видео', 'Даже одно сырое видео с телефона. Посмотрю, предложу, что из него можно сделать, и назову цену.')
    h += foot()
    return h


PROJECTS = [
    ('Для автосервисов и шиномонтажей', 'Онлайн-запись клиентов',
     'Клиент открывает ссылку, выбирает услугу и время и записывается сам, без звонка. Все записи у владельца в телефоне.',
     ['Страница сервиса с ценами, адресом и кнопкой звонка', 'Свободное время считается само', 'Уведомление о каждой новой записи', 'Работает в браузере, скачивать ничего не нужно'],
     '<p class="pprice">5 000 ₽ один раз<small>первая неделя бесплатно, без абонентской платы</small></p>',
     [('https://zapis-avibra.netlify.app', 'Открыть демо', True), (WA, 'Хочу такую', False)],
     ['zapis-home.webp', 'zapis-book.webp', 'zapis-admin.webp'], 'phones'),
    ('Для кафе и ресторанов', 'Приём заказов онлайн',
     'Гость открывает меню по ссылке или QR-коду, собирает заказ и выбирает доставку или самовывоз. Заказ сразу приходит заведению, а гость видит, на каком он этапе.',
     ['Меню с фото, добавками и ценами', 'Доставка, самовывоз и оплата онлайн', 'Статус заказа у гостя в реальном времени', 'Панель заведения: принять заказ, указать время, отметить готовность'], '',
     [('https://zakaz-r2g.pages.dev/sushi', 'Открыть демо', True), (WA, 'Хочу такое', False)],
     ['sushi-menu.webp', 'sushi-item.webp', 'sushi-cart.webp'], 'phones'),
    ('Telegram Mini App', 'Qayd, учёт для магазина',
     'Товары, остатки, продажи, финансы и работа команды прямо в Telegram. Каждый день работает в настоящем магазине, есть версия для браузера.',
     ['Продажи и остатки в реальном времени', 'Роли для владельца и продавцов', 'Отчёты по выручке и расходам'], '',
     [('https://qayd.space', 'Открыть Qayd', True)],
     ['qayd-home.webp'], 'phones one'),
    ('Программа для Mac и Windows', 'Wasl, два компьютера как один',
     'Одна мышь и клавиатура для Mac и Windows, общий буфер обмена, файлы и звук по домашней сети.', [], '',
     [('https://github.com/AVIBNR/wasl-releases/releases/latest', 'Скачать Wasl', False)], ['wasl-home.webp'], 'desk'),
    ('Telegram-бот', 'Avibra Radar',
     'Находит заказы для фрилансеров на биржах и в каналах и присылает их в первые минуты после публикации, пока откликов мало.', [], '',
     [('/radar/', 'Подробнее о боте', False)], ['radar-icon.jpg'], 'icon'),
]


def projects():
    out = []
    for tag, name, about, items, price, links, imgs, media in PROJECTS:
        li = ('<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>') if items else ''
        btns = ''
        if links:
            b = []
            for u, label, main in links:
                ext = EXT if u.startswith('http') else ''
                b.append(f'<a class="btn{" btn-main" if main else ""}" href="{u}" {ext}>{label}</a>')
            btns = '<div class="row">' + ''.join(b) + '</div>'
        pics = ''.join(f'<img src="{A}/{f}" alt="{name}" loading="lazy" decoding="async">' for f in imgs)
        out.append(f'''<article class="proj">
  <div class="proj-text"><p class="tag">{tag}</p><h3>{name}</h3><p class="about">{about}</p>{li}{price}{btns}</div>
  <div class="proj-media {media}">{pics}</div>
</article>''')
    return '\n'.join(out)


PRICES = [
    ('Сайты и приложения', [
        ('Исправить ошибку или доработать сайт', 'Найду причину, исправлю и проверю на телефоне и компьютере.', 'от 1 500 ₽'),
        ('Лендинг или сайт-визитка', 'Адаптивная вёрстка, форма заявки с уведомлением в Telegram, запуск на хостинге.', 'от 3 500 ₽'),
        ('Telegram-бот', 'Заявки, каталог, запись, рассылки, с панелью для вас.', 'от 3 000 ₽'),
        ('База данных и серверная часть', 'Supabase и PostgreSQL: таблицы, права доступа, функции.', 'от 2 500 ₽'),
        ('Веб-приложение или Mini App', 'Каталог, заявки, запись, личный кабинет, учёт, с вашей логикой и дизайном.', 'от 12 000 ₽'),
        ('Программа для Mac и Windows', 'Electron, сборка под обе системы и автообновление.', 'по договорённости'),
    ]),
    ('Дизайн', [
        ('Баннер, афиша или обложка', 'Для соцсетей, сайта, маркетплейса или печати, в нужных размерах.', 'от 800 ₽'),
        ('Карусель для соцсетей', 'Серия слайдов в одном стиле: структура, тексты, вёрстка.', 'от 1 500 ₽'),
        ('Логотип и фирменный стиль', 'Знак, цвета, шрифты и правила использования.', 'от 3 000 ₽'),
    ]),
]


def plist():
    out = ['<div class="plist">']
    for group, rows in PRICES:
        out.append(f'<h3>{group}</h3>')
        for a, b, p in rows:
            out.append(f'<div class="prow"><b>{a}</b><p>{b}</p><span>{p}</span></div>')
    out.append('</div>')
    return '\n'.join(out) + '\n'


def proekty():
    h = head('Сайты, веб-приложения и боты, Avibra',
             'Делаю сайты, веб-приложения, Telegram-ботов и Mini Apps. Мои проекты работают у реальных людей.', 'p')
    h += bar('p')
    h += f'''<main>
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-text">
      <h1>{words('Сайты, приложения и боты')}</h1>
      <p class="lede">От макета до запуска, проверяю сам на телефоне и компьютере. Ниже мои проекты: они работают на самом деле, их можно открыть.</p>
      <div class="row">
        <button class="btn btn-main" type="button" data-write>{ic('msg')}Обсудить задачу</button>
        <a class="btn" href="#price">Цены</a>
      </div>
      <p class="facts"><span>Сайты и лендинги</span><span>Веб-приложения</span><span>Telegram-боты</span><span>Mini Apps</span><span>Программы для ПК</span><span>Дизайн</span></p>
    </div>
    <div class="stage" data-show="p"><div class="stage-p">{fan()}</div></div>
  </div>
</section>
{marquee(['Сайты и лендинги', 'Веб-приложения', 'Telegram-боты', 'Mini Apps', 'Онлайн-запись', 'Приём заказов', 'Программы для Mac и Windows', 'Дизайн'])}

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Проекты</h2><p>Свои продукты, которыми пользуются каждый день.</p></div>
    {projects()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Дизайн</h2><p>Логотипы, баннеры и карусели для соцсетей, в одном стиле и с расчётом на телефон.</p></div>
    <div class="gal">
      <figure><img src="{A}/design/avibra-logo.webp" alt="Логотип Avibra" loading="lazy" decoding="async" width="900" height="900"><figcaption>Логотип и фирменный стиль</figcaption></figure>
      <figure><img src="{A}/design/carousel-01-oblozhka.webp" alt="Обложка карусели" loading="lazy" decoding="async" width="900" height="1125"><figcaption>Карусель, обложка</figcaption></figure>
      <figure><img src="{A}/design/carousel-06-vashe-menyu.webp" alt="Слайд карусели" loading="lazy" decoding="async" width="900" height="1125"><figcaption>Карусель, слайд</figcaption></figure>
      <figure class="wide"><img src="{A}/design/avibra-banner.webp" alt="Баннер профиля" loading="lazy" decoding="async" width="1600" height="800"><figcaption>Баннер профиля для соцсетей</figcaption></figure>
    </div>
  </div>
</section>

<section class="sec" id="price">
  <div class="wrap">
    <div class="sec-head"><h2>Цены</h2><p>Стартовые. Точную назову после короткого разговора, и она не изменится по ходу работы.</p></div>
    {plist()}
    {deals([('Демо', 'покажу, как это будет выглядеть у вас, до оплаты'), ('Фикс', 'цена и срок известны до начала работы'), ('После приёмки', 'оплата, когда вы проверили результат')])}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Как работаем</h2></div>
    {steps([('День 1', 'Вы пишете', 'Пару фраз о задаче в Telegram или WhatsApp.'),
            ('День 1', 'Цена и срок', 'Уточняю детали и фиксирую стоимость до начала работы.'),
            ('По ходу', 'Показываю результат', 'Вы видите работу до сдачи и можете поправить курс.'),
            ('Сдача', 'Запуск и оплата', 'Проверяю на телефоне и компьютере, оплата после приёмки.')])}
  </div>
</section>
</main>
'''
    h += contact('Обсудим задачу?', 'Напишите пару фраз о том, что нужно. Отвечу, уточню детали и назову цену и срок до начала работы.')
    h += foot()
    return h


# The same pages at the site root (the main address) and at /v2/ (links already sent to clients).
for B, ROOT in [('/', SITE), ('/v2/', os.path.join(SITE, 'v2'))]:
  ROBOTS = '' if B == '/' else '<link rel="canonical" href="https://avibnr.github.io/">'
  for path, fn in [('index.html', home), ('montazh/index.html', montazh), ('proekty/index.html', proekty)]:
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(fn())
print('ok')
