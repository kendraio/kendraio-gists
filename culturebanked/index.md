# CultureBanked/Kendraio

_first impressions, 2023-01-31_

## UI

- [Mockup Slide](https://docs.google.com/presentation/d/1Kfd87Zx0MFwDFSoW8Z209TBrgyM5WJWjHQfYXwcTOMU/edit#slide=id.g195879d82f4_0_1)
- [App Version](https://app.kendra.io/culturebanked/culturebanked)

## Infrastructure Questions

local copy - is an online hosted copy desirable?

user account?

dedicated mail server? with user accounts...but centralised..?

send mail, cc to local server - keep audit trail

forward from users own mail to dedicated?

using local mail, can send (smtp) but how do you handle responses?

Sending : Simple Mail Transfer Protocol (SMTP) [JS lib](https://www.smtpjs.com/)

Post Office Protocol (POP), Internet Message Access Protocol (IMAP) - preferred these days?

### Potential flow

Maybe use a single form for both

on submit, run through each content host with a Switch block?

### Data model

Falls out of the app UI

## Gists

**Flow creation :**

- [Flow template HTML mockup] - approx rendering
- [card.json] - card block as JSON
- [strip-control-chars-sh] - remove newlines etc.
- [card-spaced.txt] - Card block as placed in app

### Misc

Form Builder?

---

not apparent how to create a new Workflow...

Upload - save as new - http failure 500 OK

(had to overwrite?)

---

Putting form into Template block - styling is lost - sanitising?

JSON in blocks doesn't like newlines - hence strip

<input type='checkbox' value='Apple' /> - is lost

### Glossary

- CultureBanked
- DST : Digital Services Tax
- OECD : Organisation for Economic Co-operation and Development https://en.wikipedia.org/wiki/OECD
