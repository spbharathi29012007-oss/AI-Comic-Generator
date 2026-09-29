from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from reportlab.pdfgen import canvas
from fastapi.responses import FileResponse
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    panels = [
        {
            "title": "Panel 1",
            "image": "",
            "description": f"{character_name} begins an adventure in {setting}.",
            "caption": story_prompt,
            "narration": f"The story begins with a {tone} mood."
        },
        {
            "title": "Panel 2",
            "image": "",
            "description": f"{character_name} continues the adventure.",
            "caption": "A new moment begins.",
            "narration": f"The artwork style is {art_style}."
        }
    ]

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={"panels": panels}
    )


@app.get("/export")
def export_success():

    file_path = "comic.pdf"

    pdf = canvas.Canvas(file_path)

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(180, 750, "AI Comic Generator")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 700, "Your comic has been generated successfully!")

    pdf.save()

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="comic.pdf"
    )