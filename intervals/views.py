from collections import OrderedDict
from random import choice
from django.shortcuts import render
from django.db.models import Count, Max
from django.views.generic import View
from django.http import JsonResponse


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
from .models import Record

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ORDERED_INTERVALS = ['minor 2nd', 'major 2nd', 'minor 3rd', 'major 3rd', 'perfect 4th', 'tritone', 'perfect 5th', 'minor 6th', 'major 6th', 'minor 7th', 'major 7th', 'octave' ]
CORRECT_GUESS_RESPONSES = ['Great job! You guessed correct', 'Well done', 'You mastered that one', 'Way to kill it Beethoven', 'Nice you got it right']
INCORRECT_GUESS_RESPONSES = [f"You guessed {guess} but the interval was a {interval[0]}",  f"Epic fail. you guessed {guess} but it was a {interval[0]}", f"Nice try but that was wrong. it was a {interval[0]} but you guessed {guess}", f"next time you'll get it right but the correct interval was a {interval[0]} you guessed {guess}"]

def home_page(request):
    return render(request, "intervals/home_page.html")
        

def progress_details(request):
    correct_attempts = Record.objects.filter(is_correct=1).values('interval').annotate(correct=Count('interval'))
    incorrect_attempts = Record.objects.filter(is_correct=0).values('interval').annotate(incorrect=Count('interval'))

    chart_data = OrderedDict()
    for x in ORDERED_INTERVALS:
        chart_data[x] = {'interval': x, 'correct':0, 'incorrect': 0}
        if correct_attempts.filter(interval=x).exists():
            chart_data[x].update(correct_attempts.get(interval=x))
        if incorrect_attempts.filter(interval=x).exists():
            chart_data[x].update(incorrect_attempts.get(interval=x))

    max_attempts = Record.objects.values('interval').annotate(attempts=Count('interval')).aggregate(Max('attempts'))['attempts__max']
    return render(request, "intervals/progress_details.html", {
        'chart_data': chart_data,
        'max_attempts': max_attempts,
    })


class ChartData(View):
    def get(self, request):
        correct_attempts = Record.objects.filter(is_correct=1).values('interval').annotate(correct=Count('interval'))
        incorrect_attempts = Record.objects.filter(is_correct=0).values('interval').annotate(incorrect=Count('interval'))

        chart_data = OrderedDict()
        for x in ORDERED_INTERVALS:
            chart_data[x] = {'interval': x, 'correct':0, 'incorrect': 0}
            if correct_attempts.filter(interval=x).exists():
                chart_data[x].update(correct_attempts.get(interval=x))
            if incorrect_attempts.filter(interval=x).exists():
                chart_data[x].update(incorrect_attempts.get(interval=x))

        correct = [x['correct'] for x in chart_data.values()]
        incorrect = [x['incorrect'] for x in chart_data.values()]
        max_attempts = Record.objects.values('interval').annotate(attempts=Count('interval')).aggregate(Max('attempts'))['attempts__max']
        return JsonResponse({
            'correct': correct,
            'incorrect': incorrect,
            'max_attempts': max_attempts
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
            speak_output = choice(CORRECT_GUESS_RESPONSES)
        else:
            speak_output = choice(INCORRECT_GUESS_RESPONSES)
        speak_output = f"{speak_output} Do you want to continue?"

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


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input) or
                ask_utils.is_intent_name("noIntent")(handler_input)
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
# sb.add_request_handler(StartTrainingIntentHandler())
sb.add_request_handler(IntervalGuessIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())
# Add response interceptor to the skill.
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())


skill = sb.create()

