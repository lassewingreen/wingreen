Lasse Wingreen — career documents
Prepared 28 October 2026

Open dedalus.html for the tailored application, or cv.html for the CV.
Both work directly from disk, without a server, network connection or build step.
The two PDF files are ready for download from the pages or direct review.

Content is in content.json. To regenerate the HTML and PDFs after editing:
  python3 -m pip install reportlab
  python3 build.py
Run the install only if ReportLab is unavailable. The builder uses Georgia and
Arial on macOS, with built-in PDF font fallbacks on other systems. A different
font can affect pagination; inspect the rebuilt PDFs before sending them.

style.css controls the web layout and browser print styles. site.js only enables
the Print button. Navigation, content and PDF downloads work without JavaScript.

This folder is a local draft. No application has been submitted and no deployment
or Git push has been performed. The existing personal-site homepage is untouched.
The pages contain no external assets, analytics, tracking or third-party requests.
The noindex tag asks search engines not to index the pages; it is not access control.

Review before use: iPaper's end year is provisionally 2026, based on your statement
that you were recently let go; the contractual end date has not been supplied.
AccuRanker is shown as 2017, following the latest CV. Older CVs say 2016–2017.
No release, compliance, certification or measured-result claims have been added.

The full archive audit, writing-voice map and research citations are kept outside
the website folder in the task's output/wingreen-review directory.
