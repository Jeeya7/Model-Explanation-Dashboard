import type { TreeDTO } from "./types";

export async function trainTree() {
  const res = await fetch("/api/train", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error(`Train failed: ${res.status}`);
  }

  return res.json() as Promise<TreeDTO>;
}
