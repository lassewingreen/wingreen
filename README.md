# wingreen.dk

Lasse Wingreen's personal website, hosted on GitHub Pages.

## Running and publishing

The site uses plain HTML, CSS and JavaScript. No install, server runtime or build
step is required on GitHub Pages. Keep `CNAME` and `.nojekyll` when publishing.
Manrope is self-hosted in `assets/fonts/`, with its Open Font License alongside it.
The music video loads from Wistia only after the visitor presses Play.

Review the local `index.html`, then commit and push the complete change in GitHub
Desktop. Include removal of the old unencrypted application files in that commit.
GitHub Pages will publish using the repository's configured deployment settings.

## Public and private documents

- `/career/` is a public professional overview, with no application list.
- `/career/cv.html` and the CV PDF are public.
- `/career/application.html` is a privately shared, password-encrypted application.
- The old application HTML URL redirects to the password page.

The encrypted letter and PDF use AES-256-GCM with PBKDF2-SHA256 (600,000
iterations), random salt and IV. Decryption happens in the visitor's browser.
No password, decryption key or plaintext private source belongs in this repository.
The private rebuild tool, original letter and generated password are kept outside
the repository. Use that private tool to rebuild the encrypted page after edits.

The encrypted page works over HTTPS and localhost; direct file access depends on
the browser's Web Crypto support. A noindex directive is not access control.

The previous application was already published in this public repository. These
changes protect the current encrypted files after deployment. They do not remove
the earlier plaintext from Git history or from previously downloaded copies.
