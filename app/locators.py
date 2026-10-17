# locators.py

# Static selectors
ACCEPT_COOKIES_BUTTON = "button:has-text('Accept')"
TRACKING_INPUT = "input#js-tracking-input"
TRACKING_SUBMIT_BUTTON = "button#tracker-submit"

# Dynamic base for tracking link (will be formatted in main script)
TRACK_LINK_DYNAMIC = lambda tracking_id: f"a[href*='CRW/{tracking_id}']"

# Fallback selectors
TRACK_LINK_FALLBACK_1 = "div.section.clearfix a[href*='CRW/S']"
TRACK_LINK_FALLBACK_2 = "a[href*='CRW']"

# JS selector (for eval fallback)
TRACK_LINK_JS_EVAL = "document.querySelector(\"a[href*='CRW']\")?.click()"
