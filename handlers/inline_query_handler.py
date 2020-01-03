from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle

from queries import checklist_queries, user_queries


def send_invite_message(update, context):
    query = update.inline_query.query

    inline_options = []
    for checklist in checklist_queries.find_by_creator(update.inline_query.from_user['id']):
        if query and not checklist.name.lower().startswith(query.lower()):
            continue

        inline_options.append(
            InlineQueryResultArticle(
                id=checklist.id,
                title=checklist.name,
                input_message_content=InputTextMessageContent(
                    'You are invited to join the checklist {}. Press the button under this message to confirm. If you '
                    'don\'t know what this means, check out @PurchaseSplitterBot for more info.'.format(checklist.name)
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('Join checklist', callback_data='join_checklist_{}'.format(checklist.id))
                ]])
            )
        )
    context.bot.answer_inline_query(update.inline_query.id, inline_options)


def accept_invite_message(update, context):
    user_id = update.callback_query.from_user.id
    if not user_queries.exists(user_id):
        update.callback_query.answer('Please start the bot before joining a checklist!')
        return

    checklist_id = update.callback_query.data.split('_')[-1]
    if checklist_queries.is_participant(checklist_id, user_id):
        update.callback_query.answer('You are a participant of that checklist already!')
        return

    checklist_queries.join(checklist_id, user_id)
    update.callback_query.answer('Successfully joined checklist!')
