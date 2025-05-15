import logging
from pyrogram import Client
from config.config import API_ID, API_HASH, BOT_TOKEN

# Configure logging
logger = logging.getLogger(__name__)

class BotClient:
    """
    A class for managing the Pyrogram bot client.
    """

    _instance = None

    def __new__(cls):
        """
        Singleton pattern to ensure only one bot client instance.
        """
        if cls._instance is None:
            cls._instance = super(BotClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initialize the bot client.
        """
        if self._initialized:
            return

        self._initialized = True
        self.client = None

        # Validate required configuration
        if not all([API_ID, API_HASH, BOT_TOKEN]):
            logger.error("Missing required configuration: API_ID, API_HASH, or BOT_TOKEN")
            raise ValueError("Missing required configuration: API_ID, API_HASH, or BOT_TOKEN")

    def create_client(self):
        """
        Create the Pyrogram client.

        Returns:
            Client: Pyrogram client instance
        """
        if self.client is None:
            logger.info("Creating bot client with plugins from 'bot.plugins'")
            self.client = Client(
                "m3u8_downloader_bot",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=BOT_TOKEN,
                workers=8,
                plugins={"root": "bot.plugins"}
            )
            logger.info("Bot client created successfully")

            # Log the available plugins
            import os
            import importlib
            plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
            logger.info(f"Plugins directory: {plugins_dir}")
            if os.path.exists(plugins_dir):
                plugin_files = [f for f in os.listdir(plugins_dir)
                               if f.endswith('.py') and not f.startswith('__')]
                logger.info(f"Found plugin files: {plugin_files}")

                # Try to import each plugin to verify it's loadable
                for plugin_file in plugin_files:
                    plugin_name = plugin_file[:-3]  # Remove .py extension
                    try:
                        importlib.import_module(f"bot.plugins.{plugin_name}")
                        logger.info(f"Successfully imported plugin: {plugin_name}")
                    except Exception as e:
                        logger.error(f"Error importing plugin {plugin_name}: {str(e)}")
            else:
                logger.warning(f"Plugins directory not found: {plugins_dir}")

        return self.client

    def get_client(self):
        """
        Get the Pyrogram client instance.

        Returns:
            Client: Pyrogram client instance
        """
        if self.client is None:
            return self.create_client()
        return self.client

    async def start(self):
        """
        Start the bot client.
        """
        if self.client is None:
            self.create_client()

        await self.client.start()
        logger.info("Bot started")

        # Get bot information
        bot_info = await self.client.get_me()
        logger.info(f"Bot started as @{bot_info.username} ({bot_info.id})")

        return bot_info

    async def stop(self):
        """
        Stop the bot client.
        """
        if self.client is not None:
            await self.client.stop()
            logger.info("Bot stopped")
            self.client = None
