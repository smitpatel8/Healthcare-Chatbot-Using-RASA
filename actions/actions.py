# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

#For performing Forms:

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from Database_connectivity import userinfo, hospitals_near_me, new_Disease, new_Symptom
from MailCheck import email
from diseasePrediction import disease_prediction_rasa

class ValidateForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["name", "number", "email", "age", "gender", "reason", "time"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        userinfo(tracker.get_slot("name"), tracker.get_slot("number"), tracker.get_slot("email"),
                 tracker.get_slot("age"), tracker.get_slot("gender"), tracker.get_slot("reason"), tracker.get_slot("time"))

        dispatcher.utter_message(template="utter_details_thanks",
                                 Name=tracker.get_slot("name"),
                                 Mobile_number=tracker.get_slot("number"),
                                 Email=tracker.get_slot("email"),
                                 Age=tracker.get_slot("age"),
                                 Gender=tracker.get_slot("gender"),
                                 Reason=tracker.get_slot("reason"),
                                 Time=tracker.get_slot("time"))

        result = email(tracker.get_slot("name"), tracker.get_slot("number"), tracker.get_slot("email"),
                       tracker.get_slot("age"), tracker.get_slot("gender"), tracker.get_slot("reason"), tracker.get_slot("time"))
        if result == "success":
            dispatcher.utter_message(text="Your appointment is confirmed and you will receive a mail")

class ActionLocation(Action):
    def name(self) -> Text:
        return "action_ask_location"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:

        location = tracker.get_slot('location')
        result = hospitals_near_me(location)

        if result == "Failed":
            dispatcher.utter_message(text="Sorry!, I couldn't find any info to provide for this location")
        else:
            dispatcher.utter_message(text=f"Hospitals found in {location} are:")
            for res in result:
                for i in range(1):
                    x = res[i]
                    dispatcher.utter_message(text=f"{x}")


class ActionDisease(Action):
    def name(self) -> Text:
        return "action_new_disease_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:

        d_name = tracker.get_slot('new_disease')
        result = new_Disease(d_name)

        if result == "Failed":
            dispatcher.utter_message(text="Sorry, But we didn't have any info to provide")
        else:
            dispatcher.utter_message(text=f"{result[0]}")

class ActionSymptom(Action):
    def name(self) -> Text:
        return "action_new_symptom_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:

        d_name = tracker.get_slot('new_disease')
        result = new_Symptom(d_name)

        if result == "Failed":
            dispatcher.utter_message(text="Sorry, But we didn't have any info to provide")
        else:
            dispatcher.utter_message(text=f"{result[0]}")


class ActionPrediction(Action):
    def name(self) -> Text:
        return "action_prediction"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:

        rasa_symp = tracker.get_slot('user_symptoms')
        result_dName, result_dProb = disease_prediction_rasa(rasa_symp)
        if result_dName == "Failed":
            dispatcher.utter_message(text="try again please")
        else:
            for res in range(0, len(result_dName)):
                dispatcher.utter_message(text=f"Disease Name-{result_dName[res]}, Disease probability-{result_dProb[res]} %")