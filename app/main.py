import asyncio
import os

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from pydantic import BaseModel
from playwright.async_api import async_playwright

from app.locators import (
    ACCEPT_COOKIES_BUTTON,
    TRACKING_INPUT,
    TRACKING_SUBMIT_BUTTON,
    TRACK_LINK_DYNAMIC,
    TRACK_LINK_FALLBACK_1,
    TRACK_LINK_FALLBACK_2,
    TRACK_LINK_JS_EVAL,
)


app = FastAPI(
    title="CAROTRANS Cloud Logistics Tracker",
    description="API for tracking a CAROTRANS shipment and generating a PDF",
    version="1.0.0"
)


class TrackingRequest(BaseModel):
    tracking_id: str


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "CAROTRANS Cloud Logistics Tracker is running"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# PLAYWRIGHT TRACKING FUNCTION
# --------------------------------------------------

async def track_carotrans(tracking_id: str):

    start_url = "https://www.carotrans.com/track/"

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

    output_folder = os.path.join(
        base_dir,
        "carotrans_outputs"
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    pdf_path = os.path.join(
        output_folder,
        f"{tracking_id}.pdf"
    )

    async with async_playwright() as p:

        browser = None

        try:

            print("🚀 Launching Chromium...")

            browser = await p.chromium.launch(
                headless=False
            )

            context = await browser.new_context()

            page = await context.new_page()

            # ------------------------------------------
            # LOAD CAROTRANS
            # ------------------------------------------

            print("🚀 Loading CAROTRANS tracking page...")

            await page.goto(
                start_url,
                timeout=60000
            )

            # ------------------------------------------
            # COOKIES
            # ------------------------------------------

            try:

                await page.locator(
                    ACCEPT_COOKIES_BUTTON
                ).click(timeout=3000)

                print("✅ Accepted cookies")

            except Exception:

                print("ℹ️ No cookie popup")

            # ------------------------------------------
            # ENTER TRACKING ID
            # ------------------------------------------

            print(
                f"📝 Tracking: {tracking_id}"
            )

            await page.fill(
                TRACKING_INPUT,
                tracking_id
            )

            await page.click(
                TRACKING_SUBMIT_BUTTON
            )

            await page.wait_for_load_state(
                "networkidle",
                timeout=15000
            )

            # ------------------------------------------
            # FIND TRACKING RESULT
            # ------------------------------------------

            selectors = [
                TRACK_LINK_DYNAMIC(tracking_id),
                TRACK_LINK_FALLBACK_1,
                TRACK_LINK_FALLBACK_2,
            ]

            link = None

            for selector in selectors:

                try:

                    await page.wait_for_selector(
                        selector,
                        state="attached",
                        timeout=5000
                    )

                    link = page.locator(
                        selector
                    ).first

                    print(
                        f"✅ Link found: {selector}"
                    )

                    break

                except Exception:

                    pass

            if not link:

                print(
                    "❌ Tracking result link not found"
                )

                return None

            # ------------------------------------------
            # GET TRACKING LINK
            # ------------------------------------------

            href = await link.get_attribute(
                "href"
            )

            print(
                f"🔗 Tracking link: {href}"
            )

            await link.scroll_into_view_if_needed()

            # ------------------------------------------
            # CLICK TRACKING RESULT
            # ------------------------------------------

            actions = [

                lambda: link.click(
                    timeout=10000
                ),

                lambda: link.click(
                    force=True,
                    timeout=10000
                ),

                lambda: page.evaluate(
                    TRACK_LINK_JS_EVAL
                )
            ]

            clicked = False

            for i, action in enumerate(
                actions,
                1
            ):

                try:

                    await action()

                    print(
                        f"✅ Clicked using method {i}"
                    )

                    clicked = True

                    break

                except Exception:

                    print(
                        f"⚠️ Click method {i} failed"
                    )

            if not clicked:

                print(
                    "❌ Could not open tracking result"
                )

                return None

            # ------------------------------------------
            # WAIT FOR RESULT PAGE
            # ------------------------------------------

            await page.wait_for_load_state(
                "networkidle",
                timeout=20000
            )

            await asyncio.sleep(2)

            # ------------------------------------------
            # GENERATE PDF
            # ------------------------------------------

            print(
                "📄 Generating PDF..."
            )

            await page.pdf(
                path=pdf_path,
                format="A4",
                print_background=True
            )

            print(
                f"✅ PDF saved: {pdf_path}"
            )

            print(
                f"📋 Page title: {await page.title()}"
            )

            return pdf_path

        except Exception as e:

            print(
                f"❌ CAROTRANS error: {repr(e)}"
            )

            return None

        finally:

            if browser:

                await browser.close()


# --------------------------------------------------
# RUN PLAYWRIGHT IN WORKER THREAD
# --------------------------------------------------

def run_carotrans_tracking(
    tracking_id: str
):

    return asyncio.run(
        track_carotrans(tracking_id)
    )


# --------------------------------------------------
# TRACK API
# --------------------------------------------------

@app.post("/track")
async def track(
    request: TrackingRequest
):

    tracking_id = request.tracking_id.strip()

    if not tracking_id:

        raise HTTPException(
            status_code=400,
            detail="Tracking ID is required"
        )

    print(
        f"\n🚀 Starting tracking for: {tracking_id}"
    )

    pdf_path = await run_in_threadpool(
        run_carotrans_tracking,
        tracking_id
    )

    if pdf_path is None:

        return {
            "status": "failed",
            "tracking_id": tracking_id,
            "message": "CAROTRANS tracking failed"
        }

    return {
        "status": "success",
        "tracking_id": tracking_id,
        "pdf_path": pdf_path,
        "download_url": f"/download/{tracking_id}",
        "message": "Tracking completed and PDF generated"
    }


# --------------------------------------------------
# DOWNLOAD PDF
# --------------------------------------------------

@app.get("/download/{tracking_id}")
def download_pdf(
    tracking_id: str
):

    base_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )

    pdf_path = os.path.join(
        base_dir,
        "carotrans_outputs",
        f"{tracking_id}.pdf"
    )

    if not os.path.exists(pdf_path):

        raise HTTPException(
            status_code=404,
            detail="PDF not found. Run tracking first."
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{tracking_id}.pdf"
    )