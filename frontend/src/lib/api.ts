const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function createSession(
  title = "Lenny Growth Assistant"
) {
  console.log("API URL:", API_URL);

  const response = await fetch(`${API_URL}/api/sessions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      `Failed to create session: ${response.status} ${errorText}`
    );
  }

  return response.json();
}


export async function getSession(sessionId: string) {
  const response = await fetch(
    `${API_URL}/api/sessions/${sessionId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch session");
  }

  return response.json();
}