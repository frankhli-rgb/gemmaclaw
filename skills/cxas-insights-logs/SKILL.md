---
name: cxas-insights-logs
description: >-
  Query CCAI Insights logs to inspect conversation transcripts and tool calls.
  Use this when you need to check out the actual conversation logs, transcripts, 
  or AI insights for a specific GCP project using the cxas_scrapi framework.
---

# CXAS Insights Logs Query

This skill enables querying conversation logs directly from Google Cloud Contact Center AI (CCAI) Insights.
It retrieves the raw transcript segments (including speaker roles and utterances) and exposes potential tool calls and intents.

## Prerequisites

- `cxas_scrapi` must be installed in your active Python environment.
- GCP credentials must be authenticated (`gcloud auth login` or ADC).

## Usage

You can use the provided script to query recent conversations:

```bash
# Ensure you are in the correct python environment, e.g.:
# source ~/cxas-scrapi/cxas-env/bin/activate

# Fetch the last 5 conversations for a project:
python ~/dev/gemmaclaw/skills/cxas-insights-logs/scripts/query_insights_logs.py \
  --project-id "ces-deployment-dev" \
  --location "us-central1" \
  --limit 5
```

### Script Arguments

- `--project-id`: (Required) The GCP Project ID where the Insights conversations are stored.
- `--location`: (Optional) The GCP location. Defaults to `us-central1`.
- `--limit`: (Optional) Maximum number of conversations to retrieve. Defaults to 5.
- `--filter`: (Optional) A standard CCAI Insights filter string (e.g. `startTimestamp > "2026-01-01T00:00:00Z"`).

## Understanding the Output

The script connects to the CCAI Insights REST API using the internal `cxas_scrapi` HTTP client.
For each conversation, it outputs:

1. Conversation Metadata (ID, Start Time, Medium).
2. Transcript Segments (labeled by Speaker like `AGENT`, `AUTOMATED_AGENT`, `HUMAN_AGENT`).
3. Associated Dialogflow Intent data where tool calls and matched intents are logged.

When you need to investigate specific "insight logs" and tool execution paths that the agent took in production or staging, this is the primary method to fetch and analyze them without navigating the web UI.
