from utils import database
from private import accountinfo


def format_subject(s):
    while len(s) >= 3 and s[:3].lower() == 're:':
        s = s[3:]
    while len(s) > 0 and s[0] == ' ':
        s = s[1:]
    return s


def format_subscription_list(subs, title):
    result = '##' + title + '\n'
    i = 0
    if len(subs) == 0:
        result += 'No Subscriptions'
    for sub in subs:
        i += 1
        result += sub.to_table('Subscription #' + str(i)) + '\n \n'
    return result


def compose_greeting(username):
    return "Hi " + username + ",\n\n"


def compose_salutation():
    result = SIGNATURE + "\n\t \n\t \n" + \
             "/r/Alert_Bot | " + \
             "/u/" + accountinfo.developerusername + " | " + \
             "[Bot Code](https://github.com/tylerbrockett/Alert-Bot-Reddit)\n"
    return result


def compose_subscribe_message(username, new_sub, subs, subreddit_not_specified):
    result = compose_greeting(username) + \
             "Thanks for your subscription. " + \
             "You will continue to receive updates for posts that match your new subscription. " + \
             "To unsubscribe, send me a message with the body 'unsubscribe {subscription#}'.\t \nAlternatively, " + \
             "you can reply to this message or any replies from the bot in regards to this subscription and reply " + \
             "with 'unsubscribe' as the body.\t \n" + \
             ("\t \n**Note:** If no subreddit is specified, /r/buildapcsales will be used by default\t \n" if subreddit_not_specified else "") + \
             new_sub.to_table('New Subscription') + "\t \n\t \n" + \
             format_subscription_list(subs, 'Your Subscriptions') + \
             compose_salutation()
    return result


def compose_all_subscriptions_message(username, all_subscriptions):
    result = compose_greeting(username) + \
             format_subscription_list(all_subscriptions, 'Your Subscriptions') + \
             compose_salutation()
    return result


def compose_duplicate_subscription_message(username, existing_sub, new_sub):
    result = compose_greeting(username) + \
             'We think you already have an existing subscription matching the criteria specified. Below ' + \
             'both subscriptions are listed. If you believe there has been a mistake, please PM me at ' + \
             '/u/' + accountinfo.developerusername + ' and let me know.\n\n' + \
             existing_sub.to_table('Existing Subscription') + '\n\n' + \
             new_sub.to_table('New Subscription') + '\n' + \
             compose_salutation()
    return result


def compose_help_message(username, subs):
    result = compose_greeting(username) + \
             INFORMATION + "\t \n\t \n" + format_subscription_list(subs, 'Your Subscriptions') + \
             compose_salutation()
    return result


def compose_unsubscribe_invalid_sub_message(username, subs):
    result = compose_greeting(username) + \
        "I'm sorry, but it looks like the subscription you're trying to unsubscribe from is invalid. Please " + \
        "make sure you are replying to a message that was in regards to a valid and active subscription. If you " + \
        "think you are receiving this message in error, please feel free to message /u/" + \
        accountinfo.developerusername + " to try to get this sorted out.\n\n" + \
        format_subscription_list(subs, 'Your Subscriptions') + \
        compose_salutation()
    return result


def compose_unsubscribe_message(username, removed_subs, subs):
    result = compose_greeting(username) + \
             "You have unsubscribed from the following item. Thanks for using the bot!\n\n" + \
             removed_subs[0].to_table('Unsubscribed From') + \
             '\n' + \
             format_subscription_list(subs, 'Your Subscriptions') + \
             compose_salutation()
    return result


def compose_unsubscribe_all_message(username):
    result = compose_greeting(username) + \
             "You have successfully unsubscribed from all subscriptions." + \
             compose_salutation()
    return result


def compose_unsubscribe_from_num_message(username, removed_sub, subs):
    result = compose_greeting(username) + \
        "You have successfully unsubscribed from the following item.\t \n\t \n" + \
        removed_sub.to_table('Unsubscribed From') + "\t \n\t \n" + \
        format_subscription_list(subs, 'Your Subscriptions') + \
        compose_salutation()
    return result


def compose_edit_message(username):
    result = compose_greeting(username) + \
        "Unfortunately, the bot has only partially implemented this feature, so it is not available quite " + \
        "yet. Please try again at a later date. Sorry for the inconvenience! " + \
        compose_salutation()
    return result


def compose_feedback_message(username):
    result = compose_greeting(username) + \
             "Thank you very much for your feedback! \t \n" + \
             "I am open to whatever requests the community makes. If your message is urgent, please feel free to " + \
             "PM me at /u/" + accountinfo.developerusername + ". Thanks again!" + \
             compose_salutation()
    return result


def compose_reject_message(username, subject, body):
    result = compose_greeting(username) + \
             "**There was an error processing your request.** Please review your message and " + \
             "make sure it follows the guidelines that have been set. Please private message the bot " + \
             "with the subject 'Information' to get detailed information on how the bot works, " + \
             "or message /u/" + accountinfo.developerusername + " if you want specialized help or have any " + \
             "questions for me. Thank you for your patience! \n\t \n\t \n" + \
             "**Your request:** \t \n" + \
             "Subject:\t" + subject + "\t \n" + \
             "Body:\t\t" + body + \
             compose_salutation()
    return result


def format_subreddit_list(subreddits, title):
    i = 0
    result = '###' + title + '\n' + \
             '\#|Subreddit' + '\n' + \
             ':--|:--' + '\n'
    for subreddit in subreddits:
        i += 1
        result += str(i) + '|' + str(subreddit) + '\n'
    return result


def compose_invalid_subreddit_message(username, invalid_subreddits, message):
    result = compose_greeting(username) + \
        'Unfortunately, it appears that the following subreddit(s) you tried to subscribe to were invalid. If you ' + \
        'believe this is a mistake please message /u/' + accountinfo.developerusername + '. Sorry for the ' + \
        'inconvenience!\t \n\t \n' + \
        '**Subject:**\t' + message.subject + '\t \n' + \
        '**Body:**\t\t' + message.body + '\t \n' + \
        format_subreddit_list(invalid_subreddits, 'Invalid Subreddits') + \
        compose_salutation()
    return result


def compose_match_message(sub, submission, subs):
    print("SELFTEXT:   \n" + str(vars(submission)))
    result = compose_greeting(sub.username) + \
        "**Post Title:**\t \n" + \
        "[" + submission.title + "](" + submission.permalink + ")\t \n\t \n" + \
        (("**Body Text:**\t \n" + submission.preview) if submission.is_self
         else ("**Post Content Link:**\t \n[Content Link](" + submission.url + ")")) + \
        "\t \n\t \n" + \
        sub.to_table('Matched Subscription') + "\t \n\t \n" + \
        format_subscription_list(subs, 'Your Subscriptions') + \
        compose_salutation()
    return result


def compose_too_generic_message(username):
    result = compose_greeting(username) + \
        "Unfortunately, your subscription request is too generic. Allowing such a subscription would probably hog " + \
        "the bot's resources. Try constraining the subscription a bit. Sorry, and thanks for your understanding." + \
        compose_salutation()
    return result


def compose_statistics(username, current_users, all_users, unique_subs, all_subs, unique_subreddits, all_matches):
    result = compose_greeting(username) + \
        '###Statistics\n' + \
        'Statistic|Value\n' + \
        '--:|:--:' + '\n' + \
        'Current Users Subscribed|' + str(current_users) + '\n' + \
        'Total Users|' + str(all_users) + '\n' + \
        'Unique Subscriptions|' + str(unique_subs) + '\n' + \
        'Active Subscriptions|' + str(all_subs) + '\n' + \
        'Unique Subreddits|' + str(unique_subreddits) + '\n' + \
        "Total Matches to Date|" + str(all_matches) + "\n\n\n" + \
        "Thank ***YOU*** for being a part of that!\n" + \
        compose_salutation()
    return result


def compose_feedback_forward(username, body):
    result = compose_greeting(accountinfo.developerusername) + \
             "You have received feedback from /u/" + username + ". The feedback is quoted below:\n\n'" + \
             body + "'" + compose_salutation()
    return result


def compose_username_mention_forward(username, body):
    result = compose_greeting(accountinfo.developerusername) + \
             'The bot has been mentioned in a post! the body of the message is quoted below:\n\n' + \
             'USERNAME: ' + username + '\nBODY:\n' + body
    return result


def compose_post_reply_forward(username, body):
    result = compose_greeting(accountinfo.developerusername) + \
             'Someone has responded to a post by the bot! the comment is quoted below:\n\n' + \
             'USERNAME: ' + username + '\nBODY:\n' + body
    return result


SIGNATURE = '\n\t \n\t \n-/u/' + accountinfo.username

# TODO UPDATE THIS!
INFORMATION = \
    "Thanks for your interest in the bot! This is how it works: \n\n" + \
    \
    "###Subscribing\n" + \
    "Send the bot a private message with the subject line as the exact string you " + \
    "want it to keep an eye out for, and the body as 'subscribe'. Keep it " + \
    "semi-general as to not limit the search too much. For example, use " + \
    "'i5-4590' instead of 'Intel Core i5-4590 3.3GHz LGA 1150'. \n\n" + \
    \
    "###What the bot does\n" + \
    "The bot will send you a message that contains a link to that item each time " + \
    "it come across a post in /r/buildapcsales that matches. It will be a reply " + \
    "to the original message you sent. This will happen until you send the bot a " + \
    "message unsubscribing from the part, which is described more in the next " + \
    "line. \n\n" + \
    \
    "###Unsubscribing\n" + \
    "If or when you want to unsubscribe, send the bot another private message with " + \
    "the subject line as the item you want to unsubscribe from, and the body as " + \
    "'Unsubscribe'. If you want to unsubscribe from ALL of the parts you are " + \
    "subscribed to, make the body of the pm 'unsubscribe all' and the subject line " + \
    "can be whatever you want. \n\n" + \
    \
    "###Getting Help\n" + \
    "Remember that you can always send the bot a message with the subject line as " + \
    "'Information' or 'Help' to get this message, and all of the parts you are " + \
    "subscribed to. If you want more specific help, send a private message to /u/" + \
    accountinfo.developerusername + " and I will try my absolute best to help you out.\n\n" + \
    \
    "###Feedback\n" + \
    "I am always open to feedback, requests, or things of that nature. While I am " + \
    "very much still in the process of learning, I will try my best to take your " + \
    "feedback into consideration. Sending me feedback should use the subject line " + \
    "'Feedback'."
