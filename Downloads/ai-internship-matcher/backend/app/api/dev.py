import os
import importlib.util
from fastapi import APIRouter, HTTPException
from ..config import settings

router = APIRouter(prefix="/api/dev", tags=["dev"])


def _load_script(module_name: str, path: str):
    """Dynamically load a python script as a module given its path."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@router.post("/seed")
def seed_via_api():
    """Run project seeders (program outcomes + internships).

    This endpoint is gated by the `ALLOW_DEV_SEED` environment variable
    to avoid accidental production runs.
    """
    if not settings.ALLOW_DEV_SEED:
        raise HTTPException(status_code=403, detail="Dev seeding via API is disabled. Set ALLOW_DEV_SEED=True to enable.")

    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    scripts_dir = os.path.join(base, "scripts")

    results = {}
    # Seed program outcomes
    try:
        ppath = os.path.join(scripts_dir, "seed_program_outcomes.py")
        mod = _load_script("seed_program_outcomes", ppath)
        # call the seeded function if present
        if hasattr(mod, "seed_programs"):
            mod.seed_programs()
            results["programs"] = "ok"
        else:
            results["programs"] = "missing function"
    except Exception as e:
        results["programs"] = f"error: {e}"

    # Seed internships via RapidAPI scraper (uses its own settings)
    try:
        ipath = os.path.join(scripts_dir, "seed_internships.py")
        imod = _load_script("seed_internships", ipath)
        if hasattr(imod, "seed_database"):
            # call with defaults
            imod.seed_database()
            results["internships"] = "ok"
        else:
            results["internships"] = "missing function"
    except Exception as e:
        results["internships"] = f"error: {e}"

    return {"status": "completed", "results": results}
