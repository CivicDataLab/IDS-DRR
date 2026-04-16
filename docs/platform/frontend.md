# Frontend

The IDS-DRR Frontend is the user-facing web application that provides interactive maps, dashboards, and reports for disaster risk reduction decision-making.

**Repository**: [IDS-DRR-Frontend](https://github.com/CivicDataLab/IDS-DRR-Frontend)

## Features

- **Interactive Maps**: Visualize flood risk scores, hazard, exposure, vulnerability, and coping capacity at district and revenue circle levels
- **Time-based Filtering**: View data across different time periods (monthly)
- **Boundary Selection**: Toggle between district and revenue circle views
- **Indicator Selection**: Switch between different risk factors and indicators
- **Reports**: Generate tailored reports for specific administrative units

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **React** | UI framework |
| **Next.js** | React framework for SSR and routing |
| **GraphQL** | API query language |
| **TypeScript** | Type-safe JavaScript (89.3%) |
| **CSS/SCSS** | Styling |

## Dependencies

The following dependencies must be available globally on your system:

- [Node.js](https://nodejs.org/en/) LTS v18+
- npm (comes with Node.js)

## Installation & Setup

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

## Usage

After completing the installation steps, run the project locally:

```bash
npm run dev
```

No `.env` file is required for local development. The included `.env.development` file contains:

```
DATA_MANAGEMENT_LAYER_URL="http://localhost:8000"
NEXT_PUBLIC_DATA_MANAGEMENT_LAYER_URL="http://localhost:8000"
BACKEND_URL=
NEXT_PUBLIC_BACKEND_URL=
```

The first two point to the [Data Management API](data-management.md), which serves analytics maps, risk scores, and indicators.

The last two point to the [DataSpace Backend](https://github.com/CivicDataLab/DataSpaceBackend), which serves the datasets catalog and search. DataSpace is optional.

## Environment Variables

Create a `.env.local` file to override any value (e.g. to point at production or staging backends).

| Variable | Description | Example |
|----------|-------------|-----------------|
| `DATA_MANAGEMENT_LAYER_URL` | Data Management API URL (server-side) | `https://drr.backend.open-contracting.in` |
| `NEXT_PUBLIC_DATA_MANAGEMENT_LAYER_URL` | Data Management API URL (client-side) | `https://drr.backend.open-contracting.in` |
| `BACKEND_URL` | DataSpace API URL (server-side) | `https://api.dataspace.open-contracting.in` |
| `NEXT_PUBLIC_BACKEND_URL` | DataSpace API URL (client-side) | `https://api.dataspace.open-contracting.in` |
| `SITE_URL` | Public site URL, used for `<meta>` tags (`og:url`, `og:image`, etc.), `<link>` tags (manifest, icons), and sitemap generation. Defaults to `http://localhost:3000` in development. | `https://drr.open-contracting.in/en` |
| `NEXT_PUBLIC_TIME_PERIOD` | Fallback time period (e.g. `2024_08`) used when the API doesn't return one. If unset, the app uses the latest available time period from the API when possible. | `2024_08` |

### Analytics

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_GOOGLE_ANALYTICS_APP_ID` | [Google Analytics](https://analytics.google.com/) measurement ID. If unset, the Google Analytics script is not loaded. |
| `NEXT_PUBLIC_HOTJAR_ID` | [Hotjar](https://www.hotjar.com/) site ID. If unset, the Hotjar script is not loaded. |
| `GOOGLE_SITE_VERIFICATION` | [Google Search Console](https://search.google.com/search-console) verification token. Rendered as a `<meta>` tag. |

### Sentry

[Sentry](https://docs.sentry.io/platforms/javascript/guides/nextjs/) is used for error reporting. When no DSN is configured, the Sentry SDK initializes but is disabled; no errors are sent and no network requests are made.

| Variable | Description | Required for |
|----------|-------------|-------------|
| `SENTRY_DSN_URL` | Sentry DSN for server-side error reporting | Runtime error reporting |
| `NEXT_PUBLIC_SENTRY_DSN_URL` | Sentry DSN for client-side error reporting | Runtime error reporting |
| `SENTRY_AUTH_TOKEN` | Auth token for uploading source maps | CI/production builds only |
| `SENTRY_ORG_NAME` | Sentry organization slug | CI/production builds only |
| `SENTRY_PROJECT_NAME` | Sentry project slug | CI/production builds only |
| `SENTRY_URL` | Sentry instance URL (only if self-hosting Sentry) | CI/production builds only |

The `SENTRY_AUTH_TOKEN`, `SENTRY_ORG_NAME`, `SENTRY_PROJECT_NAME`, and `SENTRY_URL` variables are only used during builds to upload source maps. They have no effect at runtime or in local development.

## Running Tests

```bash
npm run test
```

## Get Involved

- Start by reading the [Code of Conduct](https://github.com/CivicDataLab/IDS-DRR-Frontend)
- Get familiar with the contributor guidelines explaining the different ways you can support this project
