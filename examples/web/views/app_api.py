# Example writer stub.
@bp.get("/api/app/sessions")
def sessions():
    return {"sessions": [], "next_before": None}
