import logging
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

# Configure logging
logger = logging.getLogger(__name__)

@Client.on_callback_query()
async def handle_callback_queries(client: Client, callback_query: CallbackQuery):
    """
    Handle callback queries from inline buttons.
    """
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    # Handle different callback data
    if data.startswith("cancel_"):
        # Extract download ID from callback data
        download_id = data.split("_")[1]
        
        # Acknowledge the callback query
        await callback_query.answer("Processing...")
        
        # Handle cancel logic here
        await callback_query.message.edit_text(
            "❌ Download cancelled."
        )
    else:
        # Unknown callback data
        await callback_query.answer("Unknown action", show_alert=True)
