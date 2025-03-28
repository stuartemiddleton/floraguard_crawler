BOT_NAME = 'undercrawler'

SPIDER_MODULES = ['undercrawler.spiders']
NEWSPIDER_MODULE = 'undercrawler.spiders'

ROBOTSTXT_OBEY = False
DEPTH_LIMIT = 1
SPLASH_URL = ''

AUTOLOGIN_URL = 'http://127.0.0.1:8089'
AUTOLOGIN_ENABLED = False
CRAZY_SEARCH_ENABLED = False
FOLLOW_LINKS = True

CDR_CRAWLER = 'scrapy undercrawler'
CDR_TEAM = 'HG'

PREFER_PAGINATION = False
ADBLOCK = False
MAX_DOMAIN_SEARCH_FORMS = 10
HARD_URL_CONSTRAINT = True
AVOID_DUP_CONTENT_ENABLED = True

FILES_STORE_S3_ACL = 'public-read'
# Set FILES_STORE to enable
ITEM_PIPELINES = {
    'undercrawler.media_pipeline.UndercrawlerMediaPipeline': 1,
}

DOWNLOADER_MIDDLEWARES = {
    'maybedont.scrapy_middleware.AvoidDupContentMiddleware': 200,
    'autologin_middleware.AutologinMiddleware': 605,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'undercrawler.middleware.CookiesMiddlewareIfNoSplash': 700,
    'undercrawler.middleware.SplashAwareAutoThrottle': 722,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression'
        '.HttpCompressionMiddleware': 810,
}

DOWNLOADER_MIDDLEWARES.update({
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
})

DOWNLOADER_MIDDLEWARES.update({
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
})

ROTATING_PROXY_LIST = [
    '117.54.114.102:80',
    '159.203.61.169:3128',
    '141.95.238.126:8080',
    '18.185.52.173:20202',
    '52.201.245.219:20202',
    '13.247.58.145:20201',
    '54.84.68.213:20201',
    '13.208.183.144:20201',
    '56.155.29.90:20201',
    '34.242.114.171:20201',
    '54.180.234.231:20201',
    '13.115.194.123:20202',
]

ROTATING_PROXY_PAGE_RETRY_TIMES = 5  # Number of retries for a failed proxy
ROTATING_PROXY_BAN_POLICY = 'rotating_proxies.policy.BanDetectionPolicy'  # Default ban detection

DUPEFILTER_CLASS = 'undercrawler.dupe_filter.DupeFilter'

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# use the same user agent as autologin by default
# USER_AGENT = ('Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 '
#               '(KHTML, like Gecko) Ubuntu Chromium/43.0.2357.130 '
#               'Chrome/43.0.2357.130 Safari/537.36')

# enabled in CookiesMiddlewareIfNoSplash only when SPLASH_URL is set
COOKIES_ENABLED = True

# Run full headless-horseman scripts
RUN_HH = True

DOWNLOAD_DELAY = 0.1  # Adjusted by AutoThrottle
SPLASH_AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_MAX_DELAY = 5

# HH scripts in Splash take a while to execute, so use higher values here
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
SCHEDULER_DEBUG = True

RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 403]


TELNETCONSOLE_ENABLED = False

# Unused settings from template

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'undercrawler.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'undercrawler.pipelines.SomePipeline': 300,
#}

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
