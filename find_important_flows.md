
# Finding important Flows

For regression testing, we needed to identify important Flows that use the HTTP Block, I did something like this and it's a useful general pattern others may want to copy:

- Go to the Kendraio Pilots document and download it as Markdown: 
https://docs.google.com/document/d/1jUj7ysme9cSrV3HyFm2AH5Sf1k-ry-PX1oOybEv6c_o/edit

## Get ALL the Flows from Flow Cloud with a command in your Terminal emulator:
```
# Using wget to get the Flows from the command line ensures it is downloaded as JSON, rather than presented with Flow Cloud to your browser:
wget https://app.kendra.io/flows 

# Rename the flows file, to be a text file so Upload File accepts it:
mv flows flows.txt
```

## Go to https://aistudio.google.com

- Add the flows.txt and Kendraio Pilots markdown file to the message prompt: Press `+`, and select "Upload File".
- Use a prompt like the following:

```
Based on the provided documents, identify important Kendraio Pilots. Then, list up to 30 key Kendraio App Flows that use the HTTP block, split into two categories: 'Flows needing login or API keys' and 'Flows that do not need login'.

For each flow, group by adapter and provide the flow name, a description, and a direct link formatted as https://app.kendra.io/{adapterName}/{flowID}.
```

**This *should* result in output like below:**

## Kendraio Pilots

These pilots are considered important based on their strategic value, such as having high user reach, direct collaborator involvement, potential funding, or demonstrating core Kendraio features.

1.  **Bandsintown**: A key pilot due to its high reach (600k artists, 85M fans) and direct collaboration with Bandsintown. It aims to solve a real-world problem for artists by creating a single interface to manage tour information, showcasing Kendraio's ability to integrate with major industry APIs.
2.  **Teosto Unidentified Works**: Highly important as it involves a major music copyright society (Teosto) to solve a significant industry problem: managing unidentified musical works. This pilot demonstrates Kendraio's potential for complex data management and rights administration in the music industry.
3.  **Kendraio Shopify / Kendraio Shop**: This pilot, in collaboration with My Green Pod, is significant because it targets the massive e-commerce sector. It aims to create a unified interface for multiple Shopify stores, demonstrating how Kendraio can aggregate data for both consumers and merchants.
4.  **Freewheelers**: A new but important pilot due to its large existing user base (45k+ registered users) and direct collaboration. This project highlights Kendraio's ability to integrate with and enhance established community platforms.
5.  **Stepping Stones Approach**: While niche, this pilot is important for its unique and high-impact use case in nuclear disarmament diplomacy. It showcases Kendraio's flexibility in handling complex document analysis and creating knowledge graphs for specialized fields.
6.  **Kendraio Task**: An essential internal pilot that demonstrates one of Kendraio's core strengths: aggregating data from multiple, disparate sources (Linear, GitHub, Google Drive) into a single, manageable dashboard.
7.  **CultureBanked Artist & GDT**: A long-standing collaboration that is crucial for demonstrating Kendraio's integration with Google Sheets as a database and its capacity to build bespoke tools for niche communities like visual artists. The GDT part explores innovative, forward-thinking concepts like digital taxation.

---

### Kendraio App flows using the HTTP block

Here are up to 30 important flows that utilize the HTTP block to connect to external APIs and services, categorized by whether they require authentication.

#### Flows needing login or API keys

These flows require some form of authentication, such as an API key, OAuth token, or user login, to function.

**Adapter: Bandsintown**
*   **Flow name:** Add Event
    *   **Description:** Provides a form to add a new event for a managed artist on Bandsintown. It uses sub-flows to find existing artists and venues.
    *   **Link:** [https://app.kendra.io/bandsintown/addEvent](https://app.kendra.io/bandsintown/addEvent)
*   **Flow name:** Edit Event
    *   **Description:** Fetches an existing event by its ID and provides a form to update its details, including lineup, venue, and status.
    *   **Link:** [https://app.kendra.io/bandsintown/editEvent](https://app.kendra.io/bandsintown/editEvent)
*   **Flow name:** List Events
    *   **Description:** After selecting a managed artist, this flow lists their past or upcoming events from the Bandsintown API and displays them in a grid.
    *   **Link:** [https://app.kendra.io/bandsintown/listEvents](https://app.kendra.io/bandsintown/listEvents)

**Adapter: Freecords**
*   **Flow name:** Dashboard
    *   **Description:** A comprehensive dashboard that retrieves a list of songs from the Freecords API. It allows users to select songs to add to a Backblaze bucket and verify the status of the uploaded files.
    *   **Link:** [https://app.kendra.io/freecords/dashboard](https://app.kendra.io/freecords/dashboard)

**Adapter: Google Drive (googledrive)**
*   **Flow name:** List Documents
    *   **Description:** Authenticates with a user's Google account (via Auth0) and lists files from their Google Drive.
    *   **Link:** [https://app.kendra.io/GoogleDrive/listDocs](https://app.kendra.io/GoogleDrive/listDocs)
*   **Flow name:** List Comments
    *   **Description:** A sub-flow that takes a file ID and lists all associated comments, including author, content, and resolution status.
    *   **Link:** [https://app.kendra.io/GoogleDrive/listComments](https://app.kendra.io/GoogleDrive/listComments)

**Adapter: Kendraio Backstage (backstage)**
*   **Flow name:** Dashboard
    *   **Description:** Connects to a Hasura database to display a full list of scheduled gigs. It includes options to edit, delete, and add new gigs, artists, and venues.
    *   **Link:** [https://app.kendra.io/backstage/dashboard](https://app.kendra.io/backstage/dashboard)
*   **Flow name:** Add Gig
    *   **Description:** A form-based workflow to add a new gig to the Hasura database, with sub-flows to find and link existing artists and venues.
    *   **Link:** [https://app.kendra.io/backstage/addgig](https://app.kendra.io/backstage/addgig)

**Adapter: Kendraio Task (task)**
*   **Flow name:** Fetch Linear Issues
    *   **Description:** Connects to the Linear API using a personal token to fetch a list of all issues, formatting them for display in a unified dashboard.
    *   **Link:** [https://app.kendra.io/task/fetchlinearissues](https://app.kendra.io/task/fetchlinearissues)
*   **Flow name:** Fetch GitHub Issues
    *   **Description:** Uses the GitHub GraphQL API with a personal token to fetch all open issues from a specified repository (kendraio/kendraio-app).
    *   **Link:** [https://app.kendra.io/task/fetchgithubissues](https://app.kendra.io/task/fetchgithubissues)
*   **Flow name:** Fetch Google Drive Comments
    *   **Description:** Authenticates with Google, lists all Drive files, and then iterates through each file to fetch its comments, creating a unified list of tasks.
    *   **Link:** [https://app.kendra.io/task/fetchgoogledrivecomments](https://app.kendra.io/task/fetchgoogledrivecomments)

**Adapter: Shopify**
*   **Flow name:** Shopify Products
    *   **Description:** Connects to a Shopify store using a private token and shop hostname. It fetches a specified number of products and displays them in a grid and as a gallery of product cards.
    *   **Link:** [https://app.kendra.io/shopify/products](https://app.kendra.io/shopify/products)

**Adapter: Teosto**
*   **Flow name:** Unidentified Works List
    *   **Description:** Loads a JSON file of unidentified works and allows users to search and filter them. Selected works can be commented on and prepared for submission.
    *   **Link:** [https://app.kendra.io/teosto/unidentifiedWorksList](https://app.kendra.io/teosto/unidentifiedWorksList)

**Adapter: YouTube**
*   **Flow name:** YouTube: Video: List and Edit
    *   **Description:** After authenticating with Google, this flow lists the user's YouTube videos and allows them to select a video to edit its metadata (title, description, tags, privacy status).
    *   **Link:** [https://app.kendra.io/youtube/bl1JysracnItvndPkIIo](https://app.kendra.io/youtube/bl1JysracnItvndPkIIo)

**Adapter: Valueflows**
*   **Flow name:** List Scopes
    *   **Description:** Connects to the ValueFlows API to list all organizational scopes, allowing a user to view commitments within a specific scope.
    *   **Link:** [https://app.kendra.io/valueflows/listScopes](https://app.kendra.io/valueflows/listScopes)
*   **Flow name:** List Commitments
    *   **Description:** Fetches and displays a detailed list of commitments (tasks, deliverables) for a selected organizational scope, including quantities, providers, and receivers.
    *   **Link:** [https://app.kendra.io/valueflows/listCommitments](https://app.kendra.io/valueflows/listCommitments)

#### Flows that do not need login

These flows connect to public APIs and do not require any user-specific authentication.

**Adapter: Kendraio**
*   **Flow name:** Coronavirus dashboard
    *   **Description:** The main dashboard that combines several sub-flows to display global, historical, and country-specific COVID-19 statistics.
    *   **Link:** [https://app.kendra.io/kendraio/coronavirus](https://app.kendra.io/kendraio/coronavirus)
*   **Flow name:** Coronavirus By Country
    *   **Description:** Fetches historical data for specific countries from a public API and displays cases, deaths, and recoveries over time on a line chart.
    *   **Link:** [https://app.kendra.io/kendraio/coronavirusByCountry](https://app.kendra.io/kendraio/coronavirusByCountry)
*   **Flow name:** Coronavirus Global
    *   **Description:** Retrieves daily global statistics and displays the trend of confirmed cases and deaths on both linear and logarithmic charts.
    *   **Link:** [https://app.kendra.io/kendraio/coronavirusGlobal](https://app.kendra.io/kendraio/coronavirusGlobal)

**Adapter: MusicBrainz**
*   **Flow name:** MusicBrainz Search Artists
    *   **Description:** Provides a simple search form to query the public MusicBrainz API for artists and displays the results in a grid.
    *   **Link:** [https://app.kendra.io/musicbrainz/musicbrainzSearchArtists](https://app.kendra.io/musicbrainz/musicbrainzSearchArtists)

**Adapter: My Green Pod (mygreenpod)**
*   **Flow name:** My Green Pod Cart
    *   **Description:** Fetches a list of top-selling products from the public My Green Pod WooCommerce API, allowing users to select items and quantities to generate a mock order email.
    *   **Link:** [https://app.kendra.io/mygreenpod/cart](https://app.kendra.io/mygreenpod/cart)

**Adapter: Stepping Stones (steppingstones)**
*   **Flow name:** Stepping Stones: Proposed ideas for multilateral nuclear disarmament initiatives
    *   **Description:** Loads initiative data from a public Google Sheet and displays it in a searchable grid and as a series of informational cards.
    *   **Link:** [https://app.kendra.io/steppingstones/proposals](https://app.kendra.io/steppingstones/proposals)
*   **Flow name:** Stepping Stones Map
    *   **Description:** Uses data from a public Google Sheet to display participating countries for different nuclear disarmament treaties and proposals on a world map.
    *   **Link:** [https://app.kendra.io/steppingstones/transposedspreadsheet](https://app.kendra.io/steppingstones/transposedspreadsheet)
