# Example writer stub. The lint checks that each declared key still appears here.
def mirror_session(session):
    payload = {
        "is_parked": session.ended_at is None,
        "zone_type": get_zone_type(session.zone.tariff_code),
    }
    firestore.collection("sessions").document(session.plate).set(payload)
