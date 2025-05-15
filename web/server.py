import os
import logging
import asyncio
import jinja2
import aiohttp
import markdown
import datetime
from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware
from typing import Dict, Any, Optional, Callable, List

from config.config import (
    WEB_SERVER_HOST, WEB_SERVER_PORT,
    WEB_AUTH_ENABLED, WEB_AUTH_USERNAME, WEB_AUTH_PASSWORD,
    SECRET_KEY
)
from utils.system_monitor import get_all_stats

# Configure logging
logger = logging.getLogger(__name__)

# Setup Jinja2 templates
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
os.makedirs(templates_dir, exist_ok=True)
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates_dir),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)

# Add custom functions
jinja_env.globals['now'] = datetime.datetime.now

class WebServer:
    """
    A class for managing the web server.
    """

    _instance = None

    def __new__(cls):
        """
        Singleton pattern to ensure only one web server instance.
        """
        if cls._instance is None:
            cls._instance = super(WebServer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initialize the web server.
        """
        if self._initialized:
            return

        self._initialized = True
        self.app = None
        self.runner = None
        self.site = None

        # Documentation sections
        self.docs_sections = [
            {
                'id': 'overview',
                'title': 'Overview',
                'url': '/docs/overview',
                'description': 'Introduction to the M3U8 Downloader Bot',
                'file': 'overview.md'
            },
            {
                'id': 'installation',
                'title': 'Installation Guide',
                'url': '/docs/installation',
                'description': 'Complete installation instructions for all platforms',
                'file': 'installation.md'
            },
            {
                'id': 'configuration',
                'title': 'Configuration Guide',
                'url': '/docs/configuration',
                'description': 'Configuration options and settings',
                'file': 'configuration.md'
            },
            {
                'id': 'usage',
                'title': 'Usage Guide',
                'url': '/docs/usage',
                'description': 'Detailed usage instructions with examples',
                'file': 'usage.md'
            },
            {
                'id': 'features',
                'title': 'Features',
                'url': '/docs/features',
                'description': 'In-depth explanation of all features',
                'file': 'features.md'
            },
            {
                'id': 'troubleshooting',
                'title': 'Troubleshooting Guide',
                'url': '/docs/troubleshooting',
                'description': 'Solutions for common issues',
                'file': 'troubleshooting.md'
            },
            {
                'id': 'api',
                'title': 'API Documentation',
                'url': '/docs/api',
                'description': 'API documentation for programmatic integration',
                'file': 'api.md'
            },
            {
                'id': 'security',
                'title': 'Security Guide',
                'url': '/docs/security',
                'description': 'Security features and best practices',
                'file': 'security.md'
            },
            {
                'id': 'docker',
                'title': 'Docker Guide',
                'url': '/docs/docker',
                'description': 'Running the bot with Docker',
                'file': 'docker.md'
            },
            {
                'id': 'cross-platform',
                'title': 'Cross-Platform Guide',
                'url': '/docs/cross-platform',
                'description': 'Cross-platform compatibility information',
                'file': 'cross-platform.md'
            },
            {
                'id': 'scalability',
                'title': 'Scalability Guide',
                'url': '/docs/scalability',
                'description': 'Scalability features and performance optimization',
                'file': 'scalability.md'
            }
        ]

    @web.middleware
    async def security_headers_middleware(self, request, handler):
        """
        Middleware to add security headers to all responses.

        Args:
            request: Web request
            handler: Request handler

        Returns:
            Response with security headers
        """
        response = await handler(request)

        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'

        return response

    async def setup_routes(self):
        """
        Setup the web server routes with authentication and security.
        """
        middlewares = [self.security_headers_middleware]

        # Setup authentication if enabled
        if WEB_AUTH_ENABLED:
            # Create basic auth middleware
            auth = BasicAuthMiddleware(
                username=WEB_AUTH_USERNAME,
                password=WEB_AUTH_PASSWORD,
                realm='M3U8 Downloader Dashboard'
            )
            middlewares.append(auth)
            logger.info(f"Web authentication enabled with username: {WEB_AUTH_USERNAME}")

        # Create application with middlewares
        self.app = web.Application(middlewares=middlewares)

        # Add routes
        self.app.router.add_get('/', self.index_handler)
        self.app.router.add_get('/api/stats', self.stats_api_handler)

        # Add documentation routes
        self.app.router.add_get('/docs', self.docs_index_handler)

        # Add routes for each documentation section
        for section in self.docs_sections:
            self.app.router.add_get(section['url'], self.docs_section_handler)

        # Add static files route
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        os.makedirs(static_dir, exist_ok=True)
        self.app.router.add_static('/static', static_dir)

    async def index_handler(self, request):
        """
        Handle requests to the root path.

        Args:
            request: Web request

        Returns:
            Response: HTML response
        """
        try:
            # Get all stats
            stats = get_all_stats()

            # Render template
            template = jinja_env.get_template('index.html')
            html_content = template.render(stats=stats)

            return web.Response(text=html_content, content_type='text/html')
        except Exception as e:
            logger.error(f"Error handling index request: {str(e)}")
            return web.Response(text=f"Error: {str(e)}", status=500)

    async def stats_api_handler(self, request):
        """
        Handle requests to the stats API.

        Args:
            request: Web request

        Returns:
            Response: JSON response
        """
        try:
            # Get all stats
            stats = get_all_stats()

            return web.json_response(stats)
        except Exception as e:
            logger.error(f"Error handling stats API request: {str(e)}")
            return web.json_response({'error': str(e)}, status=500)

    async def start(self):
        """
        Start the web server with security features.
        """
        try:
            await self.setup_routes()

            # Configure the runner with access logging
            self.runner = web.AppRunner(
                self.app,
                access_log=logging.getLogger('aiohttp.access'),
                access_log_format='%a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i" %Tf'
            )
            await self.runner.setup()

            # Start the site
            self.site = web.TCPSite(self.runner, WEB_SERVER_HOST, WEB_SERVER_PORT)
            await self.site.start()

            # Log startup information
            auth_status = "with authentication" if WEB_AUTH_ENABLED else "without authentication"
            logger.info(f"Web server started at http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT} {auth_status}")

            if WEB_AUTH_ENABLED:
                logger.info(f"Web dashboard credentials - Username: {WEB_AUTH_USERNAME}, Password: {'*' * len(WEB_AUTH_PASSWORD)}")

                # Print admin access information
                from config.config import ADMIN_USER_IDS
                if ADMIN_USER_IDS:
                    logger.info(f"Admin users can access the dashboard URL via the /help command")

            # Log documentation information
            logger.info(f"Documentation available at http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}/docs")
            logger.info(f"Documentation sections: {', '.join(section['title'] for section in self.docs_sections)}")
        except Exception as e:
            logger.error(f"Error starting web server: {str(e)}")

    async def docs_index_handler(self, request):
        """
        Handle requests to the documentation index.

        Args:
            request: Web request

        Returns:
            Response: HTML response
        """
        try:
            # Render template
            template = jinja_env.get_template('docs_index.html')
            html_content = template.render(sections=self.docs_sections)

            return web.Response(text=html_content, content_type='text/html')
        except Exception as e:
            logger.error(f"Error handling docs index request: {str(e)}")
            return web.Response(text=f"Error: {str(e)}", status=500)

    async def docs_section_handler(self, request):
        """
        Handle requests to documentation sections.

        Args:
            request: Web request

        Returns:
            Response: HTML response
        """
        try:
            # Get the section ID from the URL
            path = request.path
            section_id = path.split('/')[-1]

            # Find the section
            section = None
            for s in self.docs_sections:
                if s['id'] == section_id:
                    section = s
                    break

            if not section:
                return web.Response(text="Section not found", status=404)

            # Get the next and previous sections for navigation
            current_index = self.docs_sections.index(section)
            prev_page = self.docs_sections[current_index - 1] if current_index > 0 else None
            next_page = self.docs_sections[current_index + 1] if current_index < len(self.docs_sections) - 1 else None

            # Read the markdown file
            docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
            os.makedirs(docs_dir, exist_ok=True)
            file_path = os.path.join(docs_dir, section['file'])

            if not os.path.exists(file_path):
                logger.error(f"Documentation file not found: {file_path}")
                return web.Response(text=f"Documentation file not found: {section['file']}", status=404)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Convert markdown to HTML
            try:
                html_content = markdown.markdown(
                    content,
                    extensions=['tables', 'fenced_code']
                )
            except ImportError as e:
                logger.warning(f"Markdown extension not available: {str(e)}. Using basic markdown conversion.")
                html_content = markdown.markdown(content)

            # Custom filters are already added at initialization time

            # Render template
            template = jinja_env.get_template('docs.html')
            rendered_html = template.render(
                title=section['title'],
                content=html_content,
                prev_page=prev_page,
                next_page=next_page
            )

            return web.Response(text=rendered_html, content_type='text/html')
        except Exception as e:
            logger.error(f"Error handling docs section request: {str(e)}")
            return web.Response(text=f"Error: {str(e)}", status=500)

    async def stop(self):
        """
        Stop the web server.
        """
        if self.site:
            await self.site.stop()
            logger.info("Web server site stopped")

        if self.runner:
            await self.runner.cleanup()
            logger.info("Web server runner cleaned up")

        self.app = None
        self.runner = None
        self.site = None
        logger.info("Web server stopped")
