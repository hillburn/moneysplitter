from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.main_menu_handler import render_main_menu_from_callback
from queries import item_queries, purchase_queries, checklist_queries


def render_item_menu(update, context):
    checklist_id = context.user_data['checklist_id']
    checklist_name = context.user_data['checklist_names'][checklist_id]
    checklist_items = item_queries.find_by_checklist(checklist_id)
    if len(checklist_items) == 0:
        text = checklist_name + ' has no items.'
    else:
        text = '*{}* contains the following items:\n{}'.format(checklist_name, '\n'.join(
            map(lambda checklist_item: checklist_item.name, checklist_items)))

    keyboard = [
        [InlineKeyboardButton('Remove items', callback_data='remove_items')],
        [InlineKeyboardButton('Back to main menu', callback_data='checklist_{}'.format(checklist_id))]
    ]

    update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard),
                                            parse_mode='Markdown')


def show_purchases(update, context):
    query = update.callback_query
    checklist_id = context.user_data['checklist_id']
    checklist_name = context.user_data['checklist_names'][checklist_id]
    purchases = purchase_queries.find_by_checklist(checklist_id)
    if len(purchases) == 0:
        text = checklist_name + ' has no purchases.'
    else:
        text = ''
        for purchase in purchases:
            text += '{} has paid {} for the following items:\n'.format(purchase.buyer.username,
                                                                       purchase.get_price()) + '\n'.join(
                map(lambda item: item.name, purchase.items)) + '\n'

    query.edit_message_text(text=text)
    render_main_menu_from_callback(update, context, True)


def refresh_checklists(update, context):
    if len(context.user_data['checklist_names']) == checklist_queries.count_checklists(
            update.callback_query.from_user.id):
        update.callback_query.answer('Nothing new to show!')
        return

    render_main_menu_from_callback(update, context, False)
    update.callback_query.answer('Main menu refreshed!')
