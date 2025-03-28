
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import json
import anthropic
import requests

def home(request):
    return render(request, 'music.html', {})

@csrf_exempt
@require_http_methods(["POST"])
def get_recommendation(request):
    """
    Endpoint to get a new music recommendation
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        system_prompt = data.get('systemPrompt')
        position = data.get('position')
        time = data.get('time')
        weather = data.get('weather')
        anthropic_api_key = data.get('anthropicApiKey')
        prompt_template = data.get('promptTemplate')
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        if not anthropic_api_key:
            return JsonResponse({'error': 'Anthropic API key is required'}, status=400)
        
        # Get weather and create context
        context = _create_context(user_message, position, time, weather)
        
        # Get recommendation from Claude using client-provided template
        claude_response, user_request = _get_claude_response(context, anthropic_api_key, prompt_template, system_prompt)
        
        return JsonResponse({
            'response': claude_response,
            'request': user_request,
        })
    except Exception as e:
        raise
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def continue_conversation(request):
    """
    Endpoint to continue an existing conversation
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        system_prompt = data.get('systemPrompt')
        position = data.get('position')
        time = data.get('time')
        weather = data.get('weather')        
        time = data.get('time')        
        message_history = data.get('messageHistory', [])
        anthropic_api_key = data.get('anthropicApiKey')
        prompt_template = data.get('promptTemplate')
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        if not anthropic_api_key:
            return JsonResponse({'error': 'Anthropic API key is required'}, status=400)
        
        # Get weather and create context
        context = _create_context(user_message, position, time, weather)
        
        # Get response from Claude with message history
        claude_response, user_request = _get_claude_response(context, anthropic_api_key, prompt_template, system_prompt, message_history)
        
        return JsonResponse({
            'response': claude_response,
            'request': user_request,            
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def _create_context(user_message, position, time, weather):
    """
    Create context for Claude with time, position, and weather info
    """
    context = {
        'position': position,
        'time': time,
        'weather': weather,
        'user_message': user_message
    }
    
    return context

def _get_claude_response(context, api_key, prompt_template='', system_prompt='', message_history=None):
    """
    Get a response from Claude API
    """
    if not api_key:
        raise ValueError("Anthropic API key is required")
    
    client = anthropic.Anthropic(api_key=api_key)

    user_message = prompt_template.format(**context)
    
    try:
        if message_history:
            # Continue conversation
            response = client.messages.create(
                model="claude-3-7-sonnet-latest",
                system=system_prompt,
                messages=message_history + [{"role": "user", "content": user_message}],
                max_tokens=1024
            )
        else:
            # New conversation
            response = client.messages.create(
                model="claude-3-7-sonnet-latest",
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
                max_tokens=1024
            )
        
        return response.content[0].text, user_message
        
    except Exception as e:
        error_message = str(e)
        if 'authentication' in error_message.lower():
            raise ValueError("Invalid Anthropic API key")
        print(f"Error getting Claude response: {e}")
        return "Sorry, I couldn't generate a recommendation at this time. Please try again later."
