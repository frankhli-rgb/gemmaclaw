import { GoogleAuth } from 'google-auth-library';

async function main() {
  try {
    const auth = new GoogleAuth({
      scopes: ['https://www.googleapis.com/auth/cloud-platform']
    });
    const client = await auth.getClient();
    const token = await client.getAccessToken();
    if (!token.token) {
      throw new Error('No access token returned');
    }
    process.stdout.write(token.token);
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
}

main();
