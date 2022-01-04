from typing import Any, Text, Dict, List
from rasa_sdk.events import FollowupAction, ActionExecuted

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):



    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        a = tracker.events

        intents_list = []

        for x in a:
            if x['event'] == 'user':
                intents_list.append(x['parse_data']['intent']['name'])
            elif x['event'] == 'bot':
                try:
                    intents_list.append(x['metadata']['utter_action'])
                except:
                    pass

        # count how many confirms/how many rejects
        # intents that lead to this ca: conf/rej/alr done/alr agent
        #['start_conversation', 'utter_greeting_sharon_prudential']
        if intents_list[2] == 'confirm':

        if intents_list[-3::2] ==  ['looking_for', 'reject']:
            mx = 'oh okay thank you have a nice day good bye'
        elif intents_list[-2:] ==  ['utter_greeting_sharon_prudential', 'reject']:
            mx = 'mx'
            dispatcher.utter_message(response = "utter_discuss_nomination")
            return []
            #return [FollowupAction("utter_discuss_nomination"), FollowupAction("action_listen")]
        elif intents_list.count('reject') == 1:
            mx = 'erm okay can I understand this may not be a top priority right now or perhaps you don’t see the value in it er many people have said the same but once my manager meet them up and guide along with the nomination they find it very useful to have this settle before hand erm allow me to have  two minutes of your time and I promise that erm that you will be clear anot on whether or not this is a good use of your time'
        elif str(['utter_greeting_sharon_prudential', 'reject'])[1:-1] in str(intents_list)[1:-1]:
            mx = "erm okay can I understand this may not be a top priority right now or perhaps you don’t see the value in it er many people have said the same but once my manager meet them up and guide along with the nomination they find it very useful to have this settle before hand erm allow me to have  two minutes of your time and I promise that erm that you will be clear anot on whether or not this is a good use of your time"
        else:
            mx = 'oh okay thank you have a nice day good bye'

        dispatcher.utter_message(text=mx+str(intents_list))

        return []


class fast_sharon(Action):

    def name(self) -> Text:
        return "fast_sharon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        a = tracker.events

        story_list = []
        only_intents = []

        for x in a:
            if x['event'] == 'user':
                story_list.append(x['parse_data']['intent']['name'])
                only_intents.append(x['parse_data']['intent']['name'])
            elif x['event'] == 'bot':
                try:
                    story_list.append(x['metadata']['utter_action'])
                except:
                    pass

                
        #only_intents = ["start_conversation","confirm","reject","confirm","who_is","confirm","confirm","age"]        

        repeat = ''
        # if the last if the who_are_you_aff then add repeat
        if only_intents[-2:] == ["who_is","confirm"]:
            repeat = 'rep_'

        only_intents= str(only_intents).replace("'who_is', 'confirm'", "").replace("'","").replace(" ","")[1:-1]


        only_intents= [x for x in only_intents.split(",") if x!= ""]


        len_a = len(only_intents)

        reply = 'utter_goodbye'
        if len_a == 1:
            reply = 'utter_goodbye'
        if len_a == 2:
            if only_intents == ['start_conversation', 'confirm']:
                reply = 'utter_discuss_nomination'
            elif only_intents == ['start_conversation', 'reject']:
                reply = 'utter_discuss_nomination'
        elif len_a == 3:
            if only_intents == ['start_conversation', 'confirm', 'confirm']:
                reply = 'utter_appointment_call_time'
            elif only_intents == ['start_conversation', 'confirm', 'reject']:
                reply = 'utter_convincing'
            elif only_intents == ['start_conversation', 'confirm', 'done_nom']:
                reply = 'utter_done_nomination'
            elif only_intents == ['start_conversation', 'confirm', 'already_have_agent']:
                reply = 'try_us'
            elif only_intents == ['start_conversation', 'reject', 'confirm']:
                reply = 'utter_appointment_call_time'
        elif len_a == 4:
            if only_intents == ['start_conversation', 'confirm', 'reject','confirm']:
                reply = 'utter_appointment_call_time'
            elif only_intents[:-1] == ['start_conversation', 'confirm', 'confirm']\
                and only_intents[-1] in ['confirm','morning','afternoon','evening']:
                reply = 'utter_age_info'
            elif only_intents[:-1] == ['start_conversation', 'reject', 'confirm']\
                and only_intents[-1] in ['confirm','morning','afternoon','evening']:
                reply = 'utter_age_info'
        elif len_a == 5:
            if only_intents[:-1] == ['start_conversation', 'confirm', 'reject', 'confirm']\
                and only_intents[-1] in ['confirm','morning','afternoon','evening']:
                reply = 'utter_age_info'

        dispatcher.utter_message(response = reply)
        return []


