# Frontend

The IDS-DRR Frontend is the user-facing web application that provides interactive maps and dashboards for disaster risk reduction decision-making.

**Repository**: [IDS-DRR-Frontend](https://github.com/CivicDataLab/IDS-DRR-Frontend)

## Features

- **Interactive Maps**: Visualize flood risk scores, hazard, exposure, vulnerability, and coping capacity at district and sub-district levels
- **Time-based Filtering**: View data across different time periods (monthly)
- **Boundary Selection**: Drill down from district to sub-district level
- **Indicator Selection**: Switch between different risk factors and indicators

## Tech stack

| Technology | Purpose |
|------------|---------|
| **React** | UI framework |
| **Next.js** | React framework for server-side rendering and routing |
| **GraphQL** | API query language |
| **TypeScript** | Type-safe JavaScript |
| **CSS/SCSS** | Styling |

## Prerequisites

- [Node.js](https://nodejs.org) LTS v22+
- npm (comes with Node.js)

## Local development

1. Clone the repository:

   ```bash
   git clone https://github.com/CivicDataLab/IDS-DRR-Frontend.git
   ```

2. Navigate to the project directory:

   ```bash
   cd IDS-DRR-Frontend
   ```

3. Install the dependencies:

   ```bash
   npm install --force
   ```

   `--force` is required to tolerate existing peer-dependency warnings from the React 19 / Next.js 15 ecosystem.

4. Run the dev server:

   ```bash
   npm run dev
   ```

The repository ships `.env.development` with localhost defaults that Next.js loads automatically in development. To override any of them (e.g. to point at production or staging backends), create a `.env.local`. The only values you typically need to change for local work are the backend URLs:

| Variable | Points at |
|---|---|
| `DATA_MANAGEMENT_LAYER_URL`, `NEXT_PUBLIC_DATA_MANAGEMENT_LAYER_URL` | The [Data Management API](data-management.md), which serves analytics maps, risk scores, and indicators. |
| `BACKEND_URL`, `NEXT_PUBLIC_BACKEND_URL` | A [DataSpace Backend](https://github.com/CivicDataLab/DataSpaceBackend) instance, which serves the datasets catalog and chart visualisations. Optional. See [DataSpace Integration](dataspace.md) for which features it unlocks and how map charts are wired up. |

## Configuration

The frontend reads its deployment-specific content (states list, branding assets, tile-layer URLs, feature flags, locales and messages) from a **branding package**: a small TypeScript npm package that exports a typed `config` object. The contract is defined by [ids-drr-branding-types](https://github.com/CivicDataLab/ids-drr-branding-types), pinned in `package.json`, so a contract change fails type-checking until the branding package catches up.

`package.json` resolves the branding via:

```json
"dependencies": {
  "ids-drr-branding": "file:./branding-stub"
}
```

By default that's the empty in-repo stub in the frontend's `branding-stub/`; the app builds and runs, but renders placeholder defaults (no states, no resources, no stories). Each real deployment replaces the stub with its own branding package.

### Branding package layout

A deployment ships a TypeScript npm package shaped roughly as:

```
ids-drr-<name>-branding/
├── package.json     # name = "ids-drr-branding", entry points at src/index.ts
├── src/
│   ├── index.ts     # re-exports the deployment's components and `config`
│   ├── config.ts    # the `config: DeploymentConfig` object
│   ├── assets/      # logo, hero images, favicon, state icons (imported as TS modules for Next.js bundling)
│   ├── messages/    # next-intl message catalogs
│   └── about-us/    # custom AboutPage component
└── data/
    └── glossary.csv # imported as `glossaryCsv`
```

The full contract (required fields, optional fields, component slots) lives in [ids-drr-branding-types](https://github.com/CivicDataLab/ids-drr-branding-types/blob/main/src/index.ts). The package must type-check against `Exports`, and its `config` against `DeploymentConfig`.

A simple `src/index.ts` looks like:

```ts
import type { Exports } from 'ids-drr-branding-types';

import heroBackground from './assets/heroBackground.jpg';
import logo from './assets/logo.svg';
import regionIcon from './assets/region-icon.svg';
import messagesEn from './messages/en.json';

// Optional component slots — re-export your implementations, or leave undefined.
export const AboutPage: Exports['AboutPage'] = undefined;
export const Credits: Exports['Credits'] = undefined;
export const Footer: Exports['Footer'] = undefined;
export const IntroSection: Exports['IntroSection'] = undefined;
export const OutroSection: Exports['OutroSection'] = undefined;
export const PartnerLogos: Exports['PartnerLogos'] = undefined;

export const config: Exports['config'] = {
  logo,
  heroBackground: heroBackground.src,
  states: [
    {
      name: 'Example Region',
      slug: 'example-region',
      icon: regionIcon,
      status: 'active',
    },
  ],
  messages: { en: messagesEn },
};
```

For larger deployments, factor the `config` object out into its own `src/config.ts`. For concrete examples to crib from, see the [India and Paraguay branding packages linked here](index.md#is-this-for-me).

### Installing your own branding

By default, the in-repo stub is installed. To use your own branding package, choose the method matching how you run the frontend.

#### npm

Install your branding directly into `node_modules` without touching `package.json` or `package-lock.json`. For example:

```bash
npm install --no-save --install-links file:../my-branding
```

- `--no-save` keeps the lockfile pinned to the stub, so contributors and CI are unaffected.
- `--install-links` copies the package contents rather than symlinking, so its transitive dependencies resolve correctly.

Re-apply after any subsequent `npm install` or `npm ci`, as those revert `node_modules/ids-drr-branding` back to the stub. To return to the stub explicitly, run `npm install --force`.

#### Docker Compose

The [docker-compose.yml](https://github.com/CivicDataLab/IDS-DRR/blob/main/docker-compose.yml) bind-mounts the entire frontend source tree (`./platform/frontend:/app`), so `branding-stub/` resolves to the in-repo stub by default. To swap in your own branding without rebuilding the image, add a new volume mounted at `/app/branding-stub`:

```{code-block} yaml
:emphasize-lines: 7

services:
  frontend:
    volumes:
      - ./platform/frontend:/app
      - /app/node_modules
      - /app/.next
      - ./platform/my-branding:/app/branding-stub:ro
```

The added mount overrides the stub; Webpack resolves `ids-drr-branding` through `node_modules/ids-drr-branding` → `../branding-stub/` → your bind-mounted branding package.

### Internationalization

The frontend uses [next-intl](https://next-intl.dev/) for translations. Two sources of messages feed into it:

- **Frontend-owned** messages live under the frontend's `locales/<locale>.json`: defaults for UI chrome, error messages, navigation labels.
- **Deployment-owned** messages live in the branding package under `src/messages/<locale>.json`, plugged in via `config.messages`. Branding messages can introduce locales the frontend doesn't ship, override the frontend's defaults for any key, or both.

To add a new locale to a deployment, create `src/messages/<locale>.json` in the branding package and add the locale to `config.locales` (and, if desired, `config.defaultLocale`).

The Paraguay branding demonstrates introducing new locales (Spanish and Guaraní). The India branding demonstrates overriding the frontend's default English messages.

Right-to-left scripts (Arabic, Urdu, etc.) are **not currently supported**; the layout, components, and stylesheets assume left-to-right scripts. If interested in RTL support, see [Contributing](contributing.md).

### PDF report (opt-in)

The analytics page can show a "Download Report" button that fetches a PDF from the backend's `/report` endpoint. Both the button and the endpoint are **off by default** because the platform does not ship a PDF generator: the report's content, layout, and methodology are deployment-specific (fiscal-year conventions, currency, indicator vocabulary, statutory annexures, etc.), so producing it is the deployment's responsibility.

To turn the button on in the frontend, set the flag in the branding package's `src/config.ts`:

```ts
export const config: DeploymentConfig = {
  // ...
  features: {
    reports: true,
  },
};
```

The button then issues a download request to:

```
GET ${NEXT_PUBLIC_DATA_MANAGEMENT_LAYER_URL}/report?geo_code=<state-code>&time_period=<YYYY_MM>
```

The endpoint must respond with `Content-Type: application/pdf` (and ideally a `Content-Disposition: attachment; filename="..."` header so the browser names the saved file). Non-2xx responses surface as the user's browser-default download failure.

For a worked example, see [ids-drr-india-plugin](https://github.com/CivicDataLab/ids-drr-india-plugin): a Django app that replaces the Data Management API's empty `plugin-stub` to add a `/report` endpoint. For more, see [Data Management → PDF Report (opt-in)](data-management.md#pdf-report-opt-in).

If the frontend flag is on but no backend implementation is installed, the button renders, but clicks return 404.

## Environment variables

The full set of variables you can set in `.env.local` (e.g. to point at production or staging backends):

| Variable | Description | Example |
|----------|-------------|-----------------|
| `DATA_MANAGEMENT_LAYER_URL` | Data Management API URL (server-side) | `https://drr.backend.open-contracting.in` |
| `NEXT_PUBLIC_DATA_MANAGEMENT_LAYER_URL` | Data Management API URL (client-side) | `https://drr.backend.open-contracting.in` |
| `BACKEND_URL` | DataSpace API URL (server-side) | `https://api.dataspace.open-contracting.in` |
| `NEXT_PUBLIC_BACKEND_URL` | DataSpace API URL (client-side) | `https://api.dataspace.open-contracting.in` |
| `SITE_URL` | Public site URL, used for `<meta>` tags (`og:url`, `og:image`, etc.), `<link>` tags (manifest, icons), and sitemap generation. Defaults to `http://localhost:3000` in development. | `https://drr.open-contracting.in` |
| `NEXT_PUBLIC_TIME_PERIOD` | Fallback time period (e.g. `2024_08`) used when the API doesn't return one. If unset, the app uses the latest available time period from the API when possible. | `2024_08` |

### Analytics

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_GOOGLE_ANALYTICS_APP_ID` | [Google Analytics](https://analytics.google.com/) measurement ID. If unset, the Google Analytics script is not loaded. |
| `NEXT_PUBLIC_HOTJAR_ID` | [Hotjar](https://www.hotjar.com/) site ID. If unset, the Hotjar script is not loaded. |
| `GOOGLE_SITE_VERIFICATION` | [Google Search Console](https://search.google.com/search-console) verification token. Rendered as a `<meta>` tag. |

### Sentry

[Sentry](https://docs.sentry.io/platforms/javascript/guides/nextjs/) is configurable for error reporting. When no DSN is configured, the Sentry SDK initializes but is disabled; no errors are sent and no network requests are made.

| Variable | Description | Required for |
|----------|-------------|-------------|
| `SENTRY_DSN_URL` | Sentry DSN for server-side error reporting | Runtime error reporting |
| `NEXT_PUBLIC_SENTRY_DSN_URL` | Sentry DSN for client-side error reporting | Runtime error reporting |
| `SENTRY_AUTH_TOKEN` | Auth token for uploading source maps | CI/production builds only |
| `SENTRY_ORG_NAME` | Sentry organization slug | CI/production builds only |
| `SENTRY_PROJECT_NAME` | Sentry project slug | CI/production builds only |
| `SENTRY_URL` | Sentry instance URL (only if self-hosting Sentry) | CI/production builds only |

The `SENTRY_AUTH_TOKEN`, `SENTRY_ORG_NAME`, `SENTRY_PROJECT_NAME`, and `SENTRY_URL` variables are only used during builds to upload source maps. They have no effect at runtime or in development.

## Running tests

```bash
npm run test
```
