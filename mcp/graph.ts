// Microsoft Graph API — OneDrive operations scoped to the shared marketing team folder

const GRAPH_BASE = "https://graph.microsoft.com/v1.0";

async function getAccessToken(): Promise<string> {
  const res = await fetch(
    `https://login.microsoftonline.com/${process.env.AZURE_AD_TENANT_ID}/oauth2/v2.0/token`,
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "client_credentials",
        client_id: process.env.AZURE_AD_CLIENT_ID!,
        client_secret: process.env.AZURE_AD_CLIENT_SECRET!,
        scope: "https://graph.microsoft.com/.default",
      }),
    }
  );
  const data = await res.json();
  return data.access_token;
}

export async function uploadToOneDrive(fileName: string, content: Buffer, mimeType: string) {
  const token = await getAccessToken();
  const folderId = process.env.ONEDRIVE_FOLDER_ID;
  const res = await fetch(`${GRAPH_BASE}/drives/${folderId}/root:/${fileName}:/content`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": mimeType },
    body: content,
  });
  if (!res.ok) throw new Error(`Graph ${res.status}: ${await res.text()}`);
  return res.json();
}

export async function getOneDriveFileUrl(fileId: string): Promise<string> {
  const token = await getAccessToken();
  const res = await fetch(`${GRAPH_BASE}/me/drive/items/${fileId}/createLink`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ type: "view", scope: "organization" }),
  });
  const data = await res.json();
  return data.link.webUrl;
}
