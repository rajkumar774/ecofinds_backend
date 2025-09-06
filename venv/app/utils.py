from bson import ObjectId
from bson.errors import InvalidId

def oid(s: str) -> ObjectId:
    try:
        return ObjectId(s)
    except InvalidId:
        raise ValueError("Invalid id")

def serialize_id(doc):
    if not doc:
        return doc
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc
