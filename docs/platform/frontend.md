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
   npm install --legacy-peer-deps
   ```

4. Create your local environment configuration from the sample file:

   ```bash
   cp env.sample .env.local
   ```

## Usage

After completing the installation steps, run the project locally:

```bash
npm run dev
```

## Running Tests

```bash
npm run test
```

## Get Involved

- Start by reading the [Code of Conduct](https://github.com/CivicDataLab/IDS-DRR-Frontend)
- Get familiar with the contributor guidelines explaining the different ways you can support this project
