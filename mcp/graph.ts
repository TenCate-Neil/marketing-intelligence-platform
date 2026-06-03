// Microsoft Graph API client — OneDrive file operations for marketing team folder

const GRAPH_BASE = "https://graph.microsoft.com/v1.0";

async function getAccessToken(): Promise<string> {
  const res = await fetch(
    `https://login.microsoftonline.com//oauth2/v2.0/token`,
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

export async function uploadToOneDrive(fileName: string, content: Uint8Array, mimeType: string) {
  const token = await getAccessToken();
  const folderId = process.env.ONEDRIVE_FOLDER_ID;
  const res = await fetch(
    `/drives//root:/:/content`,
    {
      method: "PUT",
      headers: { Authorization: `Bearer `, "Content-Type": mimeType },
      body: content,
    }
  );
  if (!res.ok) throw new Error(`Graph : `);
  return res.json();
}

export async function getOneDriveFileUrl(fileId: string): Promise<string> {
  const token = await getAccessToken();
  const res = await fetch(`/me/drive/items//createLink`, {
    method: "POST",
    headers: { Authorization: `Bearer `, "Content-Type": "application/json" },
    body: JSON.stringify({ type: "view", scope: "organization" }),
  });
  const data = await res.json();
  return data.link.webUrl;
}
