from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .llm import get_reply


def index(request):
    """Page principale du chatbot — initialise la conversation en session."""
    if "conversation" not in request.session:
        request.session["conversation"] = []
    return render(request, "chat/index.html", {
        "conversation": request.session["conversation"],
    })


@require_POST
def chat(request):
    """Reçoit un message, appelle le LLM, retourne la réponse en JSON."""
    data = json.loads(request.body)
    user_message = data.get("message", "").strip()

    if not user_message:
        return JsonResponse({"error": "Message vide"}, status=400)

    conversation = request.session.get("conversation", [])

    try:
        reply = get_reply(conversation, user_message)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    # Mettre à jour l'historique de session
    conversation.append({"role": "user", "content": user_message})
    conversation.append({"role": "assistant", "content": reply})
    request.session["conversation"] = conversation
    request.session.modified = True

    return JsonResponse({"reply": reply})


def reset(request):
    """Réinitialise la conversation."""
    request.session["conversation"] = []
    return JsonResponse({"status": "ok"})
