#Imports
#import os
import random
import logging
import json
import prompts
import my_functions as mf

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Built-in Intent Handlers
#For developing/testing purposes, this test handler has been included
class TestHandler(AbstractRequestHandler):
        """Handler for Skill Launch."""
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return ask_utils.is_intent_name("TestIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Responsejam
            logger.info("In TestHandler")
            speak_output = "TEST ANSWER"
            reprompt = "Hola?"

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(reprompt)
                    .response
            )

#This is the handler for the skill launch
class LaunchRequestHandler(AbstractRequestHandler):
        """Handler for Skill Launch."""
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return ask_utils.is_request_type("LaunchRequest")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Responsejam
            logger.info("In LaunchRequest")
            speak_output = "Bienvenido, cómo puedo ayudarte?"

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .response
            )

#This is the handler for a brand new fact/ecotip
class GetNewFactHandler(AbstractRequestHandler):

        def can_handle(self, handler_input):
            return ask_utils.is_intent_name("GetNewFactIntent")(handler_input)

        def handle(self, handler_input):
            logger.info("In GetNewFactHandler")

            # get localization data
            data = handler_input.attributes_manager.request_attributes["_"]

            #Retrieves the facts dict and computes the categories (keys)
            facts = data[prompts.FACTS]
            categories = [c for c in facts.keys()]

            #Use the random library to select a category and then select a random fact of that category
            random_topic = random.choice(categories)
            random_fact = random.choice(data[prompts.FACTS][random_topic])

            #Random question for the reprompt
            question = random.choice(data[prompts.ANOTHER_FACT])

            #Building the speech like this, we don't have to wait to use the reprompt.
            speech = data[prompts.GET_FACT_MESSAGE].format(random_topic,random_fact,question)

            handler_input.response_builder.speak(speech).ask(question).set_card(SimpleCard(data[prompts.SKILL_NAME], random_fact))

            return handler_input.response_builder.speak(speech).response
#This is the handler for a fact/ecotip from a specific category
class GetCategoryFactHandler(AbstractRequestHandler):

        def can_handle(self, handler_input):
            return ask_utils.is_intent_name("GetCategoryFactIntent")(handler_input)

        def handle(self, handler_input):
            logger.info("In GetCategoryFactHandler")

            # get localization data
            data = handler_input.attributes_manager.request_attributes["_"]

            #Retrieves the facts dict and computes the categories (keys)
            facts = data[prompts.FACTS]
            categories = [c for c in facts.keys()]

            #This function will retrieve the desired category
            fact_category = mf.get_category_value(
            handler_input.request_envelope.request, 'category')

            #Building several questions like this, the question at the end of the speech won't be the same as the reprompt
            reprompt_question = "You can ask me for an eco-tip!"
            question = random.choice(data[prompts.ANOTHER_FACT])

            logger.info("FACT CATEGORY = {}".format(fact_category))

            #In the case that we have the category on our list, we'll just use the dictionary
            if fact_category in categories:
                logger.info("Category found in the list")
                random_fact = random.choice(data[prompts.FACTS][fact_category])
                speech = data[prompts.GET_FACT_MESSAGE].format(fact_category,random_fact,question)

                handler_input.response_builder.speak(speech).ask(reprompt_question).set_card(
                    SimpleCard(data[prompts.SKILL_NAME], random_fact))
                return handler_input.response_builder.response
            #If we do not have that category, we'll response with a random fact
            else:
                logger.info("Category NOT found in the list")
                random_topic = random.choice(categories)
                random_fact = random.choice(data[prompts.FACTS][random_topic])
                speech = data[prompts.GET_FACT_MESSAGE].format(random_topic, random_fact,question)

                handler_input.response_builder.speak(speech).ask(reprompt_question).set_card(
                    SimpleCard(data[prompts.SKILL_NAME], random_fact))
                return handler_input.response_builder.response

#Classic hello intent
class HelloIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            return ask_utils.is_intent_name("HelloIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            logger.info("In HelloIntent")
            speak_output = "Buenos dias, bienvenido a la Casa Verde!"

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .response
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    #.response
            )

#This intent is for the reprompts, if the user says yes, we want to reply with another fact
class YesHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return ask_utils.is_intent_name("YesIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            logger.info("In YesHandler")
            return GetNewFactHandler().handle(handler_input)

#If the user says no, we want to close the session and say goodbye
class NoHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return ask_utils.is_intent_name("NoIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            logger.info("In NoHandler")

            data = handler_input.attributes_manager.request_attributes["_"]
            goodbye = random.choice(data[prompts.STOP_MESSAGE])

            return handler_input.response_builder.speak(goodbye).set_should_end_session(True).response

#Built-in handlers
class HelpIntentHandler(AbstractRequestHandler):
        #Handler for Help Intent.
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            logger.info("In HelpIntent")
            speak_output = "HELP? I NEED SOMEBODY, HEELP!"

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )


class CancelOrStopIntentHandler(AbstractRequestHandler):
        """Single handler for Cancel and Stop Intent."""
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                    ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            data = handler_input.attributes_manager.request_attributes["_"]
            goodbye = random.choice(data[prompts.STOP_MESSAGE])

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .response
            )


class SessionEndedRequestHandler(AbstractRequestHandler):
        """Handler for Session End."""
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response

            # Any cleanup logic goes here.

            return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
        """The intent reflector is used for interaction model testing and debugging.
        It will simply repeat the intent the user said. You can create custom handlers
        for your intents by defining them above, then also adding them to the request
        handler chain below.
        """
        def can_handle(self, handler_input):
            # type: (HandlerInput) -> bool
            return ask_utils.is_request_type("IntentRequest")(handler_input)

        def handle(self, handler_input):
            # type: (HandlerInput) -> Response
            intent_name = ask_utils.get_intent_name(handler_input)
            speak_output = "You just triggered " + intent_name + "."

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )


class CatchAllExceptionHandler(AbstractExceptionHandler):
        """Generic error handling to capture any syntax or routing errors. If you receive an error
        stating the request handler chain is not found, you have not implemented a handler for
        the intent being invoked or included it in the skill builder below.
        """
        def can_handle(self, handler_input, exception):
            # type: (HandlerInput, Exception) -> bool
            return True

        def handle(self, handler_input, exception):
            # type: (HandlerInput, Exception) -> Response
            logger.error(exception, exc_info=True)

            speak_output = "Sorry, I had trouble doing what you asked. Please try again."

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )

class LocalizationInterceptor(AbstractRequestInterceptor):
        """
        Add function to request attributes, that can load locale specific data.
        """

        def process(self, handler_input):
            locale = handler_input.request_envelope.request.locale
            logger.info("Locale is {}".format(locale[:2]))

            # localized strings stored in language_strings.json
            with open("language_strings.json") as language_prompts:
                language_data = json.load(language_prompts)
            # set default translation data to broader translation
            data = language_data[locale[:2]]
            # if a more specialized translation exists, then select it instead
            # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
            #          then pick that instead
            if locale in language_data:
                data.update(language_data[locale])
            handler_input.attributes_manager.request_attributes["_"] = data

# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
        """Log the alexa requests."""

        def process(self, handler_input):
            # type: (HandlerInput) -> None
            logger.debug("Alexa Request: {}".format(
                handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
        """Log the alexa responses."""

        def process(self, handler_input, response):
            # type: (HandlerInput, Response) -> None
            logger.debug("Alexa Response: {}".format(response))
