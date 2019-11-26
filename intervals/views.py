from django.shortcuts import render

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type
from ask_sdk_model import Response
from django.views.decorators.csrf import csrf_exempt
from .interval import get_audio_file

sb = SkillBuilder()


def home_page(request):
    return render(request, "intervals/home_page.html")

def progress_details(request):

    Records = Record.objects.all()
    return render(request, "intervals/progress_details.html", {
        'Records': Records,
    })


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
         return (ask_utils.is_request_type("LaunchRequest")(handler_input) or
                ask_utils.is_intent_name("GetNewIntervalIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response        
        logger.info("In LaunchRequestHandler") 
        interval, audio_url = get_audio_info()
        # adding keys to session attributes to be retrieved in another handler.
        attrs = {
            'interval': interval,
            'audio_url': audio_url
        }
        # stores session attributes
        logger.info(interval)
        logger.info(audio_url)

        handler_input.attributes_manager.session_attributes = attrs
        speak_output = f"Great! I will play an interval for you to guess <audio src='{audio_url}' /> What is your guess"
      
        return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )


class IntervalGuessIntentHandler(AbstractRequestHandler):
    # getting session attributes
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("IntervalGuessIntent")(handler_input)

    def handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        interval = session_attrs['interval']
        audio_url = session_attrs['audio_url']
        slots = handler_input.request_envelope.request.intent.slots
        guess = slots["INTERVAL"].value
        Record.objects.create(
            guess=guess,
            interval=interval[0],
            audio_url=audio_url
        )
        is_correct = guess in interval
        if is_correct:
            speak_output = f"Your guess was correct"
        else:
            speak_output = f"You guessed {guess} but the interval was a {interval[0]}"
        speak_output = f"{speak_output} Do you want to continue guessing?"

        return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
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

# Other skill components here ....

# Register all handlers, interceptors etc.
sb.add_request_handler(LaunchRequestHandler())

skill = sb.create()

