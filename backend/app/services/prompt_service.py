from hashlib import sha256
from pathlib import Path

from sqlalchemy.dialects.sqlite import insert

from app.database.models import PromptVersion
from app.schemas import Group


PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"
TECHNIQUES = {
    Group.ELIZA: "pattern_matching",
    Group.BASELINE: "baseline",
    Group.ZERO_SHOT: "zero_shot",
    Group.FEW_SHOT: "few_shot",
}


def register_prompts(db):
    baseline = (PROMPT_DIR / "baseline.txt").read_text(encoding="utf-8").strip()
    zero = (PROMPT_DIR / "zero_shot.txt").read_text(encoding="utf-8").strip()
    examples = (PROMPT_DIR / "few_shot.txt").read_text(encoding="utf-8").strip()
    few = (
        zero + "\n\nUse these examples as demonstrations of conversational style. "
        "Do not treat them as personal facts to repeat.\n\n" + examples
    )
    versions = {}
    for group, content in ((Group.BASELINE, baseline), (Group.ZERO_SHOT, zero), (Group.FEW_SHOT, few)):
        technique = TECHNIQUES[group]
        digest = sha256(content.encode("utf-8")).hexdigest()
        version = f"v1-{digest[:12]}"
        identifier = f"{technique}:{version}"
        query = insert(PromptVersion).values(
            id=identifier, technique=technique, version=version, content=content, content_hash=digest,
        ).on_conflict_do_nothing(index_elements=["id"])
        db.execute(query)
        versions[group] = identifier
    return versions
