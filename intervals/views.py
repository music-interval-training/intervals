from django.shortcuts import render

import logging
from ask_sdk_core.utils import is_request_type
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.handler_input import HandlerInput
from django.views.decorators.csrf import csrf_exempt
from ask_sdk_model import Response

from .interval import get_audio_info

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def home_page(request):
    return render(request, "intervals/home_page.html")


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response        
        logger.info("In LaunchRequestHandler")

        speak_output = "Hello! This is Music Interval Training. Shall I play an interval for you to guess?"
        reprompt = "Say yes to start interval training or no to quit"
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )
    
class StartTrainingIntentHandler(AbstractRequestHandler):
    # setting of session attributes
    def can_handle(self, handler_input):
        logger.info("In StartTrainingIntentHandler can handle") 

        return ask_utils.is_request_type("StartTrainingIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In StartTrainingIntentHandler")
        # attrs is an assumed empty attributes dictionary established  in order to store  session attributes.
        attrs = handler_input.attributes_manager.persistent_attributes
        interval, audio_url = get_audio_info()
        # persistent attributes is a dictonary with the key interval
        attrs['interval'] = interval 
        # stores session attributes
        logger.info(interval)
        logger.info(audio_url)

        handler_input.attributes_manager.session_attributes = attrs
        speak_output = f"Great! Guess the interval <audio src='{audio_url}' />"
      
        return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask("What is your guess?")
                    .response
            )

class IntervalGuessIntentHandler(AbstractRequestHandler):
    # getting session attributes
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("IntervalGuessIntent")(handler_input)

    def handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        interval = session_attrs['interval']
        slots = handler_input.request_envelope.request.intent.slots
        guess = slots["INTERVAL"].value
        is_correct = interval == guess
        if is_correct:
            speak_output = f"Your guess was correct"
        else:
            speak_output = f"You guessed {guess} but the interval was a {interval}"

        return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask("Do you want to continue guessing?")
                    .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

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
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
                )

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

# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
            handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))


# Register all handlers, interceptors etc.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StartTrainingIntentHandler())
sb.add_request_handler(IntervalGuessIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())
# Add response interceptor to the skill.
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger());


skill = sb.create()

