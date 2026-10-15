# Example HTTP function stub.
@functions_framework.http
def firestore_upsert(request):
    body = request.get_json()
    operation = body.get("operation", "set")
