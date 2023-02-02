# CultureBanked/Kendraio

The exercise was to create a Kendraio App Workflow that captured the features of the mockup slide.

- [Mockup Slide](https://docs.google.com/presentation/d/1Kfd87Zx0MFwDFSoW8Z209TBrgyM5WJWjHQfYXwcTOMU/edit#slide=id.g195879d82f4_0_1)
- [Latest App Version](https://app.kendra.io/culturebanked/culturebanked)

## Construction as Workflow

The mockup slide has two parts : a form for submitting a request and a table for displaying the status. The current version of the app representation has the following Workflow Blocks:

- Initialisation
- Message - instructions for use
- Form - selection of content hosts to send requests
- Dialog - request confirmation
- Message - divider line
- Context and State (Save) - record the data
- Mapping - reshape the data
- Message - table title
- Data grid - status table

### Form

The form part, has a clearly corresponding Workflow Block, Form.

_There is the Form Builder section in the Kendraio App, but documentation seems to be lacking_

On a first pass the form has been creating as a set of simple Label:Checkbox elements. It should be possible to make this resemble the slide version more closely using a JSON uiSchema, however the standard layouts (https://jsonforms.io/examples/layouts) don't really offer any improvement. _If the layout styling can be improved without under-the-hood changes to the app is an open question._

### Status Table

At least two different options are available for potential Workflow Blocks with which to display the status. Given that the slide has features that correspond directly to HTML elements (with dynamically loaded data), the first attempt at this used a Template Block. For convenience this was wrapped in a Card Block. This wasn't very successful as the app strips elements, so the checkboxes were lost (eg, <input type='checkbox' value='Apple' />).

The current version uses a Data Grid block. This better fits the table layout of the slide version but lacks the checkbox-like elements. These are not included by default in the AG Grid component used by the app. However the use of checkboxes through modifying the underlying code is well-documented : https://blog.ag-grid.com/binding-boolean-values-to-checkboxes-in-ag-grid/

## Open Issues for Potential Live Version

### Infrastructure Questions

local copy - is an online hosted copy desirable?

user account?

dedicated mail server? with user accounts...but centralised..?

send mail, cc to local server - keep audit trail

forward from users own mail to dedicated?

using local mail, can send (smtp) but how do you handle responses?

Sending : Simple Mail Transfer Protocol (SMTP) [JS lib](https://www.smtpjs.com/)

Post Office Protocol (POP), Internet Message Access Protocol (IMAP) - preferred these days?

### Potential flow

Maybe use a single form for both tables in mockups

on submit, run through each content host with a Switch block?

### Data model

Falls out of the app UI

## Gists

**Flow creation :**

- [Flow template HTML mockup](https://github.com/kendraio/kendraio-gists/blob/main/culturebanked/gists/html/flow-template.html) - approx rendering
- [card.json](https://github.com/kendraio/kendraio-gists/blob/main/culturebanked/gists/card.json) - card block as JSON
- [strip-control-chars-sh](https://github.com/kendraio/kendraio-gists/blob/main/culturebanked/gists/strip-control-chars.sh) - remove newlines etc.
- [card-spaced.txt](https://github.com/kendraio/kendraio-gists/blob/main/culturebanked/gists/card-spaced.txt) - Card block as placed in app

### Glossary

- CultureBanked
- DST : Digital Services Tax
- OECD : Organisation for Economic Co-operation and Development https://en.wikipedia.org/wiki/OECD

--- TO MOVE ---

## App Issues

Form Builder - docs?

---

not apparent how to create a new Workflow (I renamed/saved an existing one)

Upload - save as new - http failure 500 OK

(had to overwrite?)

---

Putting form into Template block - styling is lost - sanitising?

JSON in blocks doesn't like newlines - hence strip

- is lost

JMESPath is hard! The docs aren't great, a lot of trial & error needed.

Mapping :

[context.[`Apple`,*.Apple],context.[`Google`,*.Google],context.[`Amazon`,*.Amazon],context.[`Meta`,*.Meta],context.[`YouTube`,*.YouTube]]
