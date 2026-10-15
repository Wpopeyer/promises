# Example writer stub.
def mirror_driver(driver):
    firestore.collection("drivers").document(driver.email).set({"is_tester": False})
