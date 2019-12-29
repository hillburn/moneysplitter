from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler

from handlers.main_menu_handler import render_checklists
from main import conv_cancel
from queries import checklist_queries

BASE_STATE = 0


def get_conversation_handler():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(conv_delete_checklist_init, pattern='^deletechecklist$')],
        states={
            BASE_STATE: [
                CommandHandler('delete', conv_delete_checklist_execute)
            ],
        },
        fallbacks=[CommandHandler('cancel', conv_cancel)]
    )


def conv_delete_checklist_init(update, context):
    update.callback_query.edit_message_text(text='You are about to delete the selected checklist. If you really '
                                                 'want to do this, type /delete. Otherwise, type /cancel.')

    return BASE_STATE


def conv_delete_checklist_execute(update, context):
    checklist_id = context.chat_data['checklist_id']
    checklist_queries.delete(checklist_id, update.message.chat_id)
    update.message.reply_text('Checklist deleted.')

    render_checklists(update, context)

    return ConversationHandler.END
