import argparse
import sys
from cxas_scrapi.core.insights import Insights

def main():
    parser = argparse.ArgumentParser(description="Fetch CCAI Insights Logs and Tool Calls.")
    parser.add_argument("--project-id", required=True, help="GCP Project ID")
    parser.add_argument("--location", default="us-central1", help="GCP Location")
    parser.add_argument("--limit", type=int, default=5, help="Number of conversations to fetch")
    parser.add_argument("--filter", default="", help="Filter string (e.g. 'startTimestamp > \"2023-01-01T00:00:00Z\"')")
    args = parser.parse_args()

    insights_client = Insights(project_id=args.project_id, location=args.location)
    
    params = {"pageSize": args.limit, "view": "FULL"}
    if args.filter:
        params["filter"] = args.filter

    path = f"projects/{args.project_id}/locations/{args.location}/conversations"
    print(f"Querying {args.limit} conversations from {path}...")
    
    try:
        response = insights_client._request("GET", path, params=params)
        conversations = response.get("conversations", [])
        
        if not conversations:
            print("No conversations found.")
            return

        for conv in conversations:
            print(f"\n{'='*50}")
            print(f"Conversation ID: {conv.get('name')}")
            print(f"Start Time: {conv.get('startTime')}")
            print(f"Medium: {conv.get('medium')}")
            print(f"Language: {conv.get('languageCode')}")
            
            transcript = conv.get("transcript", {}).get("transcriptSegments", [])
            print(f"\n--- Transcript ({len(transcript)} segments) ---")
            for seg in transcript:
                speaker = seg.get("segmentParticipant", {}).get("role", "UNKNOWN")
                text = seg.get("text", "")
                print(f"[{speaker}]: {text}")
                
            # Also check for dialogflow data (where tool calls might hide)
            df_data = conv.get("dialogflowIntents", {})
            if df_data:
                print(f"\n--- Dialogflow Intents ---")
                for intent, match in df_data.items():
                    print(f"Intent: {intent} (Match: {match})")
                    
    except Exception as e:
        print(f"Error querying Insights: {e}")

if __name__ == "__main__":
    main()
