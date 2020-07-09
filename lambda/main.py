
from ask_sdk_core.skill_builder import SkillBuilder

#Imports from handlers.py
import handlers as h

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers in the handlers.py. Make sure any new handlers or interceptors
# are included below. The intents will be processed in order, so if the can handle is true for several intents,
# the skill will use the first one 
sb = SkillBuilder()

#Register intent handlers
sb.add_request_handler(h.LaunchRequestHandler())
sb.add_request_handler(h.TestHandler())
sb.add_request_handler(h.GetNewFactHandler())
sb.add_request_handler(h.GetCategoryFactHandler())
sb.add_request_handler(h.YesHandler())
sb.add_request_handler(h.NoHandler())
sb.add_request_handler(h.HelloIntentHandler())

#Other Handlers
sb.add_request_handler(h.HelpIntentHandler())
sb.add_request_handler(h.CancelOrStopIntentHandler())
sb.add_request_handler(h.SessionEndedRequestHandler())
sb.add_request_handler(h.IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

#Register xception handlers
sb.add_exception_handler(h.CatchAllExceptionHandler())

# Register request and response interceptors
sb.add_global_request_interceptor(h.LocalizationInterceptor())
sb.add_global_request_interceptor(h.RequestLogger())
sb.add_global_response_interceptor(h.ResponseLogger())

lambda_handler = sb.lambda_handler()
