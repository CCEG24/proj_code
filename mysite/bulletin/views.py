from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .forms import BulletinUploadForm
import fitz
from ics import Calendar, Event
from datetime import datetime, timedelta
import re

def extract_pdf_text_from_file(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    return text

def extract_week_start_date(text):
    """
    Get 'Monday 23rd June' and year from
    'Monday 23rd June to Sunday 29th June 2025'
    """
    # Match 'Monday 23rd June'
    match = re.search(r"Monday (\d{1,2}(?:st|nd|rd|th)? \w+)", text)
    if not match:
        raise ValueError("Week start date not found in header")
    raw_date = match.group(1)
    # Remove ordinal suffix
    clean_date = re.sub(r"(st|nd|rd|th)", "", raw_date).strip()

    # Extract year from the string (e.g., at the end)
    year_match = re.search(r"(\d{4})", text)
    if not year_match:
        raise ValueError("Year not found in header")
    year = year_match.group(1)

    # Combine and parse
    full_date = f"{clean_date} {year}"
    return datetime.strptime(full_date, "%d %B %Y")

def extract_events(text, week_start_date):
    calendar = Calendar()
    lines = text.splitlines()
    current_date = None

    weekday_header_re = re.compile(r"^(Mon|Mon|Tues?|Wed|Thurs?|Fri|Sat|Sun)\s+(\d{1,2})\s+\w+", re.IGNORECASE)
    event_time_re = re.compile(r"(\d{1,2}\.\d{2}(?:am|pm)):")

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Check for new day header
        day_match = weekday_header_re.match(line)
        if day_match:
            day_number = int(day_match.group(2))
            current_date = week_start_date.replace(day=day_number)
            i += 1
            continue

        # Check for event time
        event_time_match = event_time_re.match(line)
        if event_time_match and current_date is not None:
            time_str = event_time_match.group(1)
            # Collect summary lines
            summary_lines = []
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                # Stop if next line is empty or a new time or a new day header
                if not next_line or event_time_re.match(next_line) or weekday_header_re.match(next_line):
                    break
                summary_lines.append(next_line)
                i += 1
            summary = " ".join(summary_lines).strip()
            if summary:
                try:
                    event_time = datetime.strptime(f"{current_date.strftime('%Y-%m-%d')} {time_str}", "%Y-%m-%d %I.%M%p")
                except ValueError as e:
                    print(f"⚠️ Could not parse time: {time_str}")
                    continue
                event = Event()
                event.name = summary
                event.begin = event_time
                event.end = event_time + timedelta(hours=1)
                calendar.events.add(event)
        else:
            i += 1

    return calendar

def save_calendar(calendar, filename="school_bulletin.ics"):
    with open(filename, "w") as f:
        f.write(str(calendar))

def bulletin_upload(request):
    error_message = None
    if request.method == "POST":
        form = BulletinUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf']
            try:
                pdf_text = extract_pdf_text_from_file(pdf_file)
                week_start_date = extract_week_start_date(pdf_text)
                calendar = extract_events(pdf_text, week_start_date)
                response = HttpResponse(str(calendar), content_type='text/calendar')
                response['Content-Disposition'] = 'attachment; filename=school_bulletin.ics'
                return response
            except Exception:
                error_message = "Sorry, but there was an error processing the bulletin. Please ensure that the bulletin is a KES bulletin."
    else:
        form = BulletinUploadForm()
        error_message = None
    return render(request, "bulletin/upload.html", {"form": form, "error_message": error_message})