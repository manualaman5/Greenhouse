#Imports
#import os
import random
import logging
import json
import prompts

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bienvenido, cómo puedo ayudarte?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# Built-in Intent Handlers

class GetNewFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetNewFactIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        random_fact = random.choice(data[prompts.FACTS])
        speech = data[prompts.GET_FACT_MESSAGE].format(random_fact)

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(data[prompts.SKILL_NAME], random_fact))
        return handler_input.response_builder.response


class HelloIntentHandler(AbstractRequestHandler):
    """Handler for Hello Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Buenos dias, bienvenido a la Casa Verde!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

"""
class SampleIntentHandler(AbstractRequestHandler):
    #Handler for Sample Intent.
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SampleIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #attr = handler_input.attributes_manager.session_attributes
        #day = attr["day"]
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = "QUIZ"
        day = attr["state"]
        #slots = handler_input.request_envelope.request.intent.slots
        #day = slots["day"]
        speak_output = "Up and running with the number "+day+"!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
"""

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
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
        speak_output = "Goodbye!"

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

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()

#Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetNewFactHandler())
#sb.add_request_handler(SampleIntentHandler())
sb.add_request_handler(HelloIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

#Register xception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Register request and response interceptors
sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()
