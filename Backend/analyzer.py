import re


RESTRICTION_PROFILES = {
    "vegan",
    "vegetarian",
    "eggetarian",
    "halal",
    "Jain",
    "nut-free",
    "dairy-free",
    "gluten-free",
}


KNOWN_INGREDIENT_RULES = {
    "milk": {
        "vegan": ("Restricted", "Milk is animal-derived and not suitable for vegan diets."),
        "dairy-free": ("Restricted", "Milk conflicts with dairy-free diets."),
    },
    "milk solids": {
        "vegan": ("Restricted", "Milk solids are animal-derived and not suitable for vegan diets."),
        "dairy-free": ("Restricted", "Milk solids conflict with dairy-free diets."),
    },
    "cheese": {
        "vegan": ("Restricted", "Cheese is dairy and not suitable for vegan diets."),
        "dairy-free": ("Restricted", "Cheese conflicts with dairy-free diets."),
    },
    "butter": {
        "vegan": ("Restricted", "Butter is dairy and not suitable for vegan diets."),
        "dairy-free": ("Restricted", "Butter conflicts with dairy-free diets."),
    },
    "cream": {
        "vegan": ("Restricted", "Cream is dairy and not suitable for vegan diets."),
        "dairy-free": ("Restricted", "Cream conflicts with dairy-free diets."),
    },
    "whey": {
        "vegan": ("Restricted", "Whey is dairy-derived and not suitable for vegan diets."),
        "dairy-free": ("Restricted", "Whey conflicts with dairy-free diets."),
    },
    "casein": {
        "vegan": ("Restricted", "Casein is milk-derived and not suitable for vegan diets."),
        "dairy-free": ("Restricted", "Casein conflicts with dairy-free diets."),
    },
    "egg": {
        "vegan": ("Restricted", "Egg is not suitable for vegan diets."),
        "Jain": ("Restricted", "Egg conflicts with Jain dietary restrictions."),
    },
    "egg powder": {
        "vegan": ("Restricted", "Egg powder is not suitable for vegan diets."),
        "Jain": ("Restricted", "Egg powder conflicts with Jain dietary restrictions."),
    },
    "gelatin": {
        "vegan": ("Restricted", "Gelatin is animal-derived and not suitable for vegan diets."),
        "vegetarian": ("Restricted", "Gelatin is not suitable for vegetarian diets."),
        "eggetarian": ("Restricted", "Gelatin is not suitable for eggetarian diets."),
        "Jain": ("Restricted", "Gelatin conflicts with Jain dietary restrictions."),
        "halal": ("Uncertain", "Gelatin source may require halal verification."),
    },
    "gelatine": {
        "vegan": ("Restricted", "Gelatine is animal-derived and not suitable for vegan diets."),
        "vegetarian": ("Restricted", "Gelatine is not suitable for vegetarian diets."),
        "eggetarian": ("Restricted", "Gelatine is not suitable for eggetarian diets."),
        "Jain": ("Restricted", "Gelatine conflicts with Jain dietary restrictions."),
        "halal": ("Uncertain", "Gelatine source may require halal verification."),
    },
    "honey": {
        "vegan": ("Restricted", "Honey is generally not considered suitable for vegan diets."),
    },
    "wheat flour": {
        "gluten-free": ("Restricted", "Wheat flour contains gluten and conflicts with gluten-free diets."),
    },
    "barley malt": {
        "gluten-free": ("Restricted", "Barley malt contains gluten and conflicts with gluten-free diets."),
    },
    "rye flour": {
        "gluten-free": ("Restricted", "Rye flour contains gluten and conflicts with gluten-free diets."),
    },
    "almond": {
        "nut-free": ("Restricted", "Almond conflicts with nut-free diets."),
    },
    "peanut": {
        "nut-free": ("Restricted", "Peanut conflicts with nut-free diets."),
    },
    "cashew": {
        "nut-free": ("Restricted", "Cashew conflicts with nut-free diets."),
    },
    "hazelnut": {
        "nut-free": ("Restricted", "Hazelnut conflicts with nut-free diets."),
    },
    "walnut": {
        "nut-free": ("Restricted", "Walnut conflicts with nut-free diets."),
    },
    "pistachio": {
        "nut-free": ("Restricted", "Pistachio conflicts with nut-free diets."),
    },
    "garlic": {
        "Jain": ("Restricted", "Garlic conflicts with Jain dietary restrictions."),
    },
    "onion": {
        "Jain": ("Restricted", "Onion conflicts with Jain dietary restrictions."),
    },
    "potato": {
        "Jain": ("Restricted", "Potato conflicts with Jain dietary restrictions."),
    },
    "beetroot": {
        "Jain": ("Restricted", "Beetroot conflicts with Jain dietary restrictions."),
    },
    "carrot": {
        "Jain": ("Restricted", "Carrot may conflict with strict Jain dietary restrictions."),
    },
}


ADDITIVE_RULES = {
    "e120": {
        "vegan": ("Restricted", "E120 is cochineal/carmine and is insect-derived."),
        "vegetarian": ("Restricted", "E120 is cochineal/carmine and is insect-derived."),
        "eggetarian": ("Restricted", "E120 is cochineal/carmine and is insect-derived."),
        "Jain": ("Restricted", "E120 is insect-derived and conflicts with Jain dietary restrictions."),
        "halal": ("Uncertain", "E120 source and certification may require halal verification."),
    },
    "e441": {
        "vegan": ("Restricted", "E441 is gelatin and is animal-derived."),
        "vegetarian": ("Restricted", "E441 is gelatin and is not suitable for vegetarian diets."),
        "eggetarian": ("Restricted", "E441 is gelatin and is not suitable for eggetarian diets."),
        "Jain": ("Restricted", "E441 is gelatin and conflicts with Jain dietary restrictions."),
        "halal": ("Uncertain", "E441 source may require halal verification."),
    },
    "e471": {
        "vegan": ("Uncertain", "E471 may be derived from plant or animal sources."),
        "halal": ("Uncertain", "E471 origin may require halal verification."),
    },
    "e472": {
        "vegan": ("Uncertain", "E472 may be derived from plant or animal sources."),
        "halal": ("Uncertain", "E472 origin may require halal verification."),
    },
    "e322": {
        "vegan": ("Uncertain", "E322 lecithin source may vary depending on formulation."),
        "halal": ("Uncertain", "E322 source may require halal verification."),
    },
    "e542": {
        "vegan": ("Restricted", "E542 is bone phosphate and is animal-derived."),
        "vegetarian": ("Restricted", "E542 is animal-derived."),
        "eggetarian": ("Restricted", "E542 is animal-derived."),
        "Jain": ("Restricted", "E542 conflicts with Jain dietary restrictions."),
        "halal": ("Uncertain", "E542 source may require halal verification."),
    },
    "e631": {
        "vegan": ("Uncertain", "E631 may be produced from animal or plant sources."),
        "vegetarian": ("Uncertain", "E631 source may require verification."),
        "eggetarian": ("Uncertain", "E631 source may require verification."),
        "halal": ("Uncertain", "E631 source may require halal verification."),
        "Jain": ("Uncertain", "E631 source may require verification."),
    },
    "e627": {
        "vegan": ("Uncertain", "E627 may be produced from animal or plant sources."),
        "vegetarian": ("Uncertain", "E627 source may require verification."),
        "eggetarian": ("Uncertain", "E627 source may require verification."),
        "halal": ("Uncertain", "E627 source may require halal verification."),
        "Jain": ("Uncertain", "E627 source may require verification."),
    },
}


ALLERGEN_RULES = {
    "en:milk": {
        "vegan": ("Restricted", "Milk allergen indicates dairy content, which is not suitable for vegan diets."),
        "dairy-free": ("Restricted", "Milk allergen conflicts with dairy-free diets."),
    },
    "en:nuts": {
        "nut-free": ("Restricted", "Nut allergen conflicts with nut-free diets."),
    },
    "en:peanuts": {
        "nut-free": ("Restricted", "Peanut allergen conflicts with nut-free diets."),
    },
    "en:gluten": {
        "gluten-free": ("Restricted", "Gluten allergen conflicts with gluten-free diets."),
    },
    "en:wheat": {
        "gluten-free": ("Restricted", "Wheat allergen conflicts with gluten-free diets."),
    },
    "en:eggs": {
        "vegan": ("Restricted", "Egg allergen conflicts with vegan diets."),
        "Jain": ("Restricted", "Egg allergen conflicts with Jain dietary restrictions."),
    },
}


def normalize_profiles(selected_profiles):
    normalized = []
    for profile in selected_profiles or []:
        if isinstance(profile, str) and profile in RESTRICTION_PROFILES:
            normalized.append(profile)
    return normalized


def split_ingredients(text):
    if not isinstance(text, str) or not text.strip():
        return []

    parts = re.split(r",|;|\.", text)
    cleaned = []
    for part in parts:
        item = part.strip().lower()
        if item:
            cleaned.append(item)

    return cleaned


def extract_e_numbers_from_text(text):
    if not isinstance(text, str):
        return []

    matches = re.findall(r"\be\s*-?\s*(\d{3,4}[a-z]?)\b", text.lower())
    codes = []
    for match in matches:
        codes.append(f"e{match.replace(' ', '')}")
    return list(dict.fromkeys(codes))


def normalize_additive_tag(tag):
    if not isinstance(tag, str):
        return None

    tag = tag.lower().strip()
    if ":" in tag:
        tag = tag.split(":")[-1]

    tag = tag.replace("-", "").replace("_", "").strip()

    if re.match(r"^e\d{3,4}[a-z]?$", tag):
        return tag

    return None


def choose_stronger_status(current_status, new_status):
    order = {
        "Allowed": 0,
        "Uncertain": 1,
        "Restricted": 2,
    }
    return new_status if order[new_status] > order[current_status] else current_status


def evaluate_rule_map(name, selected_profiles, rule_map, default_reason):
    final_status = "Allowed"
    reasons = []

    for profile in selected_profiles:
        if profile in rule_map:
            status, reason = rule_map[profile]
            final_status = choose_stronger_status(final_status, status)
            reasons.append(reason)

            if final_status == "Restricted":
                break

    if not reasons:
        reasons.append(default_reason)

    return {
        "name": name,
        "status": final_status,
        "reason": " ".join(dict.fromkeys(reasons)),
    }


def evaluate_ingredient(name, selected_profiles):
    ingredient_name = (name or "").strip().lower()

    if not ingredient_name:
        return None

    if ingredient_name in KNOWN_INGREDIENT_RULES:
        return evaluate_rule_map(
            ingredient_name,
            selected_profiles,
            KNOWN_INGREDIENT_RULES[ingredient_name],
            "No restriction conflict found."
        )

    # simple substring alias handling
    for known_name, rule_map in KNOWN_INGREDIENT_RULES.items():
        if known_name in ingredient_name:
            return evaluate_rule_map(
                ingredient_name,
                selected_profiles,
                rule_map,
                "No restriction conflict found."
            )

    return {
        "name": ingredient_name,
        "status": "Uncertain",
        "reason": "This ingredient is not currently covered by the official input interpretation rules.",
    }


def evaluate_additive(code, selected_profiles):
    normalized_code = (code or "").strip().lower()

    if not normalized_code:
        return None

    if normalized_code in ADDITIVE_RULES:
        return evaluate_rule_map(
            normalized_code,
            selected_profiles,
            ADDITIVE_RULES[normalized_code],
            "No restriction conflict found for this additive."
        )

    return {
        "name": normalized_code,
        "status": "Uncertain",
        "reason": "This additive is not currently covered by the official input interpretation rules.",
    }


def evaluate_allergen(tag, selected_profiles):
    allergen_tag = (tag or "").strip().lower()

    if not allergen_tag:
        return None

    if allergen_tag in ALLERGEN_RULES:
        return evaluate_rule_map(
            allergen_tag,
            selected_profiles,
            ALLERGEN_RULES[allergen_tag],
            "No restriction conflict found for this allergen tag."
        )

    return {
        "name": allergen_tag,
        "status": "Uncertain",
        "reason": "This allergen tag is not currently covered by the official input interpretation rules.",
    }


def deduplicate_results(results):
    deduped = {}
    for item in results:
        if not item:
            continue

        key = item["name"].strip().lower()
        if key not in deduped:
            deduped[key] = item
        else:
            existing = deduped[key]
            stronger = choose_stronger_status(existing["status"], item["status"])

            if stronger != existing["status"]:
                deduped[key] = item
            elif item["reason"] not in existing["reason"]:
                existing["reason"] = f"{existing['reason']} {item['reason']}".strip()

    return list(deduped.values())


def get_overall_result(results):
    if any(item["status"] == "Restricted" for item in results):
        return "Restricted"

    if any(item["status"] == "Uncertain" for item in results):
        return "Uncertain"

    return "Safe"


def build_summary(overall_result):
    if overall_result == "Restricted":
        return "This product is not suitable for your selected dietary restrictions."
    if overall_result == "Uncertain":
        return "This product may not be suitable for your selected dietary restrictions."
    if overall_result == "Safe":
        return "This product appears suitable for your selected dietary restrictions."
    return "No ingredients were available for analysis."


def analyze_ingredients(ingredient_text, selected_profiles, additives_tags=None, allergens_tags=None):
    normalized_profiles = normalize_profiles(selected_profiles)

    ingredient_items = split_ingredients(ingredient_text)
    text_e_numbers = extract_e_numbers_from_text(ingredient_text)

    additive_codes = []
    for tag in additives_tags or []:
        normalized = normalize_additive_tag(tag)
        if normalized:
            additive_codes.append(normalized)

    additive_codes.extend(text_e_numbers)
    additive_codes = list(dict.fromkeys(additive_codes))

    allergen_items = [tag for tag in (allergens_tags or []) if isinstance(tag, str)]

    results = []

    for ingredient in ingredient_items:
        evaluated = evaluate_ingredient(ingredient, normalized_profiles)
        if evaluated:
            results.append(evaluated)

    for additive_code in additive_codes:
        evaluated = evaluate_additive(additive_code, normalized_profiles)
        if evaluated:
            results.append(evaluated)

    for allergen in allergen_items:
        evaluated = evaluate_allergen(allergen, normalized_profiles)
        if evaluated:
            results.append(evaluated)

    results = deduplicate_results(results)

    if not results:
        overall_result = "Uncertain"
        summary = "No ingredients were available for analysis."
    else:
        overall_result = get_overall_result(results)
        summary = build_summary(overall_result)

    return {
        "overall_result": overall_result,
        "summary": summary,
        "ingredients": results,
    }