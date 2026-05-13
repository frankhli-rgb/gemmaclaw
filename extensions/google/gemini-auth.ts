import { parseGoogleOauthApiKey } from "./oauth-token-shared.js";

export function parseGeminiAuth(apiKey: string): { headers: Record<string, string> } {
  const parsed = apiKey.startsWith("{") ? parseGoogleOauthApiKey(apiKey) : null;
  if (parsed?.token || apiKey.startsWith("ya29.")) {
    const token = parsed?.token ?? apiKey;
    return {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    };
  }

  return {
    headers: {
      "x-goog-api-key": apiKey,
      "Content-Type": "application/json",
    },
  };
}
