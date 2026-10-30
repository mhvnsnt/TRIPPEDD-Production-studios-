"""Characterizer profile loading (SPEC M-1).

Clean-room, original code. A *profile* is a JSON file mapping canonical
humanoid roles (``hips``, ``upper_arm.L`` ...) to the bone names a given
skeleton family actually uses. Profiles ship in ``../../profiles/*.json``
relative to this package, and users may point the add-on at any folder of
profile JSONs of the same shape.
"""
import json
import os

# Canonical role template every profile maps onto. Order matters: parents
# before children, so retarget/bake can walk the list topologically.
CANONICAL_ROLES = [
    "hips",
    "spine", "spine2", "chest",
    "neck", "head",
    "shoulder.L", "upper_arm.L", "forearm.L", "hand.L",
    "shoulder.R", "upper_arm.R", "forearm.R", "hand.R",
    "thigh.L", "shin.L", "foot.L", "toe.L",
    "thigh.R", "shin.R", "foot.R", "toe.R",
]


def default_profiles_dir():
    """Folder of shipped profile JSONs (tools/characterizer/profiles)."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", "profiles"))


def list_profile_files(profiles_dir=None):
    folder = profiles_dir or default_profiles_dir()
    if not os.path.isdir(folder):
        return []
    return sorted(
        os.path.join(folder, name)
        for name in os.listdir(folder)
        if name.lower().endswith(".json")
    )


def load_profile(path):
    """Load one profile JSON -> dict with at least 'profile' and 'bones'."""
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or "bones" not in data:
        raise ValueError("profile %s has no 'bones' mapping" % path)
    data.setdefault("profile", os.path.splitext(os.path.basename(path))[0])
    return data


def load_all_profiles(profiles_dir=None):
    """Return {profile_name: profile_dict} for every JSON in the folder."""
    out = {}
    for path in list_profile_files(profiles_dir):
        try:
            prof = load_profile(path)
        except Exception:
            continue
        out[prof["profile"]] = prof
    return out


def build_mapping(source_profile, target_profile):
    """Pair bones by shared canonical role.

    Returns a list of dicts (in CANONICAL_ROLES order, parents first):
    ``{"role": role, "source": src_bone_name, "target": tgt_bone_name}``
    for every role present in *both* profiles.
    """
    src_bones = source_profile.get("bones", {})
    tgt_bones = target_profile.get("bones", {})
    pairs = []
    for role in CANONICAL_ROLES:
        if role in src_bones and role in tgt_bones:
            pairs.append({
                "role": role,
                "source": src_bones[role],
                "target": tgt_bones[role],
            })
    return pairs
