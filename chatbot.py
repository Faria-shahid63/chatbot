import re

# Define a generic response for unknown inputs
def unknown():
    return "I'm not sure I understand. Can you please rephrase?"

# Define a response for "what do you eat?" or similar questions
R_EATING = "I don't eat, but thanks for asking!"

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True
    
    # Count how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1
            
    # Calculate the percent of recognised words in a user message 
    if len(recognised_words) > 0:
        percentage = float(message_certainty) / float(len(recognised_words))
    else:
        percentage = 0

    # Check if all required words are present
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break 
    
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0
        
def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)
       
    # Responses ------------
    response('Hello!', ['hello', 'sup', 'hi', 'hey', 'heyo'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('Thank you!', ['I', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    response(R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
    
    print("Probability list:", highest_prob_list)  # Debugging output
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    
    return unknown() if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    responses = check_all_messages(split_message)
    return responses 

# Testing the response system 
while True:
    user_input = input('You: ')
    if user_input.lower() == 'exit':
        print('Bot: Goodbye!')
        break
    print('Bot: ' + get_response(user_input))